# Imported Ground Truth Vault

This directory serves as the static import zone for ground truth information used in Flat-File RAG threat hunting.

## Expected Formats
* **CSV Files:** Tabular mappings (e.g., `machine_owners.csv` containing hostname-to-owner matches).
* **Markdown Files:** Static vendor manuals, runbooks, or reference guides.
* **JSON Files:** Configuration snapshots or parsed static IOC tables.

*Note: Large files (>500 lines) should not be read directly by the LLM context; always use the `scripts/search_vault.py` utility to query them.*
