# frontend.py
import streamlit as st
import requests
import pandas as pd
from typing import Dict, List, Optional, Tuple
import json
from database import get_db_connection, get_table_schemas
import logging
from datetime import datetime
import plotly.express as px
from collections import defaultdict
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
API_URL = "http://localhost:8000/query"
CACHE_TTL = 300  # 5 minutes cache for database info

class DatabaseManager:
    """Manages database connections and schema information"""
    
    def __init__(self):
        self.last_refresh = None
        self.db_info = None
        self.schemas = None
    
    def get_database_info(self) -> Tuple[str, List[str], Dict]:
        """Get database name, tables, and schemas with caching"""
        try:
            current_time = time.time()
            if (not self.last_refresh or 
                current_time - self.last_refresh > CACHE_TTL):
                
                conn = get_db_connection()
                db_name = conn.info.dbname
                schemas = get_table_schemas()
                tables = list(schemas.keys())
                
                self.db_info = (db_name, tables, schemas)
                self.last_refresh = current_time
                logger.info("Database info refreshed successfully")
                
            return self.db_info
        except Exception as e:
            logger.error(f"Error fetching database info: {e}")
            return "Unknown", [], {}

class QueryManager:
    """Handles query execution and result processing"""
    
    @staticmethod
    def send_query(question: str) -> Optional[Dict]:
        """Send query to API with error handling"""
        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.error("Query timed out. Please try again.")
            logger.error("API request timed out")
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with API: {str(e)}")
            logger.error(f"API request failed: {e}")
        return None
    
    @staticmethod
    def process_results(results: List[Dict]) -> pd.DataFrame:
        """Process query results into a pandas DataFrame"""
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Convert datetime columns
        for col in df.select_dtypes(include=['object']).columns:
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                continue
        
        return df

class UIManager:
    """Manages Streamlit UI components and layouts"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.initialize_session_state()
    
    @staticmethod
    def initialize_session_state():
        """Initialize session state variables"""
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        if 'current_query' not in st.session_state:
            st.session_state.current_query = ""
    
    def render_sidebar(self, db_name: str, tables: List[str], schemas: Dict):
        """Render sidebar with database information and examples"""
        with st.sidebar:
            st.header("Database Information")
            st.info(f"Connected to: **{db_name}**")
            
            # Table Explorer
            st.subheader("Table Explorer")
            selected_table = st.selectbox(
                "Select a table to explore:",
                options=tables
            )
            
            if selected_table:
                table_schema = schemas[selected_table]
                df_schema = pd.DataFrame(table_schema)
                st.dataframe(
                    df_schema,
                    column_config={
                        "column_name": "Column",
                        "data_type": "Type",
                        "column_default": "Default"
                    },
                    hide_index=True
                )
            
            # Query History
            st.subheader("Query History")
            for idx, (q, timestamp) in enumerate(st.session_state.query_history[-5:]):
                with st.expander(f"Query {len(st.session_state.query_history) - idx}"):
                    st.text(f"Time: {timestamp}")
                    st.text(q)
                    if st.button("Rerun", key=f"rerun_{idx}"):
                        st.session_state.current_query = q
                        st.experimental_rerun()
    
    def render_main_content(self):
        """Render main content area"""
        st.title("Natural Language to SQL Query Interface 🔍")
        
        # Query Input
        st.write("### Ask your question in natural language")
        question = st.text_area(
            "Enter your question:",
            value=st.session_state.current_query,
            placeholder="Example: How many films are in the database?",
            height=100,
            key="query_input"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.button("Submit Query", type="primary")
        
        return question, submit_button
    
    @staticmethod
    def display_results(df: pd.DataFrame, sql_query: str):
        """Display query results with visualizations"""
        st.write("### Generated SQL Query")
        st.code(sql_query, language="sql")
        
        st.write("### Query Results")
        if not df.empty:
            # Display results
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )
            
            # Basic visualizations for numeric columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                st.write("### Quick Visualizations")
                viz_type = st.selectbox(
                    "Select visualization type:",
                    ["Bar Chart", "Line Chart", "Scatter Plot"]
                )
                
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("Select X axis:", numeric_cols)
                    y_col = st.selectbox("Select Y axis:", 
                                       [col for col in numeric_cols if col != x_col])
                    
                    if viz_type == "Bar Chart":
                        fig = px.bar(df, x=x_col, y=y_col)
                    elif viz_type == "Line Chart":
                        fig = px.line(df, x=x_col, y=y_col)
                    else:
                        fig = px.scatter(df, x=x_col, y=y_col)
                    
                    st.plotly_chart(fig)
            
            # Export options
            st.download_button(
                label="Download Results as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f'query_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        else:
            st.info("Query executed successfully but returned no results.")

def main():
    # Page config
    st.set_page_config(
        page_title="Natural Language SQL Query Interface",
        page_icon="🔍",
        layout="wide"
    )
    
    # Initialize managers
    db_manager = DatabaseManager()
    ui_manager = UIManager(db_manager)
    query_manager = QueryManager()
    
    # Get database info
    db_name, tables, schemas = db_manager.get_database_info()
    
    # Render UI
    ui_manager.render_sidebar(db_name, tables, schemas)
    question, submit_button = ui_manager.render_main_content()
    
    if submit_button and question:
        with st.spinner("Processing your question..."):
            # Add to query history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.query_history.append((question, timestamp))
            
            # Execute query
            result = query_manager.send_query(question)
            
            if result:
                # Process and display results
                df = query_manager.process_results(result["results"])
                ui_manager.display_results(df, result["sql_query"])

if __name__ == "__main__":
    main()