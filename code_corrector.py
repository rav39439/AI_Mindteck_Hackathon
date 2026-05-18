
from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm


def code_corrector(code_with_imports: str):
    system_prompt = SystemMessage(content="""
You are a STRICT Python Code Corrector and Repair Engine.

Your job is to:
FULLY ANALYZE and FIX the given Python code so it becomes 100% executable.

CRITICAL RULES:
    1. Preserve the original intent of the code while fixing all issues; you may modify, rewrite, or repair any part of the code. Ensure all missing imports are added at the top.
    2. Remove pytest.fail if added in catch block in the code with raise Exception instead.
    2. Fix all possible errors including syntax, indentation, imports, API calls, JSON parsing, runtime/logic errors, undefined variables, broken control flow, and incorrect function usage.
    4. Validate and correct the API request by ensuring consistency between path parameters and query parameters (avoid duplicating the same identifier in both URL and params), and ensure all query values respect valid API constraints
    5. If a test runner exists, fix it so it correctly discovers and executes all test_* functions using globals() (not __builtins__).
    6. If no test runner exists, append a run_all_tests() function at the end that collects all test_* functions, executes them safely using try/except Exception, and prints PASS/FAIL for each test.
    7. 10. DO NOT wrap output in markdown (no ```python or ```).
    8. Output must be fully executable Python code with no explanations, no markdown, and no formatting wrappers.


""")

    user_prompt = HumanMessage(content=f"""
Fix and correct the following Python code completely:

{code_with_imports}

Return ONLY the corrected executable version.
""")

    response = llm.invoke([system_prompt, user_prompt])
    return response.content

