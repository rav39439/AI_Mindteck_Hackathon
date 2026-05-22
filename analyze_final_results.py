from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm
from helper import clean_llm_output



def analyze_result(result, testscenarios):
    """
    Uses LLM to analyze test execution results and map failures back to scenarios.
    """

    system_prompt = SystemMessage(content="""
    You are an expert QA test result analyzer.

    Your job is to analyze:
    1. Test execution output (stdout/stderr)
    2. Original test scenarios

    You must identify:
    - Which scenarios passed
    - Which scenarios failed
    - Why they failed (based only on given result text)
    - Match failure messages to the correct scenario

    STRICT RULES:
    - Do NOT assume missing information
    - Use ONLY provided result and scenarios
    - Do NOT hallucinate errors not present in result
    - If mapping is unclear, mark scenario as "unknown failure"

    OUTPUT FORMAT MUST BE JSON ONLY:

    {
    "passed": ["scenario1", "scenario2"],
    "failed": [
        {
        "scenario": "scenario name/description",
        "reason": "exact reason from logs",
        "error_snippet": "relevant log snippet"
        }
    ],
    "unknown": []
    }

    Return ONLY JSON. No explanation. No markdown.
    """)

    user_prompt = HumanMessage(content=f"""
    TEST SCENARIOS:
    {testscenarios}

    EXECUTION RESULT:
    {result}
    """)

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    return cleaned

