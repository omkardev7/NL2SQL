# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from database import get_table_schemas, execute_sql
from vector_store import initialize_vector_store
from nl2sql import process_query
import uvicorn
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize on startup
logger.info("Initializing application...")
qdrant = initialize_vector_store()
schema = get_table_schemas()
logger.info("Application initialized successfully")

class Query(BaseModel):
    question: str

@app.post("/query")
async def handle_query(query: Query):
    logger.info(f"Received query: {query.question}")
    try:
        sql_query = await process_query(query.question, qdrant, schema)
        logger.info(f"Generated SQL query: {sql_query}")
        
        results = execute_sql(sql_query)
        logger.info(f"Query executed successfully. Returning {len(results)} results")
        
        return {
            "question": query.question,
            "sql_query": sql_query,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)