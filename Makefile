# simple helpers for anonymizing n8n workflows

WORKFLOWS_DIR ?= workflows
PY            ?= python3
ANON_SCRIPT   ?= scripts/anonymize_n8n.py

.PHONY: anon anon-out check-anon

# overwrite in place
anon:
	$(PY) $(ANON_SCRIPT) $(WORKFLOWS_DIR) $(WORKFLOWS_DIR) --recursive

# write to a separate dir: make anon-out OUT=out_workflows
anon-out:
	@test -n "$(OUT)" || (echo "usage: make anon-out OUT=some_dir"; exit 2)
	$(PY) $(ANON_SCRIPT) $(WORKFLOWS_DIR) $(OUT) --recursive

# quick sanity check that no credentials blocks remain
check-anon:
	@if grep -R --line-number '"credentials":' $(WORKFLOWS_DIR); then \
		echo "[fail] credentials still present"; \
		exit 1; \
	else \
		echo "[ok] no credentials found"; \
	fi
