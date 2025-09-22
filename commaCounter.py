import pandas as pd

# Use pd.read_excel as it works for you
try:
    tokens_df = pd.read_excel('Assignment_1.xlsx', sheet_name='Tokens')

    # Count the number of rows in the 'Name' column that contain a comma
    last_name_first_name_count = tokens_df['Name'].str.contains(',', na=False).sum()
    first_name_last_name_count = tokens_df['Name'].str.contains(' ', na=False).sum()

    print(f"Number of rows with 'LastName,FirstName' format: {last_name_first_name_count}")
    print(f"Number of rows with 'LastName,FirstName' format: {first_name_last_name_count}")
    print(f"Number of rows with 'LastName,FirstName' format: {first_name_last_name_count+last_name_first_name_count}")


except FileNotFoundError:
    print("Error: The file was not found. Please ensure 'Assignment_1.xlsx' is in the same directory as your script.")