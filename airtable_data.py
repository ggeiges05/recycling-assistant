import os
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv


def read_table(table_name, base_id, headers):
    """Read every page of records from an Airtable table."""

    encoded_name = quote(table_name, safe="")
    url = f"https://api.airtable.com/v0/{base_id}/{encoded_name}"

    records = []
    params = {"pageSize": 100}

    while True:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Could not read {table_name}: "
                f"HTTP {response.status_code}"
            )

        page = response.json()
        records.extend(page["records"])

        next_page = page.get("offset")

        if not next_page:
            return records

        params["offset"] = next_page


def resolve_value(value, linked_records, field_name):
    """Accept text or convert linked record IDs into readable text."""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, list):
        values = []

        for record_id in value:
            if record_id not in linked_records:
                raise ValueError(
                    f"{field_name} has an unresolved link: {record_id}"
                )

            text = linked_records[record_id]

            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    f"The linked {field_name} record has no readable value."
                )

            values.append(text.strip())

        return "; ".join(values)

    raise ValueError(
        f"{field_name} must contain text or linked records."
    )


def load_recycling_data():
    """Load recycling records and resolve category and source links."""

    load_dotenv(Path(__file__).parent / ".env")

    token = os.getenv("AIRTABLE_TOKEN")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME", "Recycling Items")

    if not token or not base_id:
        raise ValueError("Missing Airtable token or base ID in .env.")

    headers = {"Authorization": f"Bearer {token}"}
    records = read_table(table_name, base_id, headers)

    # Load linked tables only when the item records use links.
    needs_categories = any(
        isinstance(record["fields"].get("Category"), list)
        for record in records
    )

    needs_sources = any(
        isinstance(record["fields"].get("Source"), list)
        for record in records
    )

    categories = {}

    if needs_categories:
        for record in read_table("Categories", base_id, headers):
            categories[record["id"]] = record["fields"].get(
                "Category Name", ""
            )

    sources = {}

    if needs_sources:
        for record in read_table("Sources", base_id, headers):
            sources[record["id"]] = record["fields"].get(
                "Website URL", ""
            )

    recycling_data = []

    for record in records:
        fields = record["fields"]
        record_id = record["id"]

        category_value = fields.get("Category", "")

        if isinstance(category_value, list) and len(category_value) != 1:
            raise ValueError(
                f"Record {record_id} must have exactly one linked category."
            )

        item = {
            "item": fields.get("Item", ""),
            "aliases": fields.get("Aliases", ""),
            "condition": fields.get("Condition", ""),
            "category": resolve_value(
                category_value, categories, "Category"
            ),
            "instruction": fields.get("Instructions", ""),
            "source": resolve_value(
                fields.get("Source", ""), sources, "Source"
            )
        }

        # Validate and clean the final readable values.
        for field, value in item.items():
            if not isinstance(value, str):
                raise ValueError(
                    f"Record {record_id}: {field} must contain text."
                )

            item[field] = value.strip()

        required_fields = (
            "item",
            "condition",
            "category",
            "instruction",
            "source"
        )

        for field in required_fields:
            if not item[field]:
                raise ValueError(
                    f"Record {record_id} is missing {field}."
                )

        recycling_data.append(item)

    if not recycling_data:
        raise ValueError("No recycling records were found.")

    return recycling_data


if __name__ == "__main__":
    try:
        rows = load_recycling_data()
    except (
        requests.RequestException,
        RuntimeError,
        ValueError,
        KeyError
    ) as error:
        raise SystemExit(f"Could not load Airtable data: {error}")

    unique_items = {row["item"].casefold() for row in rows}

    print(f"Loaded {len(rows)} condition records from Airtable.")
    print(f"Found {len(unique_items)} unique items.")

    print("\nFirst record:")

    for field, value in rows[0].items():
        print(f"{field}: {value}")