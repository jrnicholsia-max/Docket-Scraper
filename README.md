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

## Docker usage

Build the image:

```bash
docker build -t ferc_scraper .
```

Run with default data paths:

```bash
docker run --rm -v "${PWD}:/app" -w /app ferc_scraper
```

Or use Docker Compose:

```bash
docker compose up --build
```

## Configurable input/output

The app supports:

- `--input-file` to specify the input Excel file
- `--output-file` to specify the output Excel file
- `INPUT_FILE` environment variable
- `OUTPUT_FILE` environment variable

Example:

```bash
docker run --rm -v "${PWD}:/app" -w /app -e INPUT_FILE=data/dockets_input.xlsx -e OUTPUT_FILE=data/results_output.xlsx ferc_scraper
```

## Preparing for GitHub

### Benefits of uploading to GitHub

- version control for changes
- easy collaboration and sharing
- backup and remote access
- issue tracking, pull requests, and code review
- CI/CD integration later if you want automated builds

### How to upload

```bash
git init
git add .
git commit -m "Initial Docker-ready FERC scraper"
```

Create a repository on GitHub, then:

```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

If you already have a GitHub repo, just add it as `origin` and push.
