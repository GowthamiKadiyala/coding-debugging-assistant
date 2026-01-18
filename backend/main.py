from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import get_agent
import os

# Import the logic we wrote in the previous step
from indexer import index_codebase, get_retriever

# Load the .env file with your API key
load_dotenv()

app = FastAPI()

# Define what data we expect from the user
class IndexRequest(BaseModel):
    path: str

class SearchRequest(BaseModel):
    query: str

class DebugRequest(BaseModel):
    error_message: str
    selected_code: str = "" # Optional: Code the user highlighted in VS Code

@app.get("/")
def home():
    return {"message": "Coding Assistant Backend is Running!"}

@app.post("/index")
def api_index(request: IndexRequest):
    """
    Tell the server to read a folder of code.
    """
    if not os.path.exists(request.path):
        raise HTTPException(status_code=400, detail="Path does not exist")
    
    return index_codebase(request.path)

@app.post("/search")
def api_search(request: SearchRequest):
    """
    Ask the server a question about the code.
    """
    retriever = get_retriever()
    # "invoke" searches the database for the query
    docs = retriever.invoke(request.query)
    
    # Format the results nicely
    results = []
    for doc in docs:
        results.append({
            "content": doc.page_content,
            "source_file": doc.metadata.get("source"),
        })
        
    return {"results": results}

@app.post("/debug")
def api_debug(request: DebugRequest):
    """
    The main endpoint. User sends an error -> Agent searches DB -> Returns Fix.
    """
    agent = get_agent()
    
    # Construct the query for the agent
    user_prompt = f"I have an error: {request.error_message}. "
    if request.selected_code:
        user_prompt += f"\nHere is the code snippet around the error:\n{request.selected_code}"
    
    # Run the agent
    response = agent.invoke({"input": user_prompt})
    
    return {"analysis": response["output"]}

# This starts the server when you run the file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)