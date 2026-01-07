from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agents.fetch_agent import FetchAgent
from agents.reasoning_agent import ReasoningAgent

app = FastAPI(
    title="Politician Activity Analyzer",
    description="An API that analyzes a politician's activities, promises, and legislative record.",
    version="0.1.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fetch_agent = FetchAgent()
reasoning_agent = ReasoningAgent()

@app.get("/analyze")
async def analyze_politician(name: str):
    """
    Analyzes a politician by fetching their data and using an AI to reason about it.
    """
    if not name:
        raise HTTPException(status_code=400, detail="Politician name is required.")

    try:
        # Step 1: Fetch raw data using the FetchAgent
        raw_data = fetch_agent.get_data(name)

        # Step 2: Get analysis from the ReasoningAgent
        analysis = await reasoning_agent.analyze(name, raw_data)

        if "error" in analysis:
            raise HTTPException(status_code=500, detail=analysis["error"])

        return analysis
    except Exception as e:
        # Catch any other exceptions and return a generic error
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# To run the app: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)