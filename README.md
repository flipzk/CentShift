# CentShift

CentShift is a full-stack personal finance application designed to automate expense tracking using Artificial Intelligence. The system decouples business logic from the user interface and integrates Google Gemini 2.0 Flash to extract transaction data from physical receipts via Computer Vision.

This project demonstrates a scalable software architecture using FastAPI, Streamlit, and Docker orchestration.

## Demo

<video src="https://github.com/flipzk/CentShift/raw/main/demo.mp4" width="100%" controls preload="none"></video>

## Key Features

* **AI Receipt Scanning:** Automated extraction of total amount, date, category, and description from receipt images using LLMs (Google Gemini).
* **Budget Allocation Logic:** Implementation of standard financial strategies (e.g., 50/30/20, Smart Saver) isolated in a dedicated logic layer.
* **Dashboard & Analytics:** Real-time visualization of financial data and budget limits.
* **Transaction Management:** Complete CRUD (Create, Read, Update, Delete) operations for expenses, incomes, and investments.
* **Containerization:** Fully containerized application using Docker and Docker Compose for consistent deployment.

## Tech Stack

* **Backend:** Python 3.10+, FastAPI
* **Database & ORM:** SQLite, SQLModel (SQLAlchemy + Pydantic)
* **Frontend:** Streamlit, Pandas
* **AI & ML:** Google Generative AI SDK (Gemini 2.0 Flash)
* **Infrastructure:** Docker, Docker Compose

## Installation and Setup

You can run this project using Docker (recommended) or manually with a Python environment.

### Prerequisites

* Git
* Docker Desktop (for Docker method)
* Python 3.10+ (for Manual method)
* A Google Gemini API Key

### Configuration

Before running the application, you must configure the environment variables.

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/CentShift.git](https://github.com/YOUR_USERNAME/CentShift.git)
    cd CentShift
    ```

2.  Create a `.env` file in the root directory and add your API key:
    ```ini
    GOOGLE_API_KEY="your_api_key_here"
    ```

---

### Method 1: Running with Docker (Recommended)

This method ensures all dependencies and services run in an isolated environment.

1.  Build and start the services:
    ```bash
    docker compose up --build
    ```

2.  Access the application:
    * **Frontend:** http://localhost:8501
    * **API Documentation:** http://localhost:8000/docs

---

### Method 2: Manual Installation

1.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the Backend (Terminal 1):
    ```bash
    uvicorn backend.main:app --reload
    ```

4.  Run the Frontend (Terminal 2):
    ```bash
    streamlit run frontend/app.py
    ```

## Project Structure

* **backend/**: Contains the API source code, database models, schemas, and business logic.
    * `ai_service.py`: Handles interaction with Google Gemini API.
    * `budget.py`: Contains the financial allocation algorithms.
    * `main.py`: FastAPI entry point and route definitions.
* **frontend/**: Contains the Streamlit user interface code.
* **Dockerfile**: Instructions for building the container image.
* **docker-compose.yml**: Configuration for orchestrating the frontend and backend services.

## License

This project is open-source and available under the MIT License.
