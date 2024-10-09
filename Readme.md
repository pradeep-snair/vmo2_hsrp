 
Initially I hardcoded the lines to be parsed, i.e. ce1 details are in the lines 5 
and line 9. I then used the logically better 'startswith' method of string object to 
get the o/p of CE1 and CE2 router.
Parsing the dict output to json was slightly tricky as I was not getting the format correct. Test is checking 
only the happy path . I will try to add tests and check for functionality of the script. 

hsrp_ce.txt -> has the router HSRP status
main.py -> is the main file that parses hsrp_ce.txt and outputs the Json file. 

