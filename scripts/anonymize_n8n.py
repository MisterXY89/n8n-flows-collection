#!/usr/bin/env python3
"""
anonymize n8n workflows: remove creds, scrub ids, generalize models and ua.
why: prevent leaking tokens, account names, internal ids before publishing.
"""

import argparse, json, os, re
from pathlib import Path
from copy import deepcopy

HEX32 = re.compile(r"^[0-9a-f]{32}$", re.IGNORECASE)

def scrub_parameters(p: dict):
    # collapse custom user-agent to generic to avoid fingerprinting
    hp = p.get("headerParameters", {}).get("parameters", [])
    for prm in hp:
        if isinstance(prm, dict) and prm.get("name", "").lower() == "user-agent":
            prm["value"] = "{{GENERIC_UA}}"

    # neutralize model ids to avoid vendor lock-in exposure
    mid = p.get("modelId")
    if isinstance(mid, dict) and "value" in mid:
        mid["value"] = "{{LLM_MODEL_ID}}"
        mid["cachedResultName"] = "LLM_MODEL"

    # same for other model fields used by different nodes
    if "model" in p and isinstance(p["model"], dict) and "value" in p["model"]:
        p["model"]["value"] = "{{LLM_MODEL_ID}}"
        p["model"]["cachedResultName"] = "LLM_MODEL"

    # redact notion database and block ids
    db = p.get("databaseId")
    if isinstance(db, dict):
        db["value"] = "{{NOTION_DATABASE_ID}}"
        db["cachedResultName"] = ""
        db["cachedResultUrl"] = ""

    blk = p.get("blockId")
    if isinstance(blk, dict) and "value" in blk:
        blk["value"] = "{{NOTION_BLOCK_ID}}"

    # http request auth headers: leave structure but remove actual refs if any lived here
    # (n8n typically holds creds under node.credentials, which we drop elsewhere)

def scrub_node(node: dict):
    # drop credentials blocks entirely
    node.pop("credentials", None)

    # generalize provider-specific model ids and redact ua, notion ids
    params = node.get("parameters")
    if isinstance(params, dict):
        scrub_parameters(params)

    # optional: strip node ids and canvas positions to reduce fingerprinting
    # comment the next two lines if you prefer to keep them
    # node.pop("id", None)
    # node.pop("position", None)

    # generic sweep: if a parameter looks like a raw 32-hex notion id, replace it
    for k, v in list(node.items()):
        if isinstance(v, str) and HEX32.match(v):
            node[k] = "{{NOTION_BLOCK_ID}}"

def scrub_top_level(doc: dict):
    # remove instance identifiers
    if isinstance(doc.get("meta"), dict):
        doc["meta"]["instanceId"] = "{{N8N_INSTANCE_ID}}"

def anonymize(doc: dict) -> dict:
    out = deepcopy(doc)
    nodes = out.get("nodes", [])
    if isinstance(nodes, list):
        for n in nodes:
            if isinstance(n, dict):
                scrub_node(n)
    scrub_top_level(out)
    return out

def process_file(src: Path, dst: Path):
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except Exception:
        # skip non-json or malformed files
        return False
    sanitized = anonymize(data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(sanitized, ensure_ascii=False, indent=2), encoding="utf-8")
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("in_dir", help="input directory with .json workflows")
    ap.add_argument("out_dir", help="output directory for anonymized files")
    ap.add_argument("--recursive", action="store_true", help="recurse into subdirectories")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    pattern = "**/*.json" if args.recursive else "*.json"

    count_in, count_ok = 0, 0
    for src in in_dir.glob(pattern):
        if not src.is_file():
            continue
        rel = src.relative_to(in_dir)
        dst = out_dir / rel
        count_in += 1
        if process_file(src, dst):
            count_ok += 1

    print(json.dumps({"processed": count_in, "written": count_ok, "out_dir": str(out_dir)}, indent=2))

if __name__ == "__main__":
    main()

