# API/utils.py
import re

def validate_query(query: str) -> bool:
    """
    Validate the format of the user query.
    Returns True if the query is valid, False otherwise.
    """
    # Basic validation (you can add more complex checks)
    return bool(query.strip())  # Ensure the query is not empty or just whitespace

def extract_key_information(document: str) -> str:
    """
    Extract key information from the document (e.g., to improve answer quality).
    """
    # Simple example: extract sentences or key phrases
    return document[:500]  # For simplicity, we return the first 500 characters

