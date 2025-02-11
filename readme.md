## Natural Language to SQL Query Interface
A modern web application that converts natural language questions into SQL queries using AI, complete with a FastAPI backend and Streamlit frontend.

## 🌟Features

✅ Natural language to SQL query conversion

✅ Interactive web interface with Streamlit

✅ FastAPI backend with robust error handling

✅ Vector similarity search for query examples

✅ Real-time query execution

✅ Table schema exploration

✅ Export results to CSV

✅ Comprehensive logging

## 🛠️ Technology Stack

### Backend

1. FastAPI

2. PostgreSQL

### Frontend

1. Streamlit

### AI/ML

1. Groq (Llama-3.1-8b-instant)

2. HuggingFace Embeddings

3. LangChain

### Others

1. Vector Store: Qdrant

2. Database Interface: psycopg2

## 🚀 Installation

1. Clone the repository:
```bash
   git clone https://github.com/yourusername/nl2sql-interface.git
   cd nl2sql-interface
```

2. Create and activate a virtual environment:

```bash 
   -m venv venv
```
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

bashCopypip install -r requirements.txt

4. Create a .env file in the project root:

envCopyPOSTGRES_DB=dvdrental
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
GROQ_API_KEY=your_groq_api_key

## 🎯 Usage

Start the FastAPI backend:

bashCopyuvicorn api:app --reload

In a new terminal, start the Streamlit frontend:

bashCopystreamlit run frontend.py

Open your browser and navigate to:


Frontend: http://localhost:8501
API docs: http://localhost:8000/docs