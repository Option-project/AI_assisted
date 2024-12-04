from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from API.model_integration import generate_answer  # Import the answer generation function

# Initialize the FastAPI application
app = FastAPI()

# Define the input data model (request body) for the API
class QueryRequest(BaseModel):
    question: str  # The question input by the user

# Define the response data model for the API
class QueryResponse(BaseModel):
    answer: str  # The generated answer from the model

# Define the API endpoint for generating answers
@app.post("/query", response_model=QueryResponse)
async def get_answer(query: QueryRequest):
    """
    Handle POST requests to the /query endpoint.
    Args:
        query (QueryRequest): The user input containing the question.
    Returns:
        QueryResponse: The generated answer.
    """
    try:
        # Call the model integration to generate an answer
        answer = generate_answer(query.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        # If an error occurs, return a 500 error
        raise HTTPException(status_code=500, detail="Error generating answer")

# Swagger UI will automatically be available at /docs to test the API
