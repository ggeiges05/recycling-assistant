# Recycling Assistant

This project helps users find disposal guidance for common household
items. It provides a recycling category, preparation instructions,
sources, and a short AI-generated explanation.

The guidance focuses on Normal, Illinois. It does not automatically
apply to other locations or waste collection services.

## Dataset

The working data is stored in Airtable. A CSV snapshot is stored in
`data/recycling_data.csv`. The CSV and Airtable must be updated
separately; changing one does not automatically update the other.

The Airtable dataset has been expanded to approximately 800 records.
Records represent item-condition combinations, so this does not
necessarily mean 800 different items.

The examples were created from recycling guidance, not observations
collected from users. Some items appear in multiple records because
their condition affects the instructions.

The recycling records contain six fields:

- Item: The general name, such as Aluminum beverage can.
- Aliases: Other names, such as soda can, pop can, or energy drink can.
- Condition: The state of the item, such as empty and rinsed.
- Category: The recycling outcome.
- Instructions: Preparation steps or other disposal guidance.
- Source: The source supporting the guidance.

Aliases are separated by semicolons. They allow different names to
match the same item without adding separate records for every name.

The three categories are:

- Recyclable
- Recyclable after preparation
- Not accepted in recycling

“Not accepted in recycling” means the item is excluded from the
curbside recycling stream. It does not automatically mean trash.
Some items require separate recycling or special disposal.

Airtable also contains linked Categories and Sources tables. The Python
loader converts those linked record IDs into readable category names
and source URLs.

## Sources and Limitations

The main local sources are:

- [Town of Normal: Recyclable Items](https://www.normalil.gov/482/Recyclable-Items)
- [Town of Normal: Non-Recyclable Items](https://www.normalil.gov/483/Non-Recyclable-Items)
- [Town of Normal: Electronics Recycling](https://www.normalil.gov/484/Self-Service-Electronics-Recycling)
- [Ecology Action Center: Local Recycling Information](https://ecologyactioncenter.org/waste-and-recycling/)

Additional general guidance came from:

- [EPA: Common Recyclables](https://www.epa.gov/recycle/how-do-i-recycle-common-recyclables)

Some examples apply a general material rule to a household item.
A source may describe the material group without naming that exact
product. The dataset is not a verified ranking of the most commonly
recycled items.

California guidance was used for comparison earlier in development.
The California comparison column was removed. California rules do
not determine what is accepted locally.

Normal’s guidelines may differ from other cities, apartment collection
services, or waste haulers. General EPA guidance does not override
local acceptance rules.

## Data Preparation and Checks

The original 200-record dataset was saved as CSV UTF-8 and checked
for missing values and duplicate item-condition pairs. Neither check
found an issue.

The expanded data uses more general item names and aliases to reduce
unnecessary duplication. Verification status and jurisdiction columns
were removed from the recycling records.

The loader checks required fields and resolves category and source
links. These structural checks do not prove that every disposal
instruction is correct.

The expanded Airtable dataset still needs a complete review for
duplicate rules, missing aliases, and instruction accuracy. Previous
checks on the original dataset do not verify every newly added record.

## Current Prototype

The terminal prototype loads records from Airtable when it starts.
It retrieves additional pages automatically when the table contains
more than 100 records.

Users type an item name. The program checks item names and aliases
for an exact match. If there is no exact match, it searches the item
names for the entered words.

Matching item names are displayed once, even when the item has
multiple condition records. The user selects the intended item and
then chooses its condition.

The program displays the category, instructions, and source. It sends
the selected record to Gemini to produce a short explanation.

Gemini is instructed to preserve the stored guidance and avoid
inventing rules. It does not independently research the source
webpages in the current version.

If the AI request fails, the stored guidance remains available.
If Airtable cannot load, the current version cannot start its search.

## Current Workflow

User types an item name
→ Python searches item names and aliases
→ user selects a matching item
→ user selects its condition
→ program displays stored guidance and sources
→ Gemini generates a short explanation.

The current version retrieves structured records to support AI text
generation. It does not use embeddings or a vector database.

## Main Files

- `app.py`: Handles typed search, item and condition selection,
  and displayed results.
- `airtable_data.py`: Loads Airtable records, handles pagination,
  and resolves linked categories and sources.
- `ai_response.py`: Sends the selected record to Gemini and
  returns its explanation.
- `data/recycling_data.csv`: Stores a local dataset snapshot.

## Running the Prototype

Clone the repository:

```powershell
git clone https://github.com/ggeiges05/recycling-assistant.git
cd recycling-assistant
```

Create and activate a Python virtual environment. For a standard
Windows Python installation:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install requests python-dotenv
```

Create a `.env` file in the project folder:

```dotenv
AIRTABLE_TOKEN=your_airtable_token
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=Recycling Items
GEMINI_API_KEY=your_gemini_key
```

Set `AIRTABLE_TABLE_NAME` to the actual table name if it differs.

The current loader expects these capitalized Airtable fields:

```text
Item
Aliases
Condition
Category
Instructions
Source
```

For linked fields, it also expects:

- Categories table: Category Name
- Sources table: Website URL

The loader converts the Airtable field names into lowercase keys
for the rest of the Python code.

Run:

```powershell
python app.py
```

Enter an item name, select a matching item, and choose its condition.
Type `quit` at the item-search prompt to exit.

An internet connection and authorized Airtable access are required.
A Gemini key is needed for AI explanations. Without it, the program
still displays the stored guidance before reporting that AI is
unavailable.

The `.env` file contains private credentials and must not be committed
to GitHub. Each computer needs its own environment and credentials.

## Testing and Evaluation

The Airtable connection, typed search, alias matching, condition
selection, and AI explanation have been tested during development.

More testing is needed across the expanded dataset. Evaluation will
check whether:

- Search returns the intended item without duplicate suggestions.
- The selected condition returns the correct stored rule.
- AI preserves the category and required preparation steps.
- AI avoids unsupported disposal claims.
- Invalid input and service failures are handled clearly.

Response-time measurements are also planned. Accuracy percentages
and performance results will be reported after testing.

## Known Limitations and Next Steps

The current prototype runs in the terminal. It does not have a website
or public deployment yet.

Search supports item names and stored aliases. It does not currently
interpret full questions, automatically extract conditions from
sentences, or reliably correct spelling mistakes.

Unknown items are not researched or classified automatically.
Users can only select conditions present in the database.

The next step is a simple website connected to a Python backend.
The backend will manage Airtable and Gemini credentials so website
users will not need their own API keys or database access.

A sample-data mode is also planned to make local testing easier
without Airtable credentials. The current terminal version does
not automatically fall back to the CSV.

Public deployment will require backend hosting, private credential
storage, and handling of service limits. These access issues need
to be resolved before other users can use the hosted application.

## AI Assistance

AI helped create and organize dataset examples, develop and troubleshoot
the Python code, and write this README.

The prototype also uses Gemini to explain selected records. The data
and generated explanations still need review before being relied on
for real disposal decisions.