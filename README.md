## Autonomous AI Market Intelligence System  

A comprehensive cryptocurrency system that combines real-time financial data with AI-powered analysis. Built with FastAPI, Postgres and LangChain. 
This application provides endpoints for market data and leverages Google's Gemini models to generate intelligent market insights.

## 🚀 Features

- **AI Market Analysis**: Uses a ReAct agent powered by Gemini to answer complex user queries about the market.
- **Real-time Data**: Fetches current cryptocurrency prices and intraday data.
- **Market Sentiment**: Tracks the Fear & Greed Index to gauge market sentiment.
- **News Aggregation**: Retrieves the latest cryptocurrency news.
- **Structured Output**: The AI agent returns structured data for consistent integration.
- **Observability**: Integrated with Langfuse for LLM trace monitoring.

## 📂 Project Structure

# correct this structure

```
  trading-bot/
  ├── agent/                 # AI Agent logic
  │   ├── prompts/           # System prompt for the agent
  │   ├── schemas/           # Data schemas for agent tools
  │   ├── tools/             # Tools available to the Agent
  │   └── utils/             # Utility functions for the agent
  ├── app/                   # FastAPI application
  │   ├── api/               # Route handlers for the API endpoints
  │   ├── clients/           # API clients for external services
  │   ├── data/              # Data files and data validation scripts
  │   ├── database/          # Database configuration, models, and lifespan events
  │   ├── repositories/      # Data access layer for interacting with the database
  │   ├── schemas/           # Data validation schemas (Pydantic models)
  │   ├── services/          # Business logic and service layer
  │   └── utils/             # General utility functions
  ├── docker-compose.yml     # Local development orchestration
  ├── Dockerfile             # Container definition for the application
  ├── migrations/            # SQL migrations for database schema changes
  ├── pyproject.toml         # Python project dependencies and metadata
  ├── tests/                 # Unit and integration tests
  └── uv.lock                # UV dependency lock file
```

## 🏗 Architecture

The project is structured into two main components:

1.  **`app/` (Web Layer)**: A FastAPI application that serves REST endpoints. It handles request validation, database interactions, and routing.
2.  **`agent/` (AI Layer)**: A LangChain-based module containing the logic for the AI agent, tools, and prompts.

### Tech Stack

- **Language**: Python 3.13
- **Web Framework**: FastAPI
- **AI/LLM**: LangChain, Google Gemini 
- **Database**: PostgreSQL
- **Data Sources**: yfinance, Alternative.me (Fear & Greed), AlphaVantage
- **Observability**: Langfuse
- **Deployment**: Google Cloud Platform (Cloud Build, CloudSQL, Artifact Registry), Docker

### Layers

- **API Layer**: `app/api` - Defines HTTP endpoints.
- **Service/Repository Layer**: `app/services`, `app/repositories` - Business logic and data access.
- **Agent Tools**: `agent/tools` - Specific functions (fetching prices, news) exposed to the LLM.

## 🛠 Installation & Setup

### Prerequisites

- Docker 
- Python 3.13+ 

### Local Development (Docker)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/koliush17/TradeIt    
    cd trading-bot
    ```

2.  **Configure Environment Variables:**
    Copy the example environment file and fill in the details.
    ```bash
    cp .env.example .env
    ```
    *   `GEMINI_API_KEY`: Your Google AI API key.
    *   `POSTGRES_...`: Database credentials (defaults provided in `docker-compose.yml` work out of the box).
        `CRYPTO_API_KEY`: AlphaVantage free API key.
    *   `LANGFUSE_...`: For tracing AI calls.

3.  **Run with Docker Compose:**
    This will start the FastAPI backend and a PostgreSQL database.
    ```bash
    docker-compose up --build
    ```

4.  **Access the API:**
    - API URL: `http://localhost:8080`
    - Interactive Docs (Swagger): `http://localhost:8080/docs`

## 📖 Usage

### AI Analysis Endpoint
**POST** `/analyze`
Analyze the market or ask questions about specific coins.

**Query Parameter:** `query` (string) - e.g., "What is the current sentiment for Bitcoin and should I worry about recent news?"

**Response:**
```json
{
  "summary": "Bitcoin is currently trading at...",
  "signal": "Hold",
  "score": "0 to 1",
  "confidence": "LOW, MEDIUM or HIGH"
}
```

### Data Endpoints
- **GET** `/prices/intraday/{symbol}`: Get intraday price data.
- **GET** `/fear-greed`: Get the current Fear & Greed index.
- **GET** `/news`: Fetch latest crypto news.
