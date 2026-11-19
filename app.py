import requests
from ai_response import create_response
from airtable_data import load_recycling_data

recycling_data = load_recycling_data()

print("Recycling Assistant")
print(f"Loaded {len(recycling_data)} recycling examples from Airtable.")

if not recycling_data:
    raise SystemExit("No recycling records were found.")

# Create an alphabetical list of unique item names.
items = sorted({row["item"] for row in recycling_data})

# Keep searching until the user selects an item or quits.
while True:
    query = input(
        "\nEnter an item name, or type 'quit' to exit: "
    ).strip()

    if query.casefold() == "quit":
        raise SystemExit("Recycling Assistant closed.")

    if not query:
        print("Please enter an item name.")
        continue

    # Look for an exact name first, ignoring capitalization.
    matching_items = []

    for item in items:
        if query.casefold() == item.casefold():
            matching_items.append(item)

    # Otherwise, search for the entered words.
    if not matching_items:
        search_words = query.casefold().split()

        for item in items:
            item_words = item.casefold().replace("-", " ").split()

            if all(word in item_words for word in search_words):
                matching_items.append(item)

    if not matching_items:
        print("No matching item was found in the database.")
        print("Try a shorter name, such as 'can' or 'cardboard'.")
        continue

    print("\nMatching items:")

    for number, item in enumerate(matching_items, start=1):
        print(f"{number}. {item}")

    while True:
        choice = input(
            "\nSelect an item number, or enter 0 to search again: "
        ).strip()

        if choice == "0":
            break

        if choice.isdigit() and 1 <= int(choice) <= len(matching_items):
            selected_item = matching_items[int(choice) - 1]
            break

        print(f"Please enter a number from 0 to {len(matching_items)}.")

    if choice != "0":
        break

# Find all condition records for the selected item.
matches = [
    row for row in recycling_data
    if row["item"] == selected_item
]

print(f"\nYou selected: {selected_item}")
print("Available conditions:")

for number, row in enumerate(matches, start=1):
    print(f'{number}. {row["condition"]}')

# Select a condition.
while True:
    choice = input("\nEnter a condition number: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(matches):
        selected_row = matches[int(choice) - 1]
        break

    print(f"Please enter a number between 1 and {len(matches)}.")

# Display the stored information.
print("\nDisposal guidance:")
print(f'Item: {selected_row["item"]}')
print(f'Condition: {selected_row["condition"]}')
print(f'Category: {selected_row["category"]}')
print(f'Instructions: {selected_row["instruction"]}')
print(f'Source: {selected_row["source"]}')

# Generate the AI explanation.
print("\nAI explanation:")

try:
    answer = create_response(selected_row)
    print(answer)
except (requests.RequestException, RuntimeError, ValueError) as error:
    print(f"AI explanation unavailable: {error}")
    print("Use the stored disposal guidance above.")