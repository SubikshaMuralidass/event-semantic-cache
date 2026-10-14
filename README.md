# Event Semantic Cache

**A Redis-powered semantic caching layer for an event-based RAG question-answering system, built with FastAPI, Sentence Transformers, and Google Gemini.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-Vector%20Search-DC382D)](https://redis.io/)
[![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4)](https://ai.google.dev/)

## Overview

Repeated queries to an LLM-powered application can introduce unnecessary latency, token consumption, and API costs. Traditional exact-match caching handles identical requests but misses semantically equivalent questions.

**Event Semantic Cache** explores semantic caching for a retrieval-augmented generation (RAG) application. It uses vector similarity to identify previously answered questions and reuse cached responses when the similarity score meets a configured threshold.

The application answers questions about a fictional technology conference, TechConnect 2026, using event information stored in a local Markdown document.

### Key Features

- **Semantic caching:** Finds similar questions using vector embeddings and Redis vector search.
- **RAG pipeline:** Retrieves relevant event information to ground generated answers.
- **LLM integration:** Uses Google Gemini to generate context-grounded responses.
- **REST API:** Exposes the question-answering workflow through FastAPI.
- **Cache expiration:** Applies a configurable time-to-live (TTL) to cached answers.
- **Benchmarking:** Compares cache-hit and cache-miss latency using repeated questions.
- **Separation of concerns:** Maintains separate Redis vector indexes for document retrieval and semantic caching.


## Benchmark Results

Measured in a small, local sequential benchmark using four valid question pairs.

| Metric | Result |
|---|---:|
| Valid benchmark pairs | 4 |
| Average cache-miss latency | 3,794.32 ms |
| Median cache-miss latency | 2,097.11 ms |
| Average cache-hit latency | 10.59 ms |
| Median cache-hit latency | 10.39 ms |
| Average latency reduction | 99.72% |
| Average-latency speedup | 358.21× |
| Repeated answers matching | 4/4 (100%) |

**Note:** These are preliminary local measurements, not production performance guarantees. A semantic-cache correctness issue was also identified during testing, so matching repeated answers does not establish overall cache correctness.


## Architecture


                ┌──────────────────┐
                │      Client      │
                └────────┬─────────┘
                         ▼
                ┌──────────────────┐
                │  FastAPI /chat   │
                └────────┬─────────┘
                         ▼
                ┌──────────────────┐
                │ Query Embedding  │
                └────────┬─────────┘
                         ▼
                ┌──────────────────┐
                │ Redis Semantic   │
                │      Cache       │
                └────────┬─────────┘
                         ▼
                   ┌───────────┐
                   │ Cache Hit?│
                   └─────┬─────┘
                    Yes  │  No
                 ┌───────┘  └──────────┐
                 ▼                     ▼
       ┌─────────────────┐   ┌─────────────────┐
       │ Return Cached   │   │ Redis RAG Index │
       │ Answer          │   └────────┬────────┘
       └─────────────────┘            ▼
                             ┌─────────────────┐
                             │  Build Context  │
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │  Google Gemini  │
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Store Answer in │
                             │ Redis Cache     │
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │  Return Answer  │
                             └─────────────────┘


### Request Flow

1. The client submits a question to the `/chat` endpoint.
2. The application generates an embedding using `all-MiniLM-L6-v2`.
3. Redis searches the semantic cache for the closest matching question.
4. If the nearest result passes the configured similarity threshold, the cached answer is returned.
5. Otherwise, the RAG pipeline retrieves relevant event-document chunks from Redis.
6. The retrieved context and question are sent to Google Gemini.
7. The generated answer is stored in the semantic cache with a 24-hour TTL.
8. The API returns the answer and cache status.

**Important:** The current implementation uses embedding similarity and a threshold; it does not yet have a complete semantic-safety gate. Similarity alone cannot guarantee that two questions require the same answer.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| API framework | FastAPI |
| Vector database and cache | Redis Stack |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector dimensions | 384 |
| LLM | Google Gemini |
| LLM integration | Google Gen AI SDK |
| Numerical operations | NumPy |
| Configuration | Environment variables and `python-dotenv` |
| API testing | FastAPI Swagger UI and HTTP requests |

## Project Structure

```text
event-semantic-cache/
├── app/
│   ├── main.py                # FastAPI application and chat endpoint
│   ├── embeddings.py          # Query and document embeddings
│   ├── semantic_cache.py      # Semantic cache lookup and storage
│   ├── cache.py               # Cache-related utilities
│   ├── redis_client.py        # Redis connection utilities
│   ├── create_index.py        # Semantic cache vector index
│   ├── create_rag_index.py    # RAG document vector index
│   ├── document_loader.py     # Event document loading
│   ├── chunker.py             # Document chunking
│   ├── store_rag.py           # Store document chunks and embeddings
│   ├── rag_retriever.py       # Retrieve relevant document chunks
│   ├── context_builder.py     # Build context for the LLM
│   ├── llm.py                 # Gemini integration
│   ├── rag_pipeline.py        # RAG question-answering pipeline
│   └── vector_test.py         # Vector search testing
├── data/
│   └── event.md               # Sample event knowledge base
├── .env.example               # Environment configuration template
├── .gitignore
├── requirements.txt
└── README.md
```

*The tree describes the intended project layout. Keep only files that actually exist in the repository, and include `.env.example` only after creating it.*

## Prerequisites

- Python 3.11 or a compatible version for the installed dependencies.
- Docker Desktop.
- Redis Stack with the Redis Search/vector-search module.
- A Google Gemini API key.
- Git.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SubikshaMuralidass/event-semantic-cache.git
cd event-semantic-cache
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start Redis Stack

If you do not already have a Redis Stack container, you can create one:

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

Verify connectivity:

```bash
docker exec redis-stack redis-cli ping
```

Expected response:

```text
PONG
```

If a container named `redis-stack` already exists, start that container instead of creating a duplicate.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.1-flash-lite
```

Replace the placeholder with your own API key. Do not commit `.env` or expose your API key in source code, screenshots, logs, or public repositories.

### 6. Initialize the vector indexes and event data

Create the RAG index and semantic cache index, then populate the RAG index with event-document chunks. Use the following commands in the order appropriate for your initialization scripts:

```powershell
python -m app.create_rag_index
python -m app.create_index
python -m app.store_rag
```

Run each command from the project root. If the indexes already exist, follow the scripts' behavior before rerunning them.

The first embedding-model load may take longer because the model needs to be downloaded.

### 7. Start the API

```powershell
uvicorn app.main:app --reload
```

The application should be available at:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

## API Usage

### `POST /chat`

Submit a question about TechConnect 2026.

**Request**

```json
{
  "question": "What time does the Redis session start?"
}
```

**Example response — cache miss**

```json
{
  "answer": "The Redis session starts at 2:00 PM.",
  "cache": "MISS",
  "similarity_score": 0.515463829041
}
```

**Example response — cache hit**

```json
{
  "answer": "The Redis session starts at 2:00 PM.",
  "cache": "HIT",
  "similarity_score": 0.0
}
```

These are examples from local tests; actual scores and responses depend on the cache contents and query.

### Cache status

- `HIT`: A cached answer was reused.
- `MISS`: No acceptable cache entry was used, so the RAG and LLM pipeline ran.

The `similarity_score` is the Redis vector-search distance, not a percentage of confidence. For the configured cosine distance, lower values indicate closer vectors.

## Redis Index Design

The application uses separate vector indexes for two purposes.

### Semantic cache index — `semantic_cache_idx`

Stores previously answered questions, their answers, and their query embeddings.

- Key prefix: `cache:`
- Vector field: `embedding`
- Vector dimensions: 384
- Distance metric: cosine
- Configured similarity-distance threshold: `0.35`
- Cache TTL: 86,400 seconds (24 hours)

### RAG document index — `event_rag_idx`

Stores event-document chunks and their embeddings. The retriever searches this index for relevant context when a cached answer is not reused.

Separating these indexes allows the application to retrieve knowledge from the event document independently of retrieving previously generated answers.

## Benchmark Results

A local sequential benchmark compared cache misses against repeated cache hits using four valid question pairs.

| Metric | Observed result |
|---|---:|
| Valid benchmark pairs | 4 |
| Average cache-miss latency | 3,794.32 ms |
| Median cache-miss latency | 2,097.11 ms |
| Average cache-hit latency | 10.59 ms |
| Median cache-hit latency | 10.39 ms |
| Average-latency reduction | 99.72% |
| Average-latency speedup | 358.21× |
| Repeated answers matching | 4/4 |

### Interpretation

In this small local benchmark, cache hits were substantially faster than cache misses. Cache misses included retrieval, context preparation, and Gemini API latency, whereas cache hits avoided the RAG and LLM stages.

These measurements are preliminary observations, **not production performance guarantees**. The benchmark used only four valid pairs, ran locally, and included a cache-miss latency outlier of approximately 9.26 seconds. A larger benchmark is needed to measure p95/p99 latency, concurrency, sustained throughput, and real-world performance.

### Correctness limitations

During testing, the question *“What time does the Redis session end?”* incorrectly reused the answer *“The Redis session starts at 2:00 PM.”* This demonstrated that a low vector distance does not prove that the cached answer is appropriate.

The current implementation therefore needs additional correctness safeguards before it can be considered production-ready.

## Known Limitations

- Semantic similarity can produce false cache hits.
- The cache does not yet implement comprehensive intent, entity, negation, or answer-compatibility validation.
- The cache threshold is configurable but has not been optimized against a large labeled dataset.
- Embedding generation still runs on cache lookups, adding computational overhead.
- Gemini latency and availability affect cache-miss performance.
- The current benchmark is small and does not measure concurrent workloads.
- Production concerns such as authentication, rate limiting, distributed cache-stampede protection, comprehensive observability, and deployment hardening remain future work.

## Roadmap

- [x] Integrate Google Gemini with the RAG pipeline.
- [x] Create separate Redis vector indexes for RAG and semantic caching.
- [x] Expose question answering through FastAPI.
- [x] Add cache expiration.
- [x] Benchmark cache-hit versus cache-miss latency.
- [ ] Add precision-first cache validation inspired by GatedSemanticCache.
- [ ] Create a labeled correctness test set with safe paraphrases and adversarial near-misses.
- [ ] Evaluate cache thresholds using false-hit rate, precision, recall, and latency.
- [ ] Add cache and LLM observability, including hit rate and token usage.
- [ ] Test concurrent requests and cache-stampede behavior.
- [ ] Add production deployment, security, and reliability safeguards.

## Future Safety Improvements

The next iteration will explore a gated semantic-caching approach inspired by [GatedSemanticCache](https://github.com/mariadb-JagsR/gated-semantic-cache).

The intended design is to validate candidate cache entries before reusing their answers. Ambiguous or incompatible matches should fall back to the RAG and LLM pipeline rather than risk returning a misleading answer.

This is a planned improvement, not a feature currently implemented in this repository.

## Learning Outcomes

This project explores:

- Embedding-based semantic retrieval.
- Redis vector indexes and nearest-neighbor search.
- RAG architecture and context-grounded generation.
- REST API development with FastAPI.
- LLM integration and environment-based secret management.
- Latency benchmarking and cache effectiveness.
- Correctness risks in semantic caching.

---

**Author:** Subiksha Muralidass

**GitHub:** [SubikshaMuralidass](https://github.com/SubikshaMuralidass)
