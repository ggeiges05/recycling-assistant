# SAMI Recycling Assistant

This project will help SAMI apartment residents figure out how to
dispose of common household items. The assistant will provide a
recycling category, preparation instructions, and the source used.

## Dataset

The dataset is stored in `data/recycling_data.csv`.

It contains 200 examples of household items in different conditions.
These are examples created from recycling guidance, not data collected
from residents. Some items appear more than once because their
condition changes the disposal instructions.

The three categories are:
- Recyclable
- Recyclable after preparation
- Not accepted in recycling

“Not accepted in recycling” does not automatically mean an item belongs
in the trash. Some items may need special disposal.

## Sources and Limitations

The main sources are the Town of Normal’s recyclable and
non-recyclable item guides:

- https://www.normalil.gov/482/Recyclable-Items
- https://www.normalil.gov/483/Non-Recyclable-Items

California guidance was also used for comparison during development.
California rules do not determine what is accepted in Normal or
Bloomington, Illinois.

Normal’s guidelines also may not match Bloomington’s rules or SAMI’s
waste collection service. The instructions still need to be checked
against SAMI’s actual recycling requirements.

## Current Progress

The dataset has been added to the repository. The next steps are to
finish checking and cleaning the data, then build a simple prototype.

## Planned Workflow

Resident enters an item and its condition → assistant searches the
dataset → assistant shows the category, instructions, and source.

If there is not enough information, the assistant should ask a
follow-up question or explain that the item needs further checking.

## AI Assistance

AI was used to help create the initial dataset and write this README.
The data still needs review before it is used for real disposal advice.
## Data Cleaning and Checks

I removed the California comparison column from the working dataset
and saved the file as CSV UTF-8.

The dataset has 200 rows and six columns. I checked for missing values
and duplicate item-condition pairs. Neither check found any issues.

Category counts:
- Recyclable: 84
- Recyclable after preparation: 68
- Not accepted in recycling: 48

These checks confirm the dataset's structure. The disposal instructions
still need to be verified against SAMI's waste collection rules.

## Known Limitations

The current prototype only works with items and conditions already
listed in the dataset. Users must select from the available options.
If an item is missing, the program cannot provide disposal instructions
for it.

A future version could let users type a question and search for relevant
guidance. However, it would still need a reliable source before providing
instructions for an unfamiliar item.

## Current Progress

The terminal prototype loads the CSV and lets users select an item
and its condition. It finds the matching row and displays the category,
instructions, source, and verification status.

I tested all three disposal categories and invalid menu entries.
The tested selections returned the expected results, and invalid
entries prompted the user to try again.

This version uses direct CSV lookup. It does not use an AI model
or RAG.

## Running the Prototype

Python 3 is required. No additional packages are needed.

From the project folder, run:

python app.py

Select an item number, then a condition number, to see the guidance.