import csv
from pathlib import Path

# Locate the CSV relative to this Python file.
data_path = Path(__file__).parent / "data" / "recycling_data.csv"

# Read each row as a dictionary using the column names.
with data_path.open(encoding="utf-8-sig", newline="") as file:
    recycling_data = list(csv.DictReader(file))

print("SAMI Recycling Assistant")
print(f"Loaded {len(recycling_data)} recycling examples.")

# Create an alphabetical list of unique items.
items = sorted({row["Item"] for row in recycling_data})

print("\nAvailable items:")
for number, item in enumerate(items, start=1):
    print(f"{number}. {item}")

# Keep asking until the user enters a valid number.
while True:
    choice = input("\nEnter an item number: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(items):
        selected_item = items[int(choice) - 1]
        break

    print(f"Please enter a number between 1 and {len(items)}.")

# Find all conditions listed for the selected item.
matches = [
    row for row in recycling_data
    if row["Item"] == selected_item
]

print(f"\nYou selected: {selected_item}")
print("Available conditions:")
for number, row in enumerate(matches, start=1):
    print(f'{number}. {row["Condition"]}')

while True:
    choice = input("\nEnter a condition number: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(matches):
        selected_row = matches[int(choice) - 1]
        break

    print(f"Please enter a number between 1 and {len(matches)}.")

print("\nDisposal guidance:")
print(f'Item: {selected_row["Item"]}')
print(f'Condition: {selected_row["Condition"]}')
print(f'Category: {selected_row["Category"]}')
print(f'Instructions: {selected_row["Instructions"]}')
print(f'Source: {selected_row["Source"]}')
print(f'Verification status: {selected_row["VerificationStatus"]}')