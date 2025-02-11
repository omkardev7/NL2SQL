# vector_store.py
from langchain_community.vectorstores import Qdrant
import logging
from config import embeddings

logger = logging.getLogger(__name__)

def initialize_vector_store():
    logger.info("Initializing vector store...")
    try:
        few_shot_examples = [
            {
                "question": "How many films are in the database?",
                "query": "SELECT COUNT(*) FROM film"
            },
            {
                "question": "List all customers in the database",
                "query": "SELECT first_name, last_name FROM customer"
            },
            {
                "question": "Can you find the movie titled Agent Truman?",
                "query": "SELECT * FROM film WHERE title = 'Agent Truman'"
            },
            {
                "question": "Which movies were released in 2006?",
                "query": "SELECT * FROM film WHERE release_year = 2006"
            },
            {
                "question": "What are the unique last names of actors?",
                "query": "SELECT DISTINCT last_name FROM actor"
            },
            {
                "question": "Can you show me a list of actors sorted by their first name alphabetically?",
                "query": "SELECT * FROM actor ORDER BY first_name ASC"
            },
            {
                "question": "Can you find movies that mention monkey in their description?",
                "query": "SELECT * FROM film WHERE description LIKE '%monkey%';"
            }
        ]
        
        logger.debug(f"Converting {len(few_shot_examples)} examples to texts")
        texts = [f"Question: {ex['question']}\nQuery: {ex['query']}" for ex in few_shot_examples]
        
        logger.info("Creating Qdrant vector store...")
        qdrant = Qdrant.from_texts(
            texts,
            embeddings,
            location=":memory:",
            collection_name="nl2sql_examples"
        )
        logger.info("Vector store initialized successfully")
        return qdrant
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}")
        raise

def get_similar_examples(qdrant, question: str, k: int = 2):
    logger.info(f"Finding {k} similar examples for question: {question}")
    try:
        examples = qdrant.similarity_search(question, k=k)
        logger.info(f"Found {len(examples)} similar examples")
        return examples
    except Exception as e:
        logger.error(f"Error finding similar examples: {str(e)}")
        raise