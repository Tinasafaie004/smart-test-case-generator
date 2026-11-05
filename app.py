"""Live demo: check the JavaScript solution against AI-planned and hand-built cases.

Run locally with:  streamlit run app.py
"""

import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
GENERATOR_DIR = ROOT / "edge_case_generator"
PLANS_PATH = GENERATOR_DIR / "generated_plans.json"
RUNNER_PATH = GENERATOR_DIR / "run_solution.js"
SOLUTION_PATH = ROOT / "solution.js"

sys.path.insert(0, str(GENERATOR_DIR))
from generator import multi_direction_change  # noqa: E402

MAX_LENGTH = 200  # keeps a pasted array small enough to run quickly
MAX_STEP_LENGTH = 30  # the step-through stays readable up to this many numbers

# The four branches of the loop in solution.js, shown when that branch runs.
BRANCHES = {
    "gap": (
        "Not a step of 1, so there is no run here. Start over.",
        "if(diff!==-1 && diff!==1){\n    current_sequence=[]\n    direction=0;\n}",
    ),
    "start": (
        "A step of 1 after a reset: start a new run with both numbers and remember its direction.",
        "else if(direction===0){\n    current_sequence.push(a[i]);\n    current_sequence.push(a[i+1]);\n    direction=diff;\n}",
    ),
    "extend": (
        "Same direction as before: the run keeps going, so add the next number.",
        "else if(direction===diff){\n    current_sequence.push(a[i+1]);\n}",
    ),
    "turn": (
        "The direction flipped. The turning point starts the next run, so keep only it.",
        "else{  //direction has changed\n    current_sequence=[a[i]]\n    direction=0;\n}",
    ),
}

EXAMPLES = {
    "Up, then a long way down": [10, 11, 12, 11, 10, 9, 8, 7, 6, 5, 6],
    "A gap breaks the run": [4, 5, 6, 7, 2, 3],
    "Two runs tie (first wins)": [1, 2, 3, 2, 1, 2, 3],
    "No run at all": [1, 5, 10, 4],
}


def run_solution(case):
    """Run solution.js on one array through Node and return its result."""
    result = subprocess.run(
        ["node", str(RUNNER_PATH), json.dumps(case)],
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    return json.loads(result.stdout)


def trace_solution(a):
    """Replay solution.js in Python, one loop step at a time, so each step can be shown."""
    longest, current, direction = [], [], 0
    steps = []
    for i in range(len(a) - 1):
        diff = a[i] - a[i + 1]
        if diff not in (1, -1):
            current, direction, branch = [], 0, "gap"
        elif direction == 0:
            current = current + [a[i], a[i + 1]]
            direction, branch = diff, "start"
        elif direction == diff:
            current = current + [a[i + 1]]
            branch = "extend"
        else:
            current, direction, branch = [a[i]], 0, "turn"
        new_longest = len(current) > len(longest)
        if new_longest:
            longest = list(current)
        steps.append(
            {
                "i": i,
                "diff": diff,
                "direction": direction,
                "branch": branch,
                "current": list(current),
                "longest": list(longest),
                "new_longest": new_longest,
            }
        )
    return steps, longest


def array_chips(a, i):
    """The array as a row of boxes, with the pair being compared outlined."""
    chips = []
    for index, value in enumerate(a):
        in_pair = index in (i, i + 1)
        style = (
            "display:inline-block;min-width:2.6rem;padding:0.35rem 0.5rem;margin:0.15rem;"
            "text-align:center;border-radius:0.4rem;font-family:monospace;font-size:1.05rem;"
            + ("border:2px solid #ff4b4b;background:rgba(255,75,75,0.12);" if in_pair
               else "border:1px solid rgba(250,250,250,0.25);")
        )
        label = f"<div style='font-size:0.7rem;opacity:0.6'>a[{index}]</div>"
        chips.append(f"<span style='{style}'>{label}{html.escape(str(value))}</span>")
    return "<div>" + "".join(chips) + "</div>"


def direction_word(direction):
    return {0: "0 (no run yet)", -1: "-1 (going up)", 1: "1 (going down)"}[direction]


def show_result(case, expected, actual):
    if actual == expected:
        st.success("PASS: the solution found the expected run.")
    else:
        st.error("FAIL: the solution returned a different run.")
    col_in, col_exp, col_act = st.columns(3)
    col_in.caption("Input")
    col_in.code(json.dumps(case), language="json")
    col_exp.caption("Expected")
    col_exp.code(json.dumps(expected), language="json")
    col_act.caption("Actual")
    col_act.code(json.dumps(actual), language="json")


st.set_page_config(page_title="Smart Test Case Generator", layout="wide")

st.title("Smart Test Case Generator")
st.write(
    "A JavaScript function finds the longest stretch of numbers that goes up or down by exactly 1 "
    "at each step. For `[10, 11, 12, 11, 10, 9]` that is `[12, 11, 10, 9]`. "
    "AI suggests tricky test patterns, Python builds the arrays and the right answers, "
    "and this page runs my real JavaScript code against them."
)

if shutil.which("node") is None:
    st.error("Node.js is not available on this server, so the JavaScript solution cannot run.")
    st.stop()

tab_how, tab_saved, tab_build, tab_try = st.tabs(
    ["How the solution works", "AI test plans", "Build your own case", "Try any array"]
)

# --- 0. How the solution works -------------------------------------------------
with tab_how:
    col_code, col_idea = st.columns([3, 2], gap="large")

    with col_idea:
        st.subheader("The idea")
        st.markdown(
            """
Walk through the array **one pair of neighbours at a time** and keep two lists:

- **current run**: the stretch I am building right now
- **longest run**: the best one seen so far

For each pair, `diff = a[i] - a[i+1]`:

- `diff` is **-1** when the numbers go **up** by 1, **1** when they go **down** by 1
- anything else is a **gap**, so the current run ends

`direction` remembers which way the current run is moving. If the next step goes the
same way, the run grows. If it flips, the turning point starts a new run.
After every step, if the current run is longer than the longest, it becomes the longest.
Because the check is `>` and not `>=`, **the first run wins a tie**.
"""
        )

    with col_code:
        st.subheader("solution.js")
        st.code(SOLUTION_PATH.read_text(), language="javascript", line_numbers=True)

    st.divider()
    st.subheader("Step through it")
    st.write("Pick an example, or type your own, then move the slider to run the loop one step at a time.")

    col_pick, col_own = st.columns(2)
    example_name = col_pick.selectbox("Example", list(EXAMPLES) + ["My own array"])
    if example_name == "My own array":
        own = col_own.text_input("Your array", value="[3, 4, 5, 4, 3, 2, 1]")
        try:
            array = json.loads(own)
            ok = (
                isinstance(array, list)
                and 2 <= len(array) <= MAX_STEP_LENGTH
                and all(isinstance(n, int) and not isinstance(n, bool) for n in array)
            )
        except json.JSONDecodeError:
            ok = False
        if not ok:
            st.warning(f"Enter a JSON array of 2 to {MAX_STEP_LENGTH} whole numbers, like [3, 4, 5, 4].")
            array = None
    else:
        array = EXAMPLES[example_name]
        col_own.code(json.dumps(array), language="json")

    if array is not None:
        steps, traced = trace_solution(array)
        step_number = st.slider("Loop step", 1, len(steps), 1, key=f"step-{json.dumps(array)}")
        step = steps[step_number - 1]
        i = step["i"]

        st.markdown(array_chips(array, i), unsafe_allow_html=True)

        col_now, col_branch = st.columns(2, gap="large")
        with col_now:
            st.markdown(
                f"**i = {i}**: comparing `a[{i}] = {array[i]}` with `a[{i + 1}] = {array[i + 1]}`"
            )
            st.markdown(f"`diff = {array[i]} - {array[i + 1]} = {step['diff']}`")
            st.markdown(f"`direction` is now {direction_word(step['direction'])}")
            st.markdown(f"**current run:** `{json.dumps(step['current'])}`")
            longest_note = "  (new longest)" if step["new_longest"] else ""
            st.markdown(f"**longest run:** `{json.dumps(step['longest'])}`{longest_note}")
        with col_branch:
            why, snippet = BRANCHES[step["branch"]]
            st.markdown(f"**What happened:** {why}")
            st.code(snippet, language="javascript")

        if step_number == len(steps):
            actual = run_solution(array)
            st.success(f"Done. The function returns `{json.dumps(actual)}`.")
            if actual != traced:
                st.error("The step-through and the real solution.js disagree on this input.")

# --- 1. The saved AI plans ---------------------------------------------------
with tab_saved:
    st.write(
        "Four plans the AI suggested: the longest run first, in the middle, at the end, "
        "and a tie where the first run should win. They are saved, so this page makes no API calls."
    )
    plans = json.loads(PLANS_PATH.read_text())
    if st.button("Run the saved tests", type="primary"):
        passed = 0
        for number, plan in enumerate(plans, start=1):
            actual = run_solution(plan["case"])
            passed += actual == plan["expected"]
            with st.container(border=True):
                st.markdown(f"**Plan {number}:** {plan['reason']}")
                st.caption(
                    f"Start {plan['start']}, first direction {plan['first_direction']}, "
                    f"run lengths {plan['lengths']}"
                )
                show_result(plan["case"], plan["expected"], actual)
        st.metric("Passed", f"{passed} of {len(plans)}")

# --- 2. Build a case from a plan ---------------------------------------------
with tab_build:
    st.write(
        "Describe a pattern the way the AI does: a starting number, a first direction and the "
        "length of each run. Directions alternate after every run."
    )
    col_start, col_dir = st.columns(2)
    start = col_start.number_input("Start", value=10, step=1, min_value=-1000, max_value=1000)
    first_direction = col_dir.radio("First direction", ["up", "down"], horizontal=True)
    lengths_text = st.text_input(
        "Run lengths, separated by commas (each from 2 to 20)",
        value="3, 8, 2",
        help="Each run includes the turning point it shares with the next run.",
    )

    try:
        lengths = [int(part) for part in lengths_text.split(",") if part.strip()]
        if not 1 <= len(lengths) <= 10 or any(not 2 <= n <= 20 for n in lengths):
            raise ValueError
    except ValueError:
        st.warning("Enter 1 to 10 whole numbers, each from 2 to 20, for example 3, 8, 2.")
    else:
        case, expected = multi_direction_change(int(start), first_direction, lengths)
        if st.button("Check the solution", type="primary"):
            show_result(case, expected, run_solution(case))
        else:
            st.caption("Generated input")
            st.code(json.dumps(case), language="json")

# --- 3. Any array --------------------------------------------------------------
with tab_try:
    st.write(
        "Paste any array of whole numbers to see what the solution returns. "
        "There is no expected answer here, so you are the judge."
    )
    raw = st.text_input("Array", value="[10, 11, 12, 11, 10, 9, 8, 7, 6, 5, 6]")
    if st.button("Run solution.js"):
        try:
            case = json.loads(raw)
            valid = (
                isinstance(case, list)
                and len(case) <= MAX_LENGTH
                and all(isinstance(n, int) and not isinstance(n, bool) for n in case)
            )
        except json.JSONDecodeError:
            valid = False
        if not valid:
            st.warning(f"Enter a JSON array of up to {MAX_LENGTH} whole numbers, like [1, 2, 3, 2].")
        else:
            st.caption("Longest run found")
            st.code(json.dumps(run_solution(case)), language="json")

st.divider()
st.caption(
    "Code on GitHub: [Tinasafaie004/smart-test-case-generator]"
    "(https://github.com/Tinasafaie004/smart-test-case-generator)"
)
