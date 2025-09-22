import pandas as pd
import re
import numpy as np

# Use pd.read_excel as requested to load the data correctly
memberships_df = pd.read_excel('Assignment_1.xlsx', sheet_name='Memberships')
tokens_df = pd.read_excel('Assignment_1.xlsx', sheet_name='Tokens', converters={'Last 4 Digits': str})
users_df = pd.read_excel('Assignment_1.xlsx', sheet_name='Users')
draftexport_df = pd.read_excel('Assignment_1.xlsx', sheet_name='draftExport', converters={'Masked Last 4 Digits': str})

def create_Name_Key(full_name):
    """
    Creates a standardized key from a full name string, handling different formats
    while preserving the unique numerical identifiers.
    """
    full_name = str(full_name).strip()
    
    # Check for "Last,First" format
    if ',' in full_name:
        parts = full_name.split(',', 1)
        # Re-order to "First Last" and remove extra spaces
        return f"{parts[1].strip()} {parts[0].strip()}"
    else:
        # Assume "First Last" format
        return full_name.strip()
    
def standardize_masked_digits(df, column_name):
    """Removes leading apostrophes from the masked credit card numbers."""
    # Convert the column to string type to handle mixed data types
    df[column_name] = df[column_name].astype(str)
    # Remove the leading single quote if it exists
    df[column_name] = df[column_name].str.removeprefix("'")
    #print(df[column_name])
    return df

# Apply standardization to both DataFrames
tokens_df = standardize_masked_digits(tokens_df, 'Last 4 Digits')
draftexport_df = standardize_masked_digits(draftexport_df, 'Masked Last 4 Digits')

# --- Transformation for draftExport ---

def decrement_last_digit(masked_str):
    """Subtracts 1 from the last digit of a string, handling edge cases."""
    # Handle non-string or short inputs
    if pd.isna(masked_str) or not isinstance(masked_str, str) or len(masked_str) < 4:
        print("improper format digit cannot be decremented")
        print(isinstance(masked_str, str))
        print(pd.isna(masked_str))
        print(len(masked_str))
        print(masked_str)
        return np.nan
    try:
        # Safely get the last digit and perform the decrement operation
        last_digit = int(masked_str[-1])
        new_last_digit = (last_digit - 1 + 10) % 10  # Ensure result is between 0-9
        # Return the new string with the decremented last digit
        return masked_str[:-1] + str(new_last_digit)
    except (ValueError, IndexError):
        # Return NaN for any conversion or index errors
        return np.nan
            
draftexport_df['Last 4 Digits'] = draftexport_df['Masked Last 4 Digits'].apply(decrement_last_digit)         

# Create a unique matching key in the Memberships DataFrame
memberships_df['Name_Key'] = memberships_df['First Name'].str.strip() + ' ' + memberships_df['Last Name'].str.strip()

draftexport_df['Name_Key'] = draftexport_df['Primary First Name'].str.strip() + ' ' + draftexport_df['Last Name'].str.strip()

draftexport_df['Group ID'] = draftexport_df['House #']

users_df['Name_Key'] = users_df['First Name'].str.strip() + ' ' + memberships_df['Last Name'].str.strip()


tokens_df['Name_Key'] = tokens_df['Name'].apply(create_Name_Key)


with pd.ExcelWriter('Assignment_1_Cleaned.xlsx') as writer:
    # Write the merged DataFrame to the 'Memberships' sheet
    memberships_df.to_excel(writer, sheet_name='Memberships', index=False)
    draftexport_df.to_excel(writer, sheet_name='draftExport', index=False)
    users_df.to_excel(writer, sheet_name='Users', index=False)
    
    # Write the original tokens DataFrame to the 'Tokens' sheet
    # We will remove the temporary 'Name_Key' column for a clean output
    
    tokens_df.to_excel(writer, sheet_name='Tokens', index=False)

# Select the necessary columns from the Tokens DataFrame for the merge
tokens_to_merge = tokens_df[['Last 4 Digits', 'profileid']]
draft_merge = draftexport_df[['Name_Key','Last 4 Digits']]
digits_merge=tokens_df[['Name_Key', 'profileid']]

# --- Check for duplicates in digits_merge by Name_Key ---
print("Number of duplicate Name_Key values in digits_merge:")
print(digits_merge.duplicated(subset='Name_Key').sum())
print("Number of duplicate Name_Key values in memberships_df:")
print(memberships_df.duplicated(subset='Name_Key').sum())

# List the actual duplicate rows
print("\nDuplicate rows in digits_merge by Name_Key:")
print(digits_merge[digits_merge.duplicated(subset='Name_Key', keep=False)])


# Merge the DataFrames based on the match key
# Merge 
print(f"\nNumber of NaN 'Name_Key' values in memberships_df before merge:")
print(memberships_df['Name_Key'].isnull().sum())
print(f"\nNumber of NaN 'Name_Key' values in tokens before merge:")
print(digits_merge['Name_Key'].isnull().sum())


merged_df = pd.merge(
    memberships_df, 
    digits_merge, 
    on='Name_Key',
    how='left'
)

print(len(memberships_df))

print(len(merged_df))

'''print(merged_df)
duplicate_keys = merged_df.duplicated(['Name_Key'], keep=False)
rows_not_in_memberships = merged_df[duplicate_keys]

print("Rows in merged_df that are not in memberships_df:")
print(rows_not_in_memberships)


missing_from_tokens = pd.merge(
    memberships_df,
    merged_df,
    how='outer',
    indicator=True
)
print(missing_from_tokens)

rows_in_tokens_only = missing_from_tokens[missing_from_tokens['_merge'] == 'both']

# Print the rows to see the results
print("Rows that exist only in Tokens:")
print(rows_in_tokens_only)


merged_df = pd.merge(
    merged_df, 
    draft_merge, 
    on='Name_Key',
    how='left'
)


merged_df = pd.merge(
    merged_df, 
    tokens_to_merge, 
    on='Last 4 Digits', 
    how='left'
)'''

# Populate the 'Payment Link Id' column from the 'profileid' and clean up
# Note: You now have `profileid` from the merge.
# You might want to rename it or handle it based on your later needs.

#merged_df['Payment Link Id'] = merged_df['profileid']
merged_df['Payment Link Id'] = merged_df['Payment Link Id'].fillna(merged_df['profileid'])

del merged_df['profileid']
#print(merged_df)

# there are card numbers and lines in draft export that are not present in membersips
# see if they are present in tokens?


# Populate the 'Payment Link Id' column from the 'profileid' and clean up


found_payments = merged_df[merged_df['Payment Link Id'].notnull()]
total_found_revenue = found_payments['Price $'].sum()

# Calculate revenue for rows with an unfound (missing) payment link
unfound_payments = merged_df[merged_df['Payment Link Id'].isnull()]
total_unfound_revenue = unfound_payments['Price $'].sum()

print("\n--- Financial Impact ---")
print(f"Total Revenue from Found Payments: ${total_found_revenue:.2f}")
print(f"Total Revenue from Unfound Payments: ${total_unfound_revenue:.2f}")

1720/3680


# Save both dataframes to a single Excel file with two sheets
# Create a Pandas ExcelWriter object
with pd.ExcelWriter('Assignment_1_Updated_Final.xlsx') as writer:
    # Write the merged DataFrame to the 'Memberships' sheet
    merged_df.to_excel(writer, sheet_name='Memberships', index=False)
    draftexport_df.to_excel(writer, sheet_name='draftExport', index=False)
    users_df.to_excel(writer, sheet_name='Users', index=False)
    
    # Write the original tokens DataFrame to the 'Tokens' sheet
    # We will remove the temporary 'Name_Key' column for a clean output
    
    tokens_df.to_excel(writer, sheet_name='Tokens', index=False)


print("Updated data has been saved to 'Assignment_1_Updated_Final.xlsx'")

# Check the new number of null values
print("Number of null 'Payment Link Id' values after new merge:")
print(merged_df['Payment Link Id'].isnull().sum())
