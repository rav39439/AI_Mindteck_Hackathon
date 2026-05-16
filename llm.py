
from langchain_ollama import ChatOllama



# -----------------------------
# LLM Configuration
# -----------------------------
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


llm_scenarios = ChatOllama(
    model="llama3:8b",
    temperature=0
)
