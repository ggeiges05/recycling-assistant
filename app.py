from airtable_data import load_recycling_data

recycling_data = load_recycling_data()

print("Recycling Assistant")
print(f"Loaded {len(recycling_data)} recycling examples from Airtable.")

if not recycling_data:
    raise SystemExit("No recycling records were found.")