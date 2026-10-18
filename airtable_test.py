import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load credentials from the .env beside this script.
load_dotenv(Path(__file__).parent / ".env")

token = os.getenv("AIRTABLE_TOKEN")
base_id = os.getenv("AIRTABLE_BASE_ID")

if not token or not base_id:
    raise SystemExit("Missing AIRTABLE_TOKEN or AIRTABLE_BASE_ID in .env.")

# Ask Airtable for the base's tables and fields.
url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
headers = {"Authorization": f"Bearer {token}"}

try:
    response = requests.get(url, headers=headers, timeout=30)
except requests.RequestException:
    raise SystemExit("Connection failed. Check your internet and try again.")

if response.status_code != 200:
    raise SystemExit(
        f"Airtable returned HTTP {response.status_code}. "
        "Check the token, base access, and schema.bases:read permission."
    )

# Display the structure without printing credentials.
data = response.json()

print("Connected to Airtable!")

for table in data["tables"]:
    print(f'\nTable: {table["name"]}')
    for field in table["fields"]:
        print(f'  - {field["name"]}: {field["type"]}')