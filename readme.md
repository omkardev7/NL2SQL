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
2. HuggingFace Embeddings(all-mpnet-base-v2)
3. LangChain

### Others

1. Vector Store: Qdrant

2. Database Interface: psycopg2

## 🚀 Installation

1. Clone the repository:
```bash
   git clone https://github.com/omkardev7/NL2SQL.git
   cd NL2SQL
```

2. Create and activate a virtual environment:

```bash 
   -m venv venv
```
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root:

```bash
POSTGRES_DB=dvdrental
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
GROQ_API_KEY=your_groq_api_key
```

## 🎯 Usage

1. Start the FastAPI backend:

```bash
uvicorn api:app --reload
```
2. In a new terminal, start the Streamlit frontend:

```bash
streamlit run frontend.py
```

3. Open your browser and navigate to:

Frontend: http://localhost:8501
API docs: http://localhost:8000/docs