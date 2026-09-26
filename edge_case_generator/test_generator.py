from generator import direction_change, multi_direction_change
import json
import subprocess
from pathlib import Path

runner_path = Path(__file__).resolve().parent / "run_solution.js"

ascending_to_descending_plan = {
    "start": 4,
    "first_direction": "up",
    "lengths": [4, 3],
    "reason": "Checks a change from ascending to descending"
}

descending_to_ascending_plan = {
    "start": 7,
    "first_direction": "down",
    "lengths": [4, 3],
    "reason": "Checks a change from descending to ascending"
}

longest_run_at_end_plan = {
    "start": 1,
    "first_direction": "up",
    "lengths": [6, 3, 7],
    "reason": "Checks whether the longest run appears at the end"
}

longest_run_in_middle_plan = {
    "start": 10,
    "first_direction": "down",
    "lengths": [3,4,3],
    "reason": "Checks whether the longest run appears in the middle"
}

cases=[
    direction_change(ascending_to_descending_plan["start"], ascending_to_descending_plan["lengths"][0], ascending_to_descending_plan["lengths"][1], ascending_to_descending_plan["first_direction"]),
    direction_change(descending_to_ascending_plan["start"], descending_to_ascending_plan["lengths"][0], descending_to_ascending_plan["lengths"][1], descending_to_ascending_plan["first_direction"]),
    multi_direction_change(longest_run_at_end_plan["start"], longest_run_at_end_plan["first_direction"], longest_run_at_end_plan["lengths"]),
    multi_direction_change(longest_run_in_middle_plan["start"], longest_run_in_middle_plan["first_direction"], longest_run_in_middle_plan["lengths"])
]

expected=[
    # [4,5,6,7],
    # [7,6,5,4],
    # [4,5,6,7,8,9,10],
    # [8,9,10,11]

    #to make this pattern easier: --> I'm gonna return the length of the longest  series 
    max(ascending_to_descending_plan["lengths"]),
    max(descending_to_ascending_plan["lengths"]),
    max(longest_run_at_end_plan["lengths"]),
    max(longest_run_in_middle_plan["lengths"])
]

for case, expected_result in zip(cases,expected):   #.zip pairs them
    case_as_text=json.dumps(case)  #turns a python array into text

    result=subprocess.run(
        ["node", str(runner_path), case_as_text],   #we have to pass the test case as TEXT since it's a COMMNAD LINE ARG
        capture_output=True, #captures the output as stdout
        text=True,  #makes it text instead of bytes
        check=True  #raises errors instead of continuing 
    )
    actual=json.loads(result.stdout) #this converts the console.log from run_solution back to python array
    if(actual==expected_result):
        print("PASS", case)
    else:
        print("FAIL", case) #puts space between them by deafult
    print("Expected:", expected_result)
    print("Actual:", actual)    
