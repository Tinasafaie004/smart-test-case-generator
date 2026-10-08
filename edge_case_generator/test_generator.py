from generator import multi_direction_change
import json
import subprocess
from pathlib import Path

plans_path=Path(__file__).resolve().parent/"generated_plans.json"
runner_path = Path(__file__).resolve().parent / "run_solution.js"

# ascending_to_descending_plan = {
#     "start": 4,
#     "first_direction": "up",
#     "lengths": [4, 3],
#     "reason": "Checks a change from ascending to descending"
# }

# descending_to_ascending_plan = {
#     "start": 7,
#     "first_direction": "down",
#     "lengths": [4, 3],
#     "reason": "Checks a change from descending to ascending"
# }

# longest_run_at_end_plan = {
#     "start": 1,
#     "first_direction": "up",
#     "lengths": [6, 3, 7],
#     "reason": "Checks whether the longest run appears at the end"
# }

# longest_run_in_middle_plan = {
#     "start": 10,
#     "first_direction": "down",
#     "lengths": [3,4,3],
#     "reason": "Checks whether the longest run appears in the middle"
# }

# plans=[
#     ascending_to_descending_plan,
#     descending_to_ascending_plan,
#     longest_run_at_end_plan,
#     longest_run_in_middle_plan
# ]

with open(plans_path,"r") as file:
    plans=json.load(file)
#for case, expected_result in zip(cases,expected):   #.zip pairs them
for plan in plans:
    case,expected_result=multi_direction_change(plan["start"], plan["first_direction"],plan["lengths"])    
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
    print("Reason:",plan["reason"])

# print("Input tokens:",tokens["input_tokens"])
# print("Output tokens:",tokens["output_tokens"])
# print("Total tokens:",tokens["total_tokens"])