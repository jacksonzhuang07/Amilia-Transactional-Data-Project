import pandas as pd

# Define the file path and output file name
file_path = 'Assignment_1.xlsx'
output_file = 'Users_with_Card_Digits.csv'

try:
    # Load the necessary sheets into pandas DataFrames
    users_df = pd.read_excel(file_path, sheet_name='Users')
    draftexport_df = pd.read_excel(file_path, sheet_name='draftExport')

    # --- Step 1: Data cleaning and standardization ---
    # Rename columns in draftexport to match users for easier merging
    draftexport_df = draftexport_df.rename(columns={
        'Primary First Name': 'First Name',
        'Last Name': 'Last Name',
        'House #': 'Group ID',
        'Masked Last 4 Digits': 'Last 4 Digits'
    })

    # Standardize Group ID to integer type to ensure consistent merging
    users_df['Group ID'] = users_df['Group ID'].astype(int)
    draftexport_df['Group ID'] = draftexport_df['Group ID'].astype(int)

    # Combine the name fields into a single key to improve matching accuracy
    users_df['full_name'] = users_df['First Name'] + ' ' + users_df['Last Name']
    draftexport_df['full_name'] = draftexport_df['First Name'] + ' ' + draftexport_df['Last Name']

    # Drop duplicates in draftexport to avoid one-to-many merges
    draftexport_cleaned = draftexport_df.drop_duplicates(subset=['Group ID', 'full_name', 'Last 4 Digits'])

    # --- Step 2: Merge the dataframes ---
    # Perform a left merge on Group ID and full name to add card digits to the Users dataframe
    merged_df = pd.merge(
        users_df,
        draftexport_cleaned[['Group ID', 'full_name', 'Last 4 Digits']],
        on=['Group ID', 'full_name'],
        how='left'
    )

    # --- Step 3: Finalize and save the output ---
    # Drop the temporary 'full_name' column
    final_df = merged_df.drop(columns=['full_name'])

    # Save the updated DataFrame to a new CSV file
    final_df.to_csv(output_file, index=False)

    print(f"\nSuccessfully matched data and saved to '{output_file}'.")
    
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please ensure it is in the same directory.")
except Exception as e:
    print(f"An error occurred: {e}")