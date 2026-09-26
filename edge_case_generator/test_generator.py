from generator import direction_change, multi_direction_change
import json
import subprocess
from pathlib import Path

runner_path = Path(__file__).resolve().parent / "run_solution.js"

lengths=[
    [6,3,7],
    [3,4,3]
]

cases=[
    direction_change(4,4,3,"up"),  
    direction_change(7,4,3,"down"),
    multi_direction_change(1,"up",lengths[0]),
    multi_direction_change(10,"down", lengths[1])
]

expected=[
    # [4,5,6,7],
    # [7,6,5,4],
    # [4,5,6,7,8,9,10],
    # [8,9,10,11]

    #to make this pattern easier: --> I'm gonna return the length of the longest  series 
    4,4,7,4
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
