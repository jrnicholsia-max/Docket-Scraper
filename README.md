# Docket Scraper

A Python project that reads docket numbers from an Excel file, fetches filings from docket systems, and writes results to a dated Excel file in the user's Downloads folder.

## Supported docket systems

- FERC
- Illinois Commerce Commission

## Repository layout

- `main.py` - application entry point; for example, call `main(adapter="ferc")`
- `adapters/` - adapter (scraper or API) for supported docket systems
- `data_io.py` - input/output (i/o) utilities
- `data/` - input file (`dockets_input.xlsx`) and output template (`results_output.xlsx`)
- `paths.py` - file paths for i/o data files
- `requirements.txt` - Python dependencies

## Future priorities

- Expanding to additional state-level Public Utility Commission docket systems, prioritizing states in the Northeast (New York and New England) and PJM Interconnection footprint
- Improving filters to screen out low-importance filings (e.g., petitions to intervene, requests to update service list)
- Improving output for user-specific workflows (e.g., comment summaries)