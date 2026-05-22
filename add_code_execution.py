from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm



def add_code_execution( code_with_imports: str):
    system_prompt = SystemMessage(content="""
1. Remove duplicate imports.
2. Keep imports only at the top.
3. Remove unnecessary imports.
4. Organize imports cleanly.
5. You MUST return the EXACT input code unchanged.
6. Do NOT delete, modify, reorder, or refactor any existing code or test functions.
7. You may ONLY APPEND new code at the END of the file.
8. You must add exactly one function run_all_tests() which collects all functions starting with "test_" using globals().values(), filters using callable(obj) and obj.__name__.startswith("test_"), executes each test safely using try/except, and prints PASS/FAIL for each test.
9. Test discovery MUST ONLY use globals().values(); any use of dir(), __builtins__, or alternative reflection methods is invalid.
10. You must add this exact execution block at the end of the file:
11. if __name__ == "__main__": run_all_tests()
12. In the block if testcase is run without error then print ("ran successfully") else print ("test case run failed")
13. DO NOT remove or regenerate existing test cases.
14. DO NOT output partial code.
15. Output must be:
original code (unchanged)
plus appended runner code only
11. Output ONLY valid Python code.
12.No markdown, no explanation, no text outside code.
    """)

    user_prompt = HumanMessage(content=f"""
    Here is the code:

    {code_with_imports}

    Now add a test runner that executes all tests.
    """

)

    response = llm.invoke([system_prompt, user_prompt])
    return response.content
