analysis of assignmeent file

seems uers is matching to memberships on shared group memberships

tokens is using 2 naming conventions

will involve parsing and matching logic for both

matching using one gives limited payment link id discovery

trying with both now

Number of rows with 'LastName,FirstName' format: 473
Number of rows with 'LastName,FirstName' format: 2980
Number of rows with 'LastName,FirstName' format: 3453

numbers of rows with #VALUE = 4


so groups with house id matches
4 digits in draft export and tokens match

must match draft export to users using group and house with credit card number

subtract 1 from it as it is masked

match this with tokens using the last name first name logic


create a function that creates match key first name last name for tokens and membership

creating a payment link id in memberships

match group with house id and add card number  to users from draft exports, -1 to unmask

add both group number and dhousde id to memberships correspondong to first name last name

then match payment id based on visa, first name last



match draft export first namd last name to membership and add house and digits 


match tokens first namd last name digits to membership and add payment link id

first name last name is combined and shown in various formats that need to be cleaned in tokens

first name last name need to be combined in membersehip and draft exports

aformentioned masked digits need to be unmasked and both last 4 digits in draft exports and tokens both need
to be standardized as some have a leading apostrophe