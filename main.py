from paths import input_path, output_path
from data_io import (format_date, load_dockets,
                       load_results, create_result_sheet, build_run_output_path)
from datetime import date
from importlib import import_module

ADAPTER_DEFINITIONS = {
    "ferc": {
        "module": "adapters.ferc_adapter",
        "input_sheet": "ferc",
    },
    "illinois": {
        "module": "adapters.il_adapter",
        "input_sheet": "illinois",
    },
}

ADAPTER_ALIASES = {
    "il": "illinois",
}

ALLOWED_ADAPTERS = {
    **{adapter_name: config["module"] for adapter_name, config in ADAPTER_DEFINITIONS.items()},
    **{alias: ADAPTER_DEFINITIONS[target]["module"] for alias, target in ADAPTER_ALIASES.items()},
}


def get_adapter_config(adapter_key):
    normalized = str(adapter_key).strip().lower()
    canonical = ADAPTER_ALIASES.get(normalized, normalized)
    if canonical not in ADAPTER_DEFINITIONS:
        raise ValueError(f"Unsupported adapter: {adapter_key}")
    return ADAPTER_DEFINITIONS[canonical]

def load_adapter(adapter_key):
    module_name = get_adapter_config(adapter_key)["module"]
    return import_module(module_name)

def main(adapter="ferc"):
    adapter_config = get_adapter_config(adapter)
    adapter_module = load_adapter(adapter)
    input_sheet = adapter_config["input_sheet"]
    run_output_path = build_run_output_path(adapter)
    print(
        f"Using INPUT_FILE={input_path}, TEMPLATE_OUTPUT_FILE={output_path}, "
        f"RUN_OUTPUT_FILE={run_output_path}, ADAPTER={adapter}, INPUT_SHEET={input_sheet}"
    )

    try:
        workbook, docket_rows = load_dockets(input_sheet)
    except Exception as exc:
        print(f"Unable to load dockets from worksheet '{input_sheet}': {exc}")
        return

    if not docket_rows:
        print(f"No docket rows found in worksheet '{input_sheet}' in {input_path}.")
        return

    try:
        results_workbook = load_results()
    except Exception as exc:
        print(f"Unable to load results workbook: {exc}")
        return

    for entry in docket_rows:
        docket = entry["docket"]
        try:
            start_date = format_date(entry["start_date"])
        except ValueError as exc:
            print(f"Skipping {docket}: invalid start date ({exc}).")
            continue

        print(f"Processing docket {docket} starting {start_date}...")
        try:
            data = adapter_module.fetch_search_results(docket, start_date)
        except Exception as exc:
            print(f"Fetch failed for {docket}: {exc}")
            continue

        records = adapter_module.parse_search_hits(data)
        if records:
            create_result_sheet(results_workbook, docket, records)
            print(f"Wrote {len(records)} records to {run_output_path} sheet '{docket}'.")
        else:
            print(f"No records found for docket {docket}. Skipping results sheet.")

        entry["start_date_cell"].value = date.today()

    if "TEMPLATE" in results_workbook.sheetnames:
        results_workbook.remove(results_workbook["TEMPLATE"])
    results_workbook.save(run_output_path)
    workbook.save(input_path)
    print(f"Updated start dates in {input_path} and saved {run_output_path}.")

if __name__ == "__main__":
    main(adapter="ferc")
