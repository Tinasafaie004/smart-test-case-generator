# Longest Consecutive Series — AI Edge Case Generator

A JavaScript practice problem that turned into my first DIY AI project.

After several attempts at finding the longest consecutive series, I started wondering: **what if my solution still has a bug I haven't thought to test?** So I built a Python tool that uses AI to suggest test patterns, generates the actual arrays and expected results locally, and checks my JavaScript solution.

## The problem

Find the longest **contiguous** run of integers that increases or decreases by exactly `1` at each step. Return the run itself. When two runs have the same maximum length, the first one wins.

```text
Input:    [10, 11, 12, 11, 10, 9, 8, 7, 6, 5, 6]
Expected: [12, 11, 10, 9, 8, 7, 6, 5]
```

The array stays in its original order. A change in direction starts another run, and the turning point belongs to both neighboring runs.

## How it works

1. **Suggest patterns:** `ai_plan_generator.py` requests four structured test plans: longest run first, in the middle, at the end, and a tie where the first run should win.
2. **Build cases locally:** `generator.py` converts each plan into an input array and its expected longest run. The AI supplies the pattern and explanation; Python calculates the expected answer.
3. **Save the cases:** Plans, arrays, and expected results are written to `generated_plans.json`.
4. **Check the solution:** `test_generator.py` starts a Node.js runner for each saved case and compares the JavaScript result with the expected array.

Generating plans and running tests are separate steps, so I can debug against the same cases without making another API request each time.

## Project structure

```text
longest_consecuttive_series/
├── README.md
├── solution.js                     # JavaScript solution under test
└── edge_case_generator/
    ├── ai_plan_generator.py         # Requests structured plans and saves cases
    ├── generator.py                 # Builds ascending, descending, and alternating runs
    ├── generated_plans.json         # Saved plans, inputs, and expected outputs
    ├── run_solution.js              # Calls the solution with a JSON command-line input
    └── test_generator.py            # Compares actual and expected outputs
```

## Run the saved tests

You need **Python 3.10 or newer** and **Node.js**, with `python` and `node` available in your terminal. The saved tests use only Python's standard library and do not need an API key or third-party Python packages.

From the project directory (`longest_consecuttive_series`), run:

```powershell
python edge_case_generator/test_generator.py
```

Each case prints `PASS` or `FAIL`, the pattern being tested, and the expected and actual arrays. The four checked-in cases currently pass.

To try a single input directly:

```powershell
node edge_case_generator/run_solution.js '[1,2,3,4]'
```

Expected output:

```json
[1,2,3,4]
```

## Generate new AI test plans

Install the additional dependencies in a virtual environment. These commands use PowerShell and run from the project directory:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install openai pydantic
$env:OPENAI_API_KEY = "your-api-key"
.venv\Scripts\python.exe edge_case_generator/ai_plan_generator.py
```

Keep your API key out of source files and version control.

The script makes an OpenAI API request using the model configured in `ai_plan_generator.py` (currently `gpt-6-luna`). You need API access to that model; requests may incur charges. The script prints token usage and **overwrites** `edge_case_generator/generated_plans.json` with the new cases.

Then check the newly saved cases:

```powershell
.venv\Scripts\python.exe edge_case_generator/test_generator.py
```

## Test plan format

Each saved entry contains the pattern, an explanation, and the locally generated input and expected answer:

```json
{
  "start": 1,
  "first_direction": "up",
  "lengths": [3, 4],
  "reason": "The second run is longer and changes direction from up to down.",
  "case": [1, 2, 3, 2, 1, 0],
  "expected": [3, 2, 1, 0]
}
```

- `start`: the first integer in the array.
- `first_direction`: `"up"` or `"down"`; subsequent runs alternate direction automatically.
- `lengths`: the number of elements in each run, including the shared turning point. The prompt requests 2–5 runs, each with a length of 2–8.
- `reason`: the AI's explanation of the test pattern.
- `case` and `expected`: values calculated by Python before saving.

For runs with lengths `[3, 4]`, the final array has six elements because the runs share one turning point.

## Current scope and limitations

This is a learning project focused on direction changes and the position of the longest run. Passing the saved cases does not prove the solution is correct for every input.

- Generated arrays contain consecutive steps and alternating directions. They do not currently cover empty arrays, single-element arrays, duplicates, gaps, or invalid inputs.
- The current JavaScript implementation returns `[]` when it finds no consecutive pair, including for empty and single-element inputs.
- Pydantic checks the plan's field types and direction values. The requested run counts and length bounds are prompt instructions, not explicit schema constraints.
- The test script prints mismatches as `FAIL` but does not set a failing process exit code for them. It is currently a manual debugging tool.
- Expected answers come from the Python generator, which also needs to be correct.

## Possible next steps

- Add hand-written cases for gaps, duplicates, empty arrays, and single-element arrays.
- Validate run counts and lengths before generating arrays.
- Compare results against an independent reference implementation.
- Make test failures return a nonzero exit code for automated checks.
- Save failing cases as regression tests when a bug is found.
