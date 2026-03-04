# Multi-Agent Digest System
A containerized, sequential multi-agent pipeline built with Python and Docker to transform digital noise into a structured daily brief.

## Architecture
The system employs a sequential pipeline pattern. Instead of a single "God Model" handling everything, four specialized agents perform discrete tasks, passing data via a shared Docker volume.

- **Ingestor Agent:** Scans /data/input, aggregates raw text files, and generates ingested.txt. (No LLM)

- **Summarizer Agent:** Processes the ingested text using OpenAI's gpt-4o-mini to extract key insights into summary.txt. (LLM-powered)

- **Prioritizer Agent:** Filters and scores bullet points based on urgency keywords, producing prioritized.txt. (No LLM)

- **Formatter Agent:** Converts the prioritized data into a clean Markdown report at /output/daily_digest.md. (No LLM)

## Project Structure
```
├── agents/
│   ├── ingestor/    # Aggregates input files
│   ├── summarizer/  # LLM-based summarization
│   ├── prioritizer/ # Keyword-based scoring
│   └── formatter/   # Markdown generation
├── data/            # Shared volume for intermediate files
├── output/          # Final daily_digest.md location
├── .env             # Environment variables (OPENAI_API_KEY)
└── docker-compose.yml
```
### Prerequisites
- Docker & Docker Compose V2
- Python 3.10+ (for local development/testing)
- Gemini API Key

## Setup & Execution
Clone the repository and navigate to the root.

## Configure Environment:
Create a .env file in the root directory:

```
GEMINI_KEY=your_sk_key_here
```

## Add Input Data:
Place any .txt or raw data files into the data/input/ directory.

## Run the Pipeline:
Execute the entire workflow:

```
docker compose up --build
```

### Technical Highlights
- **Separation of Concerns:** Each agent is a minimal Python environment. You can swap the Summarizer's LLM without touching the Ingestor's logic.

- **Reliability:** Uses depends_on with condition: service_completed_successfully in Docker Compose to ensure strict execution order.

- **Efficiency:** Only one agent uses an LLM. The rest are deterministic Python scripts, reducing cost and latency.

- **Portability:** Docker ensures the "it works on my machine" guarantee by packaging all dependencies and OS layers.

