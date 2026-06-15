# CodingHelperAI

CodingHelperAI is a FastAPI-based AI application designed to provide advanced coding assistance. It leverages modern GenAI technologies and integrates with robust datastores to power intelligent agent workflows.

## 🚀 Features

- **FastAPI Core**: High-performance asynchronous API web framework.
- **AI Integrations**: Built with `langchain` and supports both `openai` and `google-genai` models.
- **Vector Database**: Integration with Qdrant (`langchain-qdrant`) for fast semantic search and RAG (Retrieval-Augmented Generation) workflows.
- **Relational Database**: Uses `sqlmodel` (SQLAlchemy and Pydantic) and `alembic` for database migrations with PostgreSQL.
- **Caching & Memory**: Redis integration for high-speed caching and agent memory management.
- **Document Processing**: Includes tools like `pandas` and `pypdf` for data ingestion and text extraction.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:
- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)**: Fast Python package and project manager.
- **Docker** and **Docker Compose**: For running the supporting database and caching services (PostgreSQL & Redis).

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd codingHelperAi
   ```

2. **Start the database services:**
   Start the PostgreSQL and Redis containers using Docker Compose.
   ```bash
   docker-compose up -d
   ```

3. **Install dependencies using `uv`:**
   ```bash
   uv sync
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add any required environment variables (e.g., `OPENAI_API_KEY`, `GOOGLE_API_KEY`, Database URIs). The application uses `pydantic-settings` to manage environment configurations.

## 🚦 Running the Application

You can start the FastAPI application using the integrated `uvicorn` server.

**Using `uv`:**
```bash
uv run fastapi dev app/main.py
```
*Alternatively, you can run the application directly if your virtual environment is activated:*
```bash
python app/main.py
```

The API will be accessible at: `http://localhost:8000`
Interactive API documentation (Swagger UI) is available at: `http://localhost:8000/docs`

## 📂 Project Structure

```text
codingHelperAi/
├── app/
│   ├── api/            # API routing and endpoints
│   ├── core/           # Core configurations and prompts
│   ├── db/             # Database session and configuration
│   ├── models/         # Pydantic and SQLModel definitions (requests/responses)
│   ├── services/       # Business logic and AI memory services
│   ├── utils/          # Helper utilities
│   ├── dependencies.py # FastAPI dependencies
│   └── main.py         # Application entry point
├── docker-compose.yml  # Local infrastructure (Postgres, Redis)
├── pyproject.toml      # Project metadata and dependencies
└── uv.lock             # Exact dependency lockfile
```

## 🧪 Development

The project uses `ruff` for linting/formatting, `mypy` for static type checking, and `pytest` for testing.

To format your code:
```bash
uv run ruff format
```

To run type checking:
```bash
uv run mypy app
```

To run tests:
```bash
uv run pytest
```