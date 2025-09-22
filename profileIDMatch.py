import pandas as pd
import re
import numpy as np

# Use pd.read_excel as requested to load the data correctly
memberships_df = pd.read_excel('Assignment_1.xlsx', sheet_name='Memberships')
tokens_df = pd.read_excel('Assignment_1.xlsx', sheet_name='Tokens')
users_df=pd.read_excel('Assignment_1.xlsx', sheet_name='Users')
draftexport_df = pd.read_excel('Assignment_1.xlsx', sheet_name='draftExport')


#converts the credit digits to string so we can remove trialing apostrophes
tokens_df = pd.read_excel('Assignment_1.xlsx',sheet_name='Tokens', dtype={'Last 4 Digits': str})
draftexport_df = pd.read_excel('Assignment_1.xlsx',  sheet_name='draftExport', dtype={'Masked Last 4 Digits': str})

print("Files loaded successfully with correct data types. Beginning transformation...")

        # --- Data Cleaning and Standardization ---

        # The astype(str) is still a good practice, but setting dtype on load is more reliable
tokens_df['Last 4 Digits'] = tokens_df['Last 4 Digits'].str.lstrip("'")
draftexport_df['Masked Last 4 Digits'] = draftexport_df['Masked Last 4 Digits'].str.lstrip("'")
    
"""def standardize_masked_digits(df, column_name):
            #Removes leading apostrophes from the masked credit card numbers.
            # Convert the column to string type to handle mixed data types
            df[column_name] = df[column_name].astype(str)
            # Remove the leading single quote if it exists
            df[column_name] = df[column_name].apply(
                lambda x: x[1:] if isinstance(x, str) and x.startswith("'") else x
            )
            return df """

# Apply standardization to both DataFrames
#tokens_df = standardize_masked_digits(tokens_df, 'Last 4 Digits')
#draftexport_df = standardize_masked_digits(draftexport_df, 'Masked Last 4 Digits')

print(draftexport_df)