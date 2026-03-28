import argparse
import os

from ferc_api import fetch_search_results, parse_search_hits
from excel_io import (create_docket_result_sheet, format_date_to_api,
                      load_dockets_excel, load_results_workbook)
from datetime import date


def process_dockets_from_excel(path="data/dockets_input.xlsx", output_path="data/results_output.xlsx"):
    workbook, docket_rows = load_dockets_excel(path)
    if not docket_rows:
        print(f"No docket rows found in {path}.")
        return

    try:
        results_workbook = load_results_workbook(output_path)
    except Exception as exc:
        print(f"Unable to load results workbook: {exc}")
        return

    for entry in docket_rows:
        docket = entry["docket"]
        try:
            start_date = format_date_to_api(entry["start_date"])
        except ValueError as exc:
            print(f"Skipping {docket}: invalid start date ({exc}).")
            continue

        print(f"Processing docket {docket} starting {start_date}...")
        try:
            data = fetch_search_results(docket, start_date)
        except Exception as exc:
            print(f"Fetch failed for {docket}: {exc}")
            continue

        records = parse_search_hits(data)
        if records:
            create_docket_result_sheet(results_workbook, docket, records)
            print(f"Wrote {len(records)} records to {output_path} sheet '{docket}'.")
        else:
            print(f"No records found for docket {docket}. Skipping results sheet.")

        entry["start_date_cell"].value = date.today()

    results_workbook.save(output_path)
    workbook.save(path)
    print(f"Updated start dates in {path} and saved {output_path}.")


def main():
    parser = argparse.ArgumentParser(description="Process FERC docket search input and write results.")
    parser.add_argument("--input-file", dest="input_file", help="Path to the input dockets Excel file")
    parser.add_argument("--output-file", dest="output_file", help="Path to the results output Excel file")
    args = parser.parse_args()

    input_path = args.input_file or os.getenv("INPUT_FILE", "data/dockets_input.xlsx")
    output_path = args.output_file or os.getenv("OUTPUT_FILE", "data/results_output.xlsx")

    print(f"Using INPUT_FILE={input_path} OUTPUT_FILE={output_path}")
    process_dockets_from_excel(input_path, output_path)


if __name__ == "__main__":
    main()
