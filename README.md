# Maintenance_Work_Order_Processing_Pipeline_Public

A repository for the maintenance work order processing pipeline (PUBLIC)

IMPORTANT!
THIS REPOSITORY REPRESENTS A MOMENT IN TIME (FEB 2020) AND WILL NOT BE CHANGED. Additional work has been planned for this pipeline and will be published at a later date.

The NLP pipeline takes raw maintenance work orders, and tags then according to their symptom/state, maintenance activity and maintenance item. These three stages are downstream dependant and must be run in the correct order. The correct order of execution is shown in the src/run.py file.

To run this code, you will need to use Python 3 and have the following packages installed:
- pandas
- pattern
- nltk
- gensim
- fuzzywuzzy
- pyspellchecker
- xlrd
- openpyxl

To execute this code, you will need to create a data/static folder and a data/fluid folder. In the data/static folder you will need three files, these are:
- wo-large.xlsx: A file containing a list of work orders in a column named "ShortText".
- maintenance-activity-dict.xlsx: A file containing a list of maintenance activity terms in a column named "words".
- maintenance-item-dict.xlsx: A file containing a list of maintenance item terms in a column named "words".

To run the full pipeline on windows, run the "run.py" script. On OSX, use the "run_osx.py" script.

After running the pipeline, the final output will be stored in a file named data/fluid/output-maintenance-item.xlsx.


