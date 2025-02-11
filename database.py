# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from config import DB_CONFIG

logger = logging.getLogger(__name__)

def get_db_connection():
    logger.info("Establishing database connection...")
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        logger.info("Database connection established successfully")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise

def get_table_schemas():
    logger.info("Fetching database schemas...")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                logger.debug("Querying for table names...")
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = cur.fetchall()
                
                schemas = {}
                for table in tables:
                    table_name = table['table_name']
                    logger.debug(f"Fetching schema for table: {table_name}")
                    cur.execute(f"""
                        SELECT column_name, data_type, column_default
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}'
                    """)
                    columns = cur.fetchall()
                    schemas[table_name] = columns
                
                logger.info(f"Successfully retrieved schemas for {len(schemas)} tables")
                return schemas
    except Exception as e:
        logger.error(f"Error fetching database schemas: {str(e)}")
        raise

def execute_sql(query: str):
    logger.info(f"Executing SQL query: {query}")
    try:
        clean_query = query.replace('\\', '') 
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                logger.info(f"Executing query: {clean_query}")
                cur.execute(clean_query)
                results = cur.fetchall()
                logger.info(f"Query executed successfully. Returned {len(results)} rows")
                return results
    except Exception as e:
        logger.error(f"Error executing SQL query: {str(e)}")
        raise