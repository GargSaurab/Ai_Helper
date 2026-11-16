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

2. **Environment Variables:**
   Create a `.env` file in the root directory with the application’s required values, including `OPENAI_API_KEY`, `DB_PASSWORD`, `REDIS_PASSWORD`, and `SECRET_KEY`. Compose requires both passwords to be non-empty. The app container connects to Postgres and Redis using the hostnames `postgres` and `redis`.
   SQL statement logging is disabled by default. Set `SQL_ECHO=true` only when you need to inspect database queries; SQLAlchemy echo logging can include bound parameter values.

3. **Start the application and its database services:**
   Docker Compose builds and starts FastAPI, PostgreSQL, and Redis. The app is published on localhost port 8000; Postgres and Redis stay on the internal Compose network. Database migrations run when the app starts.
   ```bash
   docker compose up -d --build
   ```

## 🚦 Running the Application

The application is available at `http://localhost:8000` when started with Docker Compose. For local development outside Docker, install dependencies with `uv sync` and run the FastAPI application directly:

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
├── docker-compose.yml  # App, Postgres, and Redis services
├── Dockerfile          # FastAPI application image
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
