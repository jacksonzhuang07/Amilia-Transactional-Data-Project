import pandas as pd

# Define the file paths and output file name
users_with_digits_file = 'Users_with_Card_Digits.csv'
tokens_file = 'Assignment_1.xlsx'
output_file = 'Users_with_Payment_Links.csv'

try:
    # Load the DataFrames
    users_df = pd.read_csv(users_with_digits_file)
    tokens_df = pd.read_excel(tokens_file, sheet_name='Tokens')

    # --- Data Cleaning and Standardization ---

    # Create a combined name column for merging
    users_df['full_name'] = users_df['First Name'] + ' ' + users_df['Last Name']

    # --- Merge the DataFrames ---
    
    # Perform a left merge on the combined name and the last 4 digits
    merged_df = pd.merge(
        users_df,
        tokens_df[['Name', 'Last 4 Digits', 'profileid']],
        left_on=['full_name', 'Last 4 Digits'],
        right_on=['Name', 'Last 4 Digits'],
        how='left'
    )

    # --- Finalize the output ---

    # Drop temporary and duplicate columns
    final_df = merged_df.drop(columns=['full_name', 'Name'])
    
    # Rename the 'profileid' column to 'Payment Link Id'
    final_df = final_df.rename(columns={'profileid': 'Payment Link Id'})

    # Save the updated DataFrame to a new CSV file
    final_df.to_csv(output_file, index=False)
    
    print(f"\nSuccessfully matched data and saved to '{output_file}'.")
    
except FileNotFoundError:
    print(f"Error: A required file was not found.")
    print(f"Please ensure '{users_with_digits_file}' and '{tokens_file}' are in the same directory.")
except Exception as e:
    print(f"An error occurred: {e}")