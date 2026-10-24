import os
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv

"""Read every record from one Airtable table."""
def read_table(table_name, base_id, headers):

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
                f"Could not read {table_name}: HTTP {response.status_code}"
            )

        page = response.json()
        records.extend(page["records"])

        next_page = page.get("offset")

        if not next_page:
            break

        params["offset"] = next_page

    return records


"""Load Airtable data into the format used by app.py."""
def load_recycling_data():

    # 1. Load credentials.
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

    token = os.getenv("AIRTABLE_TOKEN")
    base_id = os.getenv("AIRTABLE_BASE_ID")

    if not token or not base_id:
        raise ValueError("Missing Airtable token or base ID in .env.")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Match category record IDs to category names.
    categories = {}

    for record in read_table("Categories", base_id, headers):
        record_id = record["id"]
        category_name = record["fields"]["Category Name"]

        categories[record_id] = category_name

    # 3. Match source record IDs to website URLs.
    sources = {}

    for record in read_table("Sources", base_id, headers):
        record_id = record["id"]
        website_url = record["fields"]["Website URL"]

        sources[record_id] = website_url

    # 4. Read and prepare the recycling items.
    recycling_data = []
    item_records = read_table("Recycling Items", base_id, headers)

    for record in item_records:
        fields = record["fields"]
        item_name = fields.get("Item", "")

        category_ids = fields.get("Category", [])
        source_ids = fields.get("Source", [])

        if len(category_ids) != 1:
            raise ValueError(f"{item_name} must have exactly one category.")

        if not source_ids:
            raise ValueError(f"{item_name} has no source.")

        category_id = category_ids[0]
        category_name = categories[category_id]

        source_urls = []

        for source_id in source_ids:
            website_url = sources[source_id]
            source_urls.append(website_url)

        item = {
            "Item": item_name,
            "Condition": fields.get("Condition", ""),
            "Category": category_name,
            "Instructions": fields.get("Instructions", ""),
            "Source": "; ".join(source_urls),
            "VerificationStatus": fields.get("Verification Status", "")
        }

        recycling_data.append(item)

    return recycling_data


# Run this test only when this file is executed directly.
if __name__ == "__main__":
    try:
        rows = load_recycling_data()
    except (requests.RequestException, RuntimeError, ValueError, KeyError) as error:
        raise SystemExit(f"Could not load Airtable data: {error}")

    print(f"Loaded {len(rows)} recycling records from Airtable.")

    for number, row in enumerate(rows, start=1):
        print(f"\nRecord {number}:")

        for field, value in row.items():
            print(f"{field}: {value}")