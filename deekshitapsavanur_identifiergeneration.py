# -*- coding: utf-8 -*-
"""DeekshitaPSavanur_IdentifierGeneration.ipynb

Automatically generated by Colab.

"""

# Importing the necessary libraries

import pandas as pd

# Loading the Excel file
xls = pd.ExcelFile('IdentifierList.xlsm')

# Viewing the sheets inside the Excel file_name
xls.sheet_names

# Loading each dataset in different sheets to respective dataframes

dataset1 = pd.read_excel(xls, sheet_name='Data Set 1')
dataset2 = pd.read_excel(xls, sheet_name='Data Set 2')
dataset3 = pd.read_excel(xls, sheet_name='Data Set 3')

"""**NOTE :** Each function is created to handle each of the requirements mentioned."""

# Requirement : HOIDs must start with the Association code.

def add_acode_hoid(df):
    # Convert Association Codes to string value
    df['Association Code'] = df['Association Code'].astype(str)

    # Adding Association codes to HOID rows respectively
    df['HOID'] = df['Association Code'].str[:2]

    return df

# Requirement : Writing a function to accomodate 3 cases shown in Sample Dataset's Commentary

def generate_hoid(df):

    # CASE 1 : If no unit number or lot number is present,
    # and street numbers are all different, further add street number to HOID.

    if df['Unit Number'].isna().all() and df['Lot Number'].isna().all():
        # To check if street numbers are are unique within the same association code
        if df['Street Number'].nunique() == len(df):
            # Adding street number to HOID
            df['HOID'] = df['HOID'] + df['Street Number'].astype(str) # Converting Street numbers to string


    # CASE 2 : If all street numbers and street names are the same,
    # the unit number is further added to HOID.

    elif df['Street Number'].nunique() == 1 or df['Street Name'].nunique() == 1:
        # To check if unit numbers are not null
        if df['Unit Number'].notna().any():
            # Adding unit number to HOID
            df['HOID'] = df['HOID'] + df['Unit Number'].astype(str)

        # To remove duplicates present in 'HOID' column, (for example, dataset 2)
        # a new column 'HOID NEW' is added, which combines Association code, Street Number and Unit Number.

            if df['HOID'].duplicated().sum()>0:
              df['HOID NEW'] = df.apply(lambda row: row['HOID'].replace(str(row['Unit Number']), ''), axis=1)
              df['HOID NEW'] = df['HOID NEW'] + df['Street Number'].astype(str) + df['Unit Number'].astype(str)

    # Case 3: If street number, street name, and lot number are present,
    # the street name is represented by it's initials and lot number's non-alpha numeric characters are removed,
    # further adding street number, street name initials and lot number to HOID.

    elif (df['Street Number'].nunique() == 1 or
          df['Street Name'].nunique() == 1 or
          df['Lot Number'].notna().any()):

        # Creating the initials from Street Name

        initials = ""

        # Iterating through unique street names to create initials
        street_initials_map = {}
        for street_name in df['Street Name'].unique():
            initials = ''.join([word[0].upper() for word in street_name.split() if word])
            street_initials_map[street_name] = initials

        # Adding all the components to HOID based on the previous mapping, row-wise
        for index, row in df.iterrows():
            street_initials = street_initials_map[row['Street Name']]

            # Removing non-alphanumeric characters
            cleaned_lot_number = ''.join(filter(str.isalnum, str(row['Lot Number'])))

            # Generating final HOID
            df.at[index, 'HOID'] += str(row['Street Number']) + street_initials + cleaned_lot_number

            # Requirement : Ensuring HOID length is not greater than 16 characters (considering 12 characters as ideal)
            df['HOID'] = df['HOID'].apply(lambda x: x[:16] if len(x) > 16 else x)

    return df

# Requirement : Ensuring no duplicates are present among HOIDs in all datasets

def count_duplicates(df):

    # Counting the number of duplicates in the 'HOID' column
    duplicates_count = df['HOID'].duplicated().sum()
    print("Number of duplicate HOIDs:", duplicates_count)

# Applying the logic to dataset 1

add_acode_hoid(dataset1)
dataset1_processed = generate_hoid(dataset1)
dataset1_processed
count_duplicates(dataset1)

# Applying the logic to dataset 2

add_acode_hoid(dataset2)
dataset2_processed = generate_hoid(dataset2)
dataset2_processed
count_duplicates(dataset2)

# Validating the duplication issue for Dataset 2

duplicates_count_new = dataset2['HOID NEW'].duplicated().sum()
print("Number of duplicate HOIDs:", duplicates_count_new)

# Applying the logic to dataset 3

add_acode_hoid(dataset3)
dataset3_processed = generate_hoid(dataset3)
dataset3_processed
count_duplicates(dataset3)

# Exporting the Processed Datasets

dataset1_processed.to_excel('Processed_DataSet_1.xlsx', index=False)
dataset2_processed.to_excel('Processed_DataSet_2.xlsx', index=False)
dataset3_processed.to_excel('Processed_DataSet_3.xlsx', index=False)
