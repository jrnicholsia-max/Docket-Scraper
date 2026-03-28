# FERC Scraper

A small Python project that reads docket numbers from an Excel file, queries the FERC eLibrary API, and writes results back to Excel.

## Repository layout

- `main.py` - application entry point
- `ferc_api.py` - FERC API request and response parsing
- `excel_io.py` - Excel input/output utilities
- `data/` - folder for input/output Excel files
- `Dockerfile` - builds the application image
- `docker-compose.yml` - runs the container with `data/` mounted
- `requirements.txt` - Python dependencies
