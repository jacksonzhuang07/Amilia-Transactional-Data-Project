
Assignment 2 - Micro Household Grouping Solution

Approach:
1.  Data Normalization: Cleaned and standardized address and email data using string manipulation and regex.
2.  Grouping Logic: Employed a Union-Find algorithm to correctly group people into households. This approach iteratively merges groups based on two rules: shared normalized addresses and guardian-child relationships.
3.  GroupID Assignment: Assigned a deterministic GroupID to each household, using the format G-<min PersonId in group>.
4.  Account Owner Selection: Calculated each person's age and applied a strict priority system to select a single owner per group. The smallest PersonId was used as a tie-breaker, ensuring a stable output.

Instructions:
To reproduce the results, place this script in the same directory as 'people.csv' and run it using a Python interpreter. The script will generate 'groups_out.csv', 'owners_out.csv', and this 'README.txt' file.
