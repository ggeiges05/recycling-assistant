import requests
from ai_response import create_response
from airtable_data import load_recycling_data

recycling_data = load_recycling_data()

print("Recycling Assistant")
print(f"Loaded {len(recycling_data)} recycling examples from Airtable.")

if not recycling_data:
    raise SystemExit("No recycling records were found.")

# Display the available items.
items = sorted({row["Item"] for row in recycling_data})

print("\nAvailable items:")
for number, item in enumerate(items, start=1):
    print(f"{number}. {item}")

# Ask the user to select an item.
while True:
    choice = input("\nEnter an item number: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(items):
        selected_item = items[int(choice) - 1]
        break

    print(f"Please enter a number between 1 and {len(items)}.")

# Find the records for that item.
matches = [
    row for row in recycling_data
    if row["Item"] == selected_item
]

print(f"\nYou selected: {selected_item}")
print("Available conditions:")

for number, row in enumerate(matches, start=1):
    print(f'{number}. {row["Condition"]}')

# Select the condition and define selected_row.
while True:
    choice = input("\nEnter a condition number: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(matches):
        selected_row = matches[int(choice) - 1]
        break

    print(f"Please enter a number between 1 and {len(matches)}.")

# Display the original database information.
print("\nDisposal guidance:")
print(f'Item: {selected_row["Item"]}')
print(f'Condition: {selected_row["Condition"]}')
print(f'Category: {selected_row["Category"]}')
print(f'Instructions: {selected_row["Instructions"]}')
print(f'Source: {selected_row["Source"]}')
print(f'Verification status: {selected_row["VerificationStatus"]}')

# Ask Gemini to explain the selected record.
print("\nAI explanation:")

try:
    answer = create_response(selected_row)
    print(answer)
except (requests.RequestException, RuntimeError, ValueError) as error:
    print(f"AI explanation unavailable: {error}")
    print("Use the stored disposal guidance above.")