import subprocess
import sys
from llm import llm 
from typing import Optional


def handle_error_and_correct(code: str, stderr: str):
    """
    Called only when execution error is detected.
    Sends original code + stderr to LLM,
    receives corrected code, and saves to corrected.py
    """

    print("\n[INFO] Error detected. Sending to LLM for correction...\n")

    # ----- Construct LLM Prompt -----
    prompt = f"""
    The following Python test code has errors.

    Original Code:
    ----------------
    {code}

    Error Output (stderr):
    ----------------
    {stderr}

    Please correct the code and return only the corrected Python code.
    """

    # ----- CALL YOUR LLM HERE -----
    # Replace this mock function with your actual LLM call
    corrected_code = call_llm(prompt)

    if corrected_code:
        with open("corrected.py", "w", encoding="utf-8") as f:
            f.write(corrected_code)

        return corrected_code
    else:
        return "[ERROR] LLM did not return corrected code"


def call_llm(prompt: str) -> str:
    """
    Uses the existing LLM to regenerate corrected test cases.
    """

    print("\n[INFO] Calling LLM...\n")

    # Build corrected prompt
    final_prompt = f"""
    The previously generated test code failed during execution.

    {prompt}

    TASK:
    - Fix the code so it runs successfully.

    STRICT OUTPUT RULES:
    - Return ONLY valid Python code
    - Do NOT include explanations
    - Do NOT include comments describing the fix
    - Do NOT include markdown (no ``` or ```python)
    - Do NOT include any text before or after the code
    - Output must start with Python code and end with Python code
    - No conversational text is allowed

    Failure to follow these rules will invalidate the response.
"""
    response = llm.invoke(final_prompt)

    # Extract actual text from LLM response
    corrected_code = response.content

    return corrected_code