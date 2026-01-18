from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from indexer import get_retriever

# --- 1. Define the Tool (The "Hands") ---
# This allows the LLM to call your Python function 
@tool
def search_codebase(query: str):
    """
    Useful for searching the project code to understand context, 
    find class definitions, or locate error sources.
    """
    print(f"🕵️ Agent is searching for: {query}")
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    # Return the code chunks to the LLM
    return "\n\n".join([f"File: {d.metadata.get('source')}\nCode:\n{d.page_content}" for d in docs])

# --- 2. Setup the Agent (The "Brain") ---
def get_agent():
    # We use GPT-4o or Turbo because debugging requires high intelligence
    # temperature=0 makes it deterministic (crucial for code)
    llm = ChatOpenAI(model="gpt-4o", temperature=0) 
    
    tools = [search_codebase]
    
    # The Prompt Engineering (SDE 3 Level: Role + Constraints)
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a Senior Software Engineer assisting with debugging. "
         "You have access to a codebase search tool. "
         "RULES: \n"
         "1. ALWAYS search the codebase for the relevant files before guessing.\n"
         "2. If the user provides a stack trace, search for the error line.\n"
         "3. Provide the fix in a code block."
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), # Memory for the agent's thought process
    ])
    
    # Construct the agent loop
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # verbose=True lets us see the "Thought Process" in the terminal (Great for demos!)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)