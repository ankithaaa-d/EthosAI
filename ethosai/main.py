import time
import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

# ── Logging Setup ───────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ethosai.api")

app = FastAPI(
    title="EthosAI — AI Middleware",
    description="""
    EthosAI acts as an intelligent middleware between AI agents and the web.
    It provides ethical evaluation, compliance scoring, and automated policy analysis.
    """,
    version="1.1.0",
    contact={
        "name": "EthosAI Support",
        "url": "https://ethosai.com",
    }
)

# ── Middleware ──────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from collections import defaultdict

# ── Rate Limiting ────────────────────────────────────────
# Simple in-memory rate limiter: 60 requests per minute per IP
RATE_LIMIT = 60 
RATE_LIMIT_WINDOW = 60 # seconds
request_counts = defaultdict(list)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    # Filter out requests outside the window
    request_counts[client_ip] = [t for t in request_counts[client_ip] if now - t < RATE_LIMIT_WINDOW]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        return Response(content="Rate limit exceeded", status_code=429)
    
    request_counts[client_ip].append(now)
    return await call_next(request)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}ms".format(process_time)
    
    logger.info(f"RID: {request.scope.get('root_path')} | Path: {request.url.path} | Time: {formatted_process_time} | Status: {response.status_code}")
    
    return response

# ── Register API routes ─────────────────────────────────
app.include_router(router)