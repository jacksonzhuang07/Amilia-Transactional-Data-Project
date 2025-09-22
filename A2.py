import pandas as pd
import re
from datetime import datetime

# Load the data
df = pd.read_csv('people.csv')

# --- Data Normalization Functions ---

# Requirement 1a & 1b: Trim spaces and standardize 'Street/St./St' to one form
def normalize_address(address):
    """Trims spaces and standardizes 'Street/St./St' to 'Street'."""
    if not isinstance(address, str):
        return None
    address = address.strip()
    # Use a more robust regex to handle variations like "St." or "St" with or without a trailing period
    address = re.sub(r'\b(?:street|st)\.?', 'Street', address, flags=re.IGNORECASE)
    return address


# Requirement 2a: Normalize email by removing any '+tag'
def normalize_email(email):
    """Normalizes emails by lowercasing, trimming spaces, and removing '+tag'."""
    if not isinstance(email, str):
        return None
    email = email.strip().lower()
    # Remove the "+tag" part from the email, e.g., 'alex+kids@' -> 'alex@'
    email = re.sub(r'\+.*?(?=@)', '', email)
    return email

# Apply normalization to the DataFrame
df['Address1_normalized'] = df['Address1'].apply(normalize_address)
# Requirement 1b: Uppercase City
df['City_normalized'] = df['City'].str.upper().str.strip()
# Requirement 1c: Treat Zip as text
df['Zip'] = df['Zip'].astype(str).str.strip()
df['Email_normalized'] = df['Email'].apply(normalize_email)
df['GuardianEmail_normalized'] = df['GuardianEmail'].apply(normalize_email)

# Create a combined address key for initial grouping (Requirement 1b)
df['AddressKey'] = df['Address1_normalized'].astype(str) + df['City_normalized'].astype(str) + df['State'].astype(str) + df['Zip'].astype(str)



# --- Grouping Logic (Union-Find Algorithm) ---

# This algorithm is used to create groups without explicit graphs or fuzzy matching.
parent = {pid: pid for pid in df['PersonId']} #creates dictionary which links pid to pid

def find(item):
    """Finds the root of the group for a given item, with path compression."""
    if item not in parent:
        return None
    if parent[item] == item:
        return item
    parent[item] = find(parent[item])
    return parent[item]

def union(item1, item2):
    """Merges two groups by updating the parent pointers."""
    root1 = find(item1)
    root2 = find(item2)
    if root1 is None or root2 is None:
        return
    if root1 != root2:
        # Merge the two groups by making the smaller PersonId the parent for deterministic GroupID
        parent[root2] = min(root1, root2)

# Requirement 1: Same normalized address ⇒ same group
# This is the first main grouping step. It iterates through people with the same normalized address and merges their groups.
for _, group in df.groupby('AddressKey'):  #groups by address key and iterates through group not _ which is the address key aka the first value in the tuples made by groupby
    # Iterate over each group of people who share the same normalized address.
    if len(group) > 1:
        # Check if the group contains more than one person. If so, they belong in the same household.
        group_person_ids = group['PersonId'].tolist() #adds PersonID column of groups to list
        # Get a list of the PersonIds within the current address group.
        for i in range(1, len(group_person_ids)):
            # Iterate through the rest of the people in the group, starting from the second person.
            union(group_person_ids[0], group_person_ids[i])
            # Merge the group of the first person (anchor) with the group of the current person.

# Requirement 2: GuardianEmail ⇒ child links to guardian’s household
email_to_person = df.set_index('Email_normalized')['PersonId'].to_dict()
#creates normalized email : person id dictinoary

for _, row in df.iterrows():
    guardian_email = row['GuardianEmail_normalized']
    if pd.notna(guardian_email) and guardian_email in email_to_person:
        child_id = row['PersonId']
        guardian_id = email_to_person[guardian_email]
        union(child_id, guardian_id) #joins child to parents club

# Assign the final GroupID based on the min PersonId in each group
# review stopped here
final_groups = {}
for pid in df['PersonId']:
    root = find(pid) #finds group id
    if root not in final_groups:
        final_groups[root] = []
    final_groups[root].append(pid) #if root isn't in final groups then adds group id and adds pid ot that group

groups_list = []
for root, pids in final_groups.items(): #so final_group.items() has one root : list of pids
    min_pid = min(pids)
    for pid in pids:
        groups_list.append({'PersonId': pid, 'GroupID': f'G-{min_pid}'})

groups_df = pd.DataFrame(groups_list).sort_values('PersonId')
groups_df.to_csv('groups_out.csv', index=False)
print("File 'groups_out.csv' has been generated.")

# --- Account Owner Selection ---

# Calculate age using the provided date
today = datetime(2025, 9, 11)
print(df['DOB'])
df['DOB'] = pd.to_datetime(df['DOB'])
df['DOBtest'] = pd.to_datetime(df['DOB'])
df['Age'] = (today - df['DOB']).dt.days / 365.25

print(pd.to_datetime('8/23/1993'))
# Merge with final GroupID
df = pd.merge(df, groups_df, on='PersonId')

df.to_csv('df.csv', index=False)

# Create a priority score for owner selection
df['HasEmail'] = df['Email_normalized'].notna()
df['IsOver18'] = df['Age'] >= 18
df['PriorityScore'] = 0
df.loc[df['IsOver18'] & df['HasEmail'], 'PriorityScore'] = 3  # Priority 1: Over 18 with email set to Priority 3
df.loc[df['IsOver18'] & ~df['HasEmail'], 'PriorityScore'] = 2 # Priority 2: Over 18 without email 
df.loc[~df['IsOver18'], 'PriorityScore'] = 1                 # Priority 3: Under 18

# Sort by GroupID, then by priority (desc), then by PersonId (asc) for tie-breaking
df_sorted = df.sort_values(by=['GroupID', 'PriorityScore', 'PersonId'], ascending=[True, False, True])
# tie breaker

# Select the first person from each group
owners_df = df_sorted.drop_duplicates(subset='GroupID', keep='first')
owners_df = owners_df[['GroupID', 'PersonId']].rename(columns={'PersonId': 'OwnerPersonId'})
owners_df.to_csv('owners_out.csv', index=False)
print("File 'owners_out.csv' has been generated.")

# --- Create README.txt ---

readme_content = """
Assignment 2 - Micro Household Grouping Solution

Approach:
1.  Data Normalization: Cleaned and standardized address and email data using string manipulation and regex.
2.  Grouping Logic: Employed a Union-Find algorithm to correctly group people into households. This approach iteratively merges groups based on two rules: shared normalized addresses and guardian-child relationships.
3.  GroupID Assignment: Assigned a deterministic GroupID to each household, using the format G-<min PersonId in group>.
4.  Account Owner Selection: Calculated each person's age and applied a strict priority system to select a single owner per group. The smallest PersonId was used as a tie-breaker, ensuring a stable output.

Instructions:
To reproduce the results, place this script in the same directory as 'people.csv' and run it using a Python interpreter. The script will generate 'groups_out.csv', 'owners_out.csv', and this 'README.txt' file.
"""

with open('README.txt', 'w') as f:
    f.write(readme_content)
print("File 'README.txt' has been generated.")