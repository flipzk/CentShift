# CentShift | AI-Powered Personal Finance Tracker

CentShift is a full-stack financial management application designed to modernize personal finance tracking. Unlike traditional solutions, it decouples business logic from the user interface and leverages **Google's Gemini AI** to automate data entry through receipt scanning and computer vision.

The project demonstrates a clean architecture approach using Python, separating data models, schemas, and business rules to ensure scalability and maintainability.

## Key Features

* **AI Receipt Scanner**: Automated data extraction from physical receipts. The system utilizes Google Gemini (LLM) to parse images and extract transaction details (Total, Date, Category, Description) into structured JSON.
* **Smart Budgeting Algorithms**: Implementation of financial strategies (e.g., 50/30/20, Smart Saver) within a dedicated logic layer (`budget.py`), completely isolated from the API layer.
* **Interactive Dashboard**: Real-time data visualization of spending versus budget limits using Streamlit and Pandas for data processing.
* **Transaction Management**: Full CRUD capabilities for expenses, incomes, and investments with category-based filtering.
* **Scalable Architecture**: Built with SQLModel to allow easy migration from SQLite to PostgreSQL if required.

## Tech Stack

* **Backend**: Python 3.10+, FastAPI, SQLModel (SQLAlchemy + Pydantic).
* **Frontend**: Streamlit, Pandas, Matplotlib.
* **AI/ML**: Google Generative AI SDK (Gemini 1.5 Flash).
* **Database**: SQLite (Development).
* **Tooling**: Uvicorn, Python-Dotenv.

---

## Installation & Setup Guide

Follow these steps to set up the environment locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/CentShift.git](https://github.com/YOUR_USERNAME/CentShift.git)
cd CentShift

2. Environment Configuration
This project requires an API Key for the AI features.

Create a file named .env in the root directory.

Add your Google Gemini API key as shown below:

Ini, TOML

GOOGLE_API_KEY="your_api_key_here"
3. Install Dependencies
Using a virtual environment is recommended.

Bash

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
Projeto Pessoal - CentShift
Gem personalizado
Aqui está a versão final e profissional do README.md. Removi o excesso de emojis, foquei numa linguagem técnica direta e estruturei tudo num único bloco para copiares e colares.

Esta versão transmite seriedade e foco na arquitetura do software, ideal para análise por Tech Leads.

Ficheiro: README.md
Markdown
# CentShift | AI-Powered Personal Finance Tracker

CentShift is a full-stack financial management application designed to modernize personal finance tracking. Unlike traditional solutions, it decouples business logic from the user interface and leverages **Google's Gemini AI** to automate data entry through receipt scanning and computer vision.

The project demonstrates a clean architecture approach using Python, separating data models, schemas, and business rules to ensure scalability and maintainability.

## Key Features

* **AI Receipt Scanner**: Automated data extraction from physical receipts. The system utilizes Google Gemini (LLM) to parse images and extract transaction details (Total, Date, Category, Description) into structured JSON.
* **Smart Budgeting Algorithms**: Implementation of financial strategies (e.g., 50/30/20, Smart Saver) within a dedicated logic layer (`budget.py`), completely isolated from the API layer.
* **Interactive Dashboard**: Real-time data visualization of spending versus budget limits using Streamlit and Pandas for data processing.
* **Transaction Management**: Full CRUD capabilities for expenses, incomes, and investments with category-based filtering.
* **Scalable Architecture**: Built with SQLModel to allow easy migration from SQLite to PostgreSQL if required.

## Tech Stack

* **Backend**: Python 3.10+, FastAPI, SQLModel (SQLAlchemy + Pydantic).
* **Frontend**: Streamlit, Pandas, Matplotlib.
* **AI/ML**: Google Generative AI SDK (Gemini 1.5 Flash).
* **Database**: SQLite (Development).
* **Tooling**: Uvicorn, Python-Dotenv.

---

## Installation & Setup Guide

Follow these steps to set up the environment locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/CentShift.git](https://github.com/YOUR_USERNAME/CentShift.git)
cd CentShift
2. Environment Configuration
This project requires an API Key for the AI features.

Create a file named .env in the root directory.

Add your Google Gemini API key as shown below:

Ini, TOML
GOOGLE_API_KEY="your_api_key_here"
3. Install Dependencies
Using a virtual environment is recommended.

Bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
Running the Application
The architecture requires the Backend and Frontend to run as separate processes. Open two terminal windows.

Terminal 1: Backend API
Initialize the FastAPI server. The database will be created automatically on the first startup.

Bash
uvicorn backend.main:app --reload
Server running at: http://127.0.0.1:8000

Terminal 2: Frontend Dashboard
Launch the Streamlit interface.

Bash
streamlit run frontend/app.py
Dashboard accessible at: http://localhost:8501

Project Structure
The codebase follows a modular structure to ensure separation of concerns:

Plaintext
CentShift/
├── backend/
│   ├── main.py         # API Entry point & Route definitions
│   ├── ai_service.py   # AI integration logic (Gemini SDK)
│   ├── budget.py       # Pure Python business logic (Budgeting strategies)
│   ├── models.py       # Database models (SQLModel)
│   ├── schemas.py      # Pydantic data validation schemas
│   └── crud.py         # Database interface layer
├── frontend/
│   └── app.py          # Streamlit UI components
└── requirements.txt    # Project dependencies