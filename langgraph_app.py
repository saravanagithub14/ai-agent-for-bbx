from dotenv import load_dotenv

from typing import TypedDict

from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END

# -----------------------------------
# LOAD API KEY
# -----------------------------------

load_dotenv()

# -----------------------------------
# LLM
# -----------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# -----------------------------------
# SHARED STATE
# -----------------------------------

class AgentState(TypedDict):

    task: str

    plan: str

    research: str

    code: str

    test_result: str

    review: str

    debug_notes: str


# -----------------------------------
# AGENT 1 — PLANNER
# -----------------------------------

def planner(state):

    task = state["task"]

    prompt = f"""
    You are a senior software architect.

    Create a development plan for this task:

    Task:
    {task}
    """

    response = llm.invoke(prompt)

    print("\n🧠 PLANNER FINISHED\n")

    return {
        "plan": response.content
    }

# -----------------------------------
# AGENT 2 — RESEARCHER
# -----------------------------------

def researcher(state):

    task = state["task"]

    plan = state["plan"]

    prompt = f"""
    Research the best approach for this project.

    Task:
    {task}

    Plan:
    {plan}

    Suggest:
    - libraries
    - architecture
    - implementation ideas
    """

    response = llm.invoke(prompt)

    print("\n📚 RESEARCHER FINISHED\n")

    return {
        "research": response.content
    }

# -----------------------------------
# AGENT 3 — CODER
# -----------------------------------

def coder(state):

    task = state["task"]

    research = state["research"]

    debug_notes = state.get("debug_notes", "")

    prompt = f"""
    You are a Python developer.

    Build Python code for this task.

    Task:
    {task}

    Research:
    {research}

    Previous Debug Notes:
    {debug_notes}

    Generate clean Python code only.
    """

    response = llm.invoke(prompt)

    print("\n💻 CODER FINISHED\n")

    return {
        "code": response.content
    }

# -----------------------------------
# AGENT 4 — TESTER
# -----------------------------------

def tester(state):

    code = state["code"]

    prompt = f"""
    You are a software tester.

    Analyze this Python code.

    Check for:
    - syntax issues
    - missing imports
    - logical problems

    Respond ONLY with:
    PASS

    or

    FAIL: followed by reason.

    Code:
    {code}
    """

    response = llm.invoke(prompt)

    print("\n🧪 TESTER FINISHED\n")

    return {
        "test_result": response.content
    }

# -----------------------------------
# AGENT 5 — DEBUGGER
# -----------------------------------

def debugger(state):

    test_result = state["test_result"]

    code = state["code"]

    prompt = f"""
    You are a debugging expert.

    Fix the problems in this code.

    Test Result:
    {test_result}

    Code:
    {code}

    Explain what should be fixed.
    """

    response = llm.invoke(prompt)

    print("\n🐞 DEBUGGER FINISHED\n")

    return {
        "debug_notes": response.content
    }

# -----------------------------------
# AGENT 6 — REVIEWER
# -----------------------------------

def reviewer(state):

    code = state["code"]

    prompt = f"""
    You are a senior code reviewer.

    Improve this code:
    - readability
    - optimization
    - comments
    - structure

    Code:
    {code}
    """

    response = llm.invoke(prompt)

    print("\n✅ REVIEWER FINISHED\n")

    return {
        "review": response.content
    }

# -----------------------------------
# CONDITIONAL ROUTING
# -----------------------------------

def route_after_testing(state):

    result = state["test_result"]

    if "PASS" in result:
        return "reviewer"

    return "debugger"

# -----------------------------------
# BUILD GRAPH
# -----------------------------------

workflow = StateGraph(AgentState)

# ADD NODES

workflow.add_node("planner", planner)

workflow.add_node("researcher", researcher)

workflow.add_node("coder", coder)

workflow.add_node("tester", tester)

workflow.add_node("debugger", debugger)

workflow.add_node("reviewer", reviewer)

# ENTRY POINT

workflow.set_entry_point("planner")

# NORMAL EDGES

workflow.add_edge("planner", "researcher")

workflow.add_edge("researcher", "coder")

workflow.add_edge("coder", "tester")

# CONDITIONAL EDGES

workflow.add_conditional_edges(
    "tester",
    route_after_testing,
    {
        "reviewer": "reviewer",
        "debugger": "debugger"
    }
)

# LOOP BACK AFTER DEBUGGING

workflow.add_edge("debugger", "coder")

# FINISH

workflow.add_edge("reviewer", END)

# -----------------------------------
# COMPILE GRAPH
# -----------------------------------

app = workflow.compile()

# -----------------------------------
# RUNNER
# -----------------------------------

def run_task(task: str) -> dict[str, str]:
    """Invoke the LangGraph workflow for a given software task."""
    if not task or not task.strip():
        raise ValueError("Task must not be empty.")

    result = app.invoke({
        "task": task.strip()
    })

    return {
        "plan": result.get("plan", ""),
        "research": result.get("research", ""),
        "code": result.get("code", ""),
        "test_result": result.get("test_result", ""),
        "review": result.get("review", ""),
    }

# -----------------------------------
# CLI ENTRYPOINT
# -----------------------------------

if __name__ == "__main__":
    task = input("\nEnter Software Task: ")
    result = run_task(task)

# -----------------------------------
# FINAL OUTPUTS
# -----------------------------------

    print("\n" + "=" * 50)
    print("🧠 DEVELOPMENT PLAN")
    print("=" * 50)

    print(result["plan"])

    print("\n" + "=" * 50)
    print("📚 RESEARCH")
    print("=" * 50)

    print(result["research"])

    print("\n" + "=" * 50)
    print("💻 GENERATED CODE")
    print("=" * 50)

    print(result["code"])

    print("\n" + "=" * 50)
    print("🧪 TEST RESULT")
    print("=" * 50)

    print(result["test_result"])

    print("\n" + "=" * 50)
    print("✅ FINAL REVIEW")
    print("=" * 50)

    print(result["review"])
