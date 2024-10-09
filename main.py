from typing import TextIO
import json


def parse_hsrp_state(hsrp_status_file: TextIO) -> str:
    """ Function will take an open file as argument and return the parsed string
     that can be dumped to json format
     Function will check for Group1 HSRP status and will set Group 1 status to Fail if not active
     Group2 status will be set to Pass if it is active """

    hsrp_status = {"CE1": {}, "CE2": {}}
    current_device = None
    lines = hsrp_status_file.readlines()

    """ Assumptions, router name will be CE1/2 and interfaces are Gig Ethernet 
    Initially I hardcoded the lines to be 
    parsed, i.e. ce1 details are in the lines 5 and line 9 . As this was error prone I switched to the 
    startswith method of string object to get the o/p of CE1 and CE2."""

    for line in lines:
        if line.startswith("CE1"):
            current_device = "CE1"
        elif line.startswith("CE2"):
            current_device = "CE2"
        elif line.startswith("Gi"):
            parts = line.split()
            hsrp_group = f"Group {parts[1]}"
            hsrp_state = parts[4]
            hsrp_status[current_device][hsrp_group] = hsrp_state

    # print(f"OP before JSON parsing is {hsrp_status}")
    """OP before JSON parsing is {'CE1': {'Group 1': 'NotActive', 'Group 2': 'Standby'},
     'CE2': {'Group 1': 'Standby', 'Group 2': 'Active'}}"""
    # Generate  JSON formatted output , hsrp_result is the json key for a list value.
    hsrp_result = {"hsrp_result": []}
    """ Loop through the dict key & values to check for CE1 status. If CE1 goes down for any reason in o/p  
        CE1 group1 status will be set to Fail and CE2 group1 status will be set to Fail- No Longer Standby """

    for ce, groups in hsrp_status.items():
        ce_result = {ce: []}
        for hsrp_group, hsrp_state in groups.items():
            if hsrp_group == "Group 1" and hsrp_state != "Active":
                ce_result[ce].append({
                    "hsrp_group": hsrp_group,
                    "status": "Fail - No Longer Active" if ce == "CE1" else "Fail - No Longer Standby"
                })

            else:
                ce_result[ce].append({
                    "hsrp_group": hsrp_group,
                    "status": "Pass"
                })
        hsrp_result["hsrp_result"].append(ce_result)

    return hsrp_result


with open('hsrp_ce.txt', 'r') as file:
    result = parse_hsrp_state(file)
    print(json.dumps(result, indent=4))
