# Recycling Assistant

This project helps users find disposal guidance for common household
items. It provides a recycling category, preparation instructions,
a source, and a short AI-generated explanation.

The current dataset uses Town of Normal, Illinois guidance. The project
is no longer limited to SAMI residents, but the information does not
automatically apply to other locations.

## Dataset

The working data is stored in Airtable. The original CSV snapshot is
stored in `data/recycling_data.csv`.

The dataset contains 200 item-condition examples created from recycling
guidance, not observations collected from users. Some items appear more
than once because their condition changes the disposal instructions.

The three categories are:

- Recyclable
- Recyclable after preparation
- Not accepted in recycling

“Not accepted in recycling” does not automatically mean trash. Some
items may require special disposal.

Airtable contains three linked tables:

- Recycling Items: item names, conditions, instructions, and verification status.
- Categories: the three recycling categories.
- Sources: source names and website links.

## Sources and Limitations

The main sources are the Town of Normal’s guides:

- https://www.normalil.gov/482/Recyclable-Items
- https://www.normalil.gov/483/Non-Recyclable-Items

California guidance was used for comparison during development, but
the California comparison column was removed from the working dataset.
California rules do not determine what is accepted in Normal or
Bloomington, Illinois.

Normal’s guidelines may differ from other cities, apartment collection
services, or waste haulers. Users should check that the guidance applies
to their collection program.

## Data Cleaning and Checks

I saved the original dataset as CSV UTF-8 and checked its 200 rows and
six columns for missing values and duplicate item-condition pairs.
Neither check found any issues.

Category counts:

- Recyclable: 84
- Recyclable after preparation: 68
- Not accepted in recycling: 48

These checks confirm the dataset’s structure. They do not prove that
every disposal instruction is accurate or current.

## Current Prototype

The terminal prototype loads records from Airtable. Users select an
item and its condition from numbered menus. The program finds the
matching record and displays its category, instructions, source, and
verification status.

The selected record is then sent to Gemini, which turns the information
into a short explanation. The model is instructed to preserve the
stored guidance and avoid adding unsupported rules.

If the AI request fails, the original database guidance remains
available.

I previously tested all three disposal categories and invalid menu
entries. I have also confirmed that the Airtable connection and
AI explanation work for a selected record. More testing is needed
to check the AI’s accuracy across different items.

## Current Workflow

User selects an item → user selects a condition → Python finds the
matching Airtable record → Gemini writes an explanation → the program
displays the guidance and source.

The current version retrieves a record and uses it to support AI text
generation. It does not use embeddings or a vector database.

## Main Files

- `app.py`: Runs the menus and displays the results.
- `airtable_data.py`: Loads Airtable records and converts linked
  category and source IDs into readable information.
- `ai_response.py`: Sends the selected record to Gemini and returns
  its explanation.
- `data/recycling_data.csv`: Stores the original dataset snapshot.

## Running the Prototype

Create and activate a Python virtual environment, then install:

```powershell
python -m pip install requests python-dotenv
```

Create a `.env` file in the project folder:

```dotenv
AIRTABLE_TOKEN=your_airtable_token
AIRTABLE_BASE_ID=your_base_id
GEMINI_API_KEY=your_gemini_key
```

The Airtable base must contain the tables and fields expected by
`airtable_data.py`. API access and an internet connection are required.

Run:

```powershell
python app.py
```

Select an item number and then a condition number.

The `.env` file contains private credentials and must not be committed
to GitHub. Each computer needs its own environment and credentials.
Gemini API usage is subject to the account’s limits and pricing.

## Known Limitations and Next Steps

The current prototype only handles items and conditions already in the
database. It uses numbered menus rather than typed requests.

The next step is to let users type an item with or without its condition.
The backend will find matching information and ask a follow-up question
when the missing condition affects the answer.

A website will later provide the user interface. Adding new records is
also planned, with source checking and review before new guidance is
used.

AI-generated explanations can contain mistakes and still need testing.

## AI Assistance

AI was used to help create the initial dataset, develop and troubleshoot
the Python code, and write this README.

The prototype also uses Gemini to explain selected database records.
The data and generated answers still need review before being relied
on for real disposal decisions.