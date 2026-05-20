
import subprocess
import sys
from llm import llm 
from typing import Optional
def write_and_run_test_file(code: str, filename: str = "testcases.py"):
    """
    Writes generated test code to file and executes it.
    """

    loop=1

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"\n[INFO] Test file written: {filename}\n")

    try:
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True
        )

        print("===== STDOUT =====")
        print(result.stdout)
        if result.stderr:
            print("===== STDERR =====")           # print(result.stderr)
            print("\n[INFO] Error detected. Sending to LLM for correction...\n")
            loop+=1
            try:
                handle_error_and_correct(code, result.stderr)
                result = subprocess.run(
                    [sys.executable, filename],
                    capture_output=True,
                    text=True
                )

                print("===== STDOUT =====")
                print(result.stdout)
            except Exception as e:
                print(f"[ERROR] Execution failed: {e}")

        if(result.stdout==""):
            print("===== STDERR =====")
            print("Test cases could not be run.No output was captured.")
            print("\n[INFO] Error detected. Sending to LLM for correction...\n")
            try:
                handle_error_and_correct_empty(code, "Test cases could not be run.No output was captured.")
                result = subprocess.run(
                    [sys.executable, filename],
                    capture_output=True,
                    text=True
                )

                print("===== STDOUT =====")
                print(result.stdout)
            except Exception as e:
                print(f"[ERROR] Execution failed: {e}")

    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")





def run_test_file(filename: str = "testcases.py"):
    """
    Reads Python code from filename, executes it,
    and triggers correction if errors occur.
    """

    try:
        # Read code from file
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        print(f"\n[INFO] Running test file: {filename}\n")

        # Execute file
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True
        )

        print("===== STDOUT =====")
        print(result.stdout)

        if(result.stdout==""):
            print("===== STDERR =====")
            print("Test cases could not be run.No output was captured.")
            print("\n[INFO] Error detected. Sending to LLM for correction...\n")
            try:
                handle_error_and_correct(code, "Test cases could not be run.No output was captured.")
                result = subprocess.run(
                    [sys.executable, filename],
                    capture_output=True,
                    text=True
                )

                print("===== STDOUT =====")
                print(result.stdout)
            except Exception as e:
                print(f"[ERROR] Execution failed: {e}")

        # if result.stderr:
        #     print("===== STDERR =====")
        #     print(result.stderr)

        #     # If error detected → call correction function
        #     handle_error_and_correct(code, result.stderr)

    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")


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
        with open("testcases.py", "w", encoding="utf-8") as f:
            f.write(corrected_code)

        print("[INFO] Corrected code saved to corrected.py")
    else:
        print("[ERROR] LLM did not return corrected code.")

def handle_error_and_correct_empty(code: str, stderr: str):
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
    "The code is not producing any output. Correct the code so that it should produce output.
    STRICT RULES:
    Use simple logic to run the testcases and produce output.
    Do not use unittest library.
    "

    Please correct the code and return only the corrected Python code.
    """

    # ----- CALL YOUR LLM HERE -----
    # Replace this mock function with your actual LLM call
    corrected_code = call_llm(prompt)

    if corrected_code:
        with open("testcases.py", "w", encoding="utf-8") as f:
            f.write(corrected_code)

        print("[INFO] Corrected code saved to corrected.py")
    else:
        print("[ERROR] LLM did not return corrected code.")

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


# def run_test_file(filename: str = "testcases.py"):
#     """
#     Reads Python code from filename, executes it,
#     and triggers correction if errors occur.
#     """

#     try:
#         print("\n[INFO] Running file for the second time: {filename}\n")
#         # Read code from file
#         with open(filename, "r", encoding="utf-8") as f:
#             code = f.read()

#         print(f"\n[INFO] Running test file: {filename}\n")

#         # Execute file
#         result = subprocess.run(
#             [sys.executable, filename],
#             capture_output=True,
#             text=True
#         )

#         print("===== STDOUT =====")
#         print(result.stdout)

#         if result.stderr:
#             print("===== STDERR =====")
#             print(result.stderr)

#             # If error detected → call correction functio
#     except Exception as e:
#         print(f"[ERROR] Execution failed: {e}")



