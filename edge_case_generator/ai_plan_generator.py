from openai import OpenAI
from pydantic import BaseModel
from typing import Literal
import json
from pathlib import Path

class TestPlan(BaseModel):
    start:int
    first_direction:Literal["up","down"]
    lengths:list[int]
    reason:str

class TestPlanBatch(BaseModel):
    plans:list[TestPlan]

client= OpenAI()
plans_path=Path(__file__).resolve().parent/"generated_plans.json"

def generate_plans():
    response= client.responses.parse(
        model="gpt-6-luna",
        input="""
        Generate four different test plans for my multi_direction_change function.
        Include:
        -one where the longest run is first
        -one where the longest run is in the middle
        -one where the longest run is last
        -one where two runs tie for longest, to check the first wins

        The function receives:
        - start: the first integer
        - first_direction: either "up" or "down"
        - lengths: the lengths of consecutive runs

        Directions alternate automatically after every run.

        Requirements:
        - Include between 2 and 5 runs.
        - Every run length must be between 2 and 8.
        - The reason must describe the test pattern represented by these exact fields.
        - Do not invent or include a separate array.
        - Do not provide the expected answer.
        """,
        text_format=TestPlanBatch,
        reasoning={"effort":"none"},
        max_output_tokens=900   #looked at the total for one --> times 4
    )

    # for plan in plans:
    #     case,expected_result = multi_direction_change(
    #         plan.start,
    #         plan.first_direction,
    #         plan.lengths
    #     )
    #     print("Plan:", plan)
    #     print("Generated test array:",case)
    #     print("Expected longest length:", max(plan.lengths))
    #     print("Expected longest run:",expected_result)
    #     print("Input tokens:", response.usage.input_tokens)
    #     print("Output tokens:", response.usage.output_tokens)
    #     print("Total tokens:", response.usage.total_tokens)
    tokens={
        "input_tokens":response.usage.input_tokens,
        "output_tokens":response.usage.output_tokens,
        "total_tokens":response.usage.total_tokens
    }
    plan_batch=response.output_parsed
    return plan_batch.plans, tokens

def save_plans(plans):
    plan_dictionaries=[]

    for plan in plans:
        plan_dictionaries.append(plan.model_dump()) #turns TestPlan object as python dictionary

    with open(plans_path,"w") as file:
        json.dump(plan_dictionaries,file,indent=2) #turns python data inot file

if __name__=="__main__":   
    #generate_plan is run once this file is run directly
    #  NOT when it's imported through test_generator
    #  --> so our ai is run once and it avoid using too may token when debugging
    plans,tokens=generate_plans()
    save_plans(plans)

    print("Saved", len(plans),"plans")
    print("Token usage:",tokens)