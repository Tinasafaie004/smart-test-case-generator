from openai import OpenAI
from pydantic import BaseModel
from typing import Literal
from generator import multi_direction_change

class TestPlan(BaseModel):
    start:int
    first_direction:Literal["up","down"]
    lengths:list[int]
    reason:str

client= OpenAI()

response= client.responses.parse(
    model="gpt-6-luna",
    input="""
    Generate one test plan for my multi_direction_change function.

    The function receives:
    - start: the first integer
    - first_direction: either "up" or "down"
    - lengths: the lengths of consecutive runs

    Directions alternate automatically after every run.

    Requirements:
    - Include between 2 and 5 runs.
    - Every run length must be between 2 and 8.
    - Make one run uniquely longer than the others.
    - The reason must describe the test pattern represented by these exact fields.
    - Do not invent or include a separate array.
    - Do not provide the expected answer.
    """,
    text_format=TestPlan,
    reasoning={"effort":"none"},
    max_output_tokens=300
)

plan=response.output_parsed
case,expected_result = multi_direction_change(
    plan.start,
    plan.first_direction,
    plan.lengths
)
print("Plan:", plan)
print("Generated test array:",case)
print("Expected longest length:", max(plan.lengths))
print("Expected longest run:",expected_result)
print("Input tokens:", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)
print("Total tokens:", response.usage.total_tokens)