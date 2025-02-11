# nl2sql.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import logging
from config import llm
from vector_store import get_similar_examples

logger = logging.getLogger(__name__)

def create_sql_chain(schema: str, examples: list):
    logger.info("Creating SQL chain...")
    try:
        prompt = ChatPromptTemplate.from_template("""
        You are a PostgreSQL expert. Given the question, create a syntactically correct PostgreSQL query.
        
        Important: Do not use escape characters in the SQL query. Use simple SQL syntax.
        
        Database schema:
        {schema}
        
        Similar examples:
        {examples}
        
        User question: {question}
        
        Return only the SQL query without any explanation or special characters.
        """)
        
        chain = (
            {"schema": lambda x: schema, "examples": lambda x: examples, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        logger.info("SQL chain created successfully")
        return chain
    except Exception as e:
        logger.error(f"Error creating SQL chain: {str(e)}")
        raise

async def process_query(question: str, qdrant, schema):
    logger.info(f"Processing question: {question}")
    try:
        examples = get_similar_examples(qdrant, question)
        examples_text = "\n".join([doc.page_content for doc in examples])
        
        chain = create_sql_chain(schema, examples_text)
        sql_query = await chain.ainvoke(question)
        
        logger.info(f"Generated SQL query: {sql_query}")
        return sql_query
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise