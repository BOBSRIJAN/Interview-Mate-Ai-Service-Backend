# Livekit Session Manager (InterviewMateAiServiceBackend)

A FastAPI service that manages **LiveKit session token generation** and coordinates session events through **Kafka** while caching session data in **Redis**.

> The app boots Kafka consumers/producers during FastAPI startup (`lifespan`), listens for incoming user/agent events, generates LiveKit access tokens, publishes results back to Kafka, and writes session results into Redis.

---

## Project Folder Structure

```text
LivekitSessionManager/
├─ Dockerfile
└─ app/
   ├─ __init__.py
   ├─ main.py
   ├─ BrokerUnit/
   │  ├─ __init__.py
   │  ├─ brokerConfig.py
   │  └─ brokerMethods.py
   ├─ CacheUnit/
   │  ├─ __init__.py
   │  ├─ cacheConfig.py
   │  └─ cacheMethods.py
   ├─ Components/
   │  ├─ __init__.py
   │  ├─ AgentSession.py
   │  └─ UserSession.py
   ├─ Config/
   │  ├─ __init__.py
   │  └─ envConfig.py
   ├─ Resources/
   │  └─ banner.txt
   ├─ Routers/
   │  ├─ __init__.py
   │  ├─ controller.py
   │  └─ route.py
   ├─ Schemas/
   │  ├─ __init__.py
   │  └─ Validator.py
   └─ Services/
      ├─ __init__.py
      ├─ Hendler.py
      └─ Worker.py
```

---

## Key Design / Code Highlights (Good Parts)

### 1) FastAPI `lifespan` lifecycle controls Kafka + Redis
**File:** `app/main.py`

- Uses an `@asynccontextmanager` lifespan to perform all startup/shutdown orchestration.
- On startup:
  - Prints the startup banner from `app/Resources/banner.txt`.
  - Initializes Redis client.
  - Initializes:
    - Kafka consumer for **user** topic
    - Kafka consumer for **agent** topic
    - Kafka producer
  - Spawns two background tasks:
    - `Workers.userWorker()`
    - `Workers.agentWorker()`
- On shutdown:
  - Cancels worker tasks
  - Stops Kafka consumers
  - Flushes/stops Kafka producer
  - Closes Redis connection

This keeps infrastructure wiring inside one place and avoids “startup code spread across modules”.

### 2) Clean separation of concerns
The code is split into focused modules:
- `BrokerUnit/`: Kafka configuration + message production + shutdown helpers
- `CacheUnit/`: Redis initialization + shutdown
- `Components/`: Pure session generation logic (LiveKit tokens)
- `Services/`:
  - `Worker.py` runs consumer loops
  - `Hendler.py` validates/handles events and triggers session generation + publishing
- `Routers/`: HTTP endpoints (currently system status)
- `Schemas/`: Pydantic request/response models
- `Config/`: environment variable loading

### 3) Pydantic validation for Kafka payloads
**File:** `app/Schemas/Validator.py`

- Defines request/response models:
  - `UserSessionRequest` (expects: `userid`, optional `topics`, optional `paragraph`, `duration`)
  - `UserSessionResponce` (sends back: `roomname`, `token`, `livekiturl`)
  - `AgentSessionRequest` (expects: `roomname`)
  - `AgentSessionResponce` (sends back: `roomname`, `token`, `livekiturl`)
  - `SystemStatusResponce`

In `app/Services/Hendler.py`, payloads are validated with `model_validate(...)`. If validation fails, the handler publishes to the appropriate error Kafka topic and logs the exception.

### 4) LiveKit token generation is encapsulated
**Files:**
- `app/Components/UserSession.py`
- `app/Components/AgentSession.py`

Both functions create an `AccessToken` with `VideoGrants(room_join=True, can_publish=True, can_subscribe=True, room=...)`.

- **User token**:
  - Room: `Imate-room-{uuid4}`
  - Identity: `req.userid`
  - Name: `req.userid`
- **Agent token**:
  - Identity: `agent-{uuid4}`
  - Room: provided roomname from the event
  - Name: `Agent`

This ensures session logic stays consistent and reusable.

### 5) Kafka event flow is explicit
**Files:**
- `app/BrokerUnit/brokerConfig.py`
- `app/Services/Worker.py`
- `app/Services/Hendler.py`

Flow:
1. `Workers.userWorker()` consumes Kafka events from the configured **user** topic.
2. For each message:
   - Spawns `Hendlers.userEventHendler(...)`
   - Commits offsets after processing loop iteration
3. `Hendlers.userEventHendler(...)`:
   - Validates the event payload via `UserSessionRequest`
   - Generates LiveKit session via `createUserSession`
   - Publishes to `room.info.user`
   - Stores session result in Redis under key = `userid`
4. `Workers.agentWorker()` and `agentEventHendler` mirror the same behavior for agents.

**Kafka error topics used in the code**:
- `val.error.user`
- `val.error.agent`

**Kafka success topics used in the code**:
- `room.info.user`
- `room.info.agent`

### 6) Redis caching of generated session results
**Files:**
- `app/CacheUnit/cacheConfig.py`
- `app/Services/Hendler.py`

- Redis is initialized in `CacheConf.initRedis()`.
- After user session generation, the handler does:
  - `redis.set(name=userData.userid, value=json.dumps(res), exat=900)`

This makes user session retrieval fast for consumers that need it.

---

## HTTP API

### Base Router
**File:** `app/Routers/route.py`

Router prefix:
- `/api/v1/livekitsessionmanager`

### Endpoints
#### `GET /api/v1/livekitsessionmanager/systemstatus`
**File:** `app/Routers/controller.py`

Returns a simple runtime health snapshot:
- CPU percent
- Memory RSS in MB
- Thread count

Uses `psutil` + current PID.

---

## Configuration (Environment Variables)

**File:** `app/Config/envConfig.py`

The app loads environment variables via `python-dotenv` (`load_dotenv()`).

Required/used variables:
- `CONSUMER_TOPIC_USER`
- `CONSUMER_TOPIC_AGENT`
- `KAFKA_BROKER_URL`
- `REDIS_HOST`
- `REDIS_PORT`
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `GLOBAL_HOST`

CORS configuration uses:
- `http://localhost:5173`
- `GLOBAL_HOST`

---

## Running the Service

### Option A: Run with Docker
1. Build:

```bash
docker build -t livekit-session-manager .
```

2. Run (example):

```bash
docker run --rm -p 8000:8000 \
  -e CONSUMER_TOPIC_USER="..." \
  -e CONSUMER_TOPIC_AGENT="..." \
  -e KAFKA_BROKER_URL="..." \
  -e REDIS_HOST="..." \
  -e REDIS_PORT="..." \
  -e LIVEKIT_URL="..." \
  -e LIVEKIT_API_KEY="..." \
  -e LIVEKIT_API_SECRET="..." \
  -e GLOBAL_HOST="..." \
  livekit-session-manager
```

3. App starts using:
- `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Option B: Run locally (Python)
1. Install dependencies (ensure you have the project’s `requirements.txt` present in the root):

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Notes on Operational Behavior

- The Kafka consumers are created during FastAPI startup, so the service should be started only when Kafka + Redis are reachable.
- The handler functions are launched as background tasks from the consumer loop.
- Shutdown attempts to stop background workers and flush/stop Kafka/Redis cleanly.

---

## Non-Public / Internal Use Only

This project is **not** intended for public use. Do not distribute or publish this codebase (including documentation, configuration patterns, or infrastructure details) outside the intended internal/private environment.