from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import uuid
import asyncio
import threading
from queue import PriorityQueue
import time
from datetime import datetime
from typing import List, Dict, Optional

app = FastAPI()

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestionRequest(BaseModel):
    ids: List[int]
    priority: Priority = Priority.MEDIUM

class BatchStatus(str, Enum):
    YET_TO_START = "yet_to_start"
    TRIGGERED = "triggered"
    COMPLETED = "completed"

class BatchInfo(BaseModel):
    batch_id: str
    ids: List[int]
    status: BatchStatus

class IngestionStatus(BaseModel):
    ingestion_id: str
    status: str
    batches: List[BatchInfo]

ingestion_requests = {}
batch_queue = PriorityQueue()
current_batches = {}
lock = threading.Lock()
last_batch_time = 0

PRIORITY_WEIGHTS = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

async def process_batch(batch_id: str, ids: List[int]):
    with lock:
        current_batches[batch_id]["status"] = BatchStatus.TRIGGERED
    await asyncio.sleep(5)
    with lock:
        current_batches[batch_id]["status"] = BatchStatus.COMPLETED

async def batch_processor():
    global last_batch_time
    while True:
        if not batch_queue.empty():
            current_time = time.time()
            if current_time - last_batch_time >= 5:
                _, (_, batch_id, ids) = batch_queue.get()
                asyncio.create_task(process_batch(batch_id, ids))
                last_batch_time = current_time
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(batch_processor())

@app.post("/ingest")
async def ingest_data(request: IngestionRequest):
    ingestion_id = str(uuid.uuid4())
    batches = []
    for i in range(0, len(request.ids), 3):
        batch_ids = request.ids[i:i+3]
        batch_id = str(uuid.uuid4())
        batches.append(BatchInfo(
            batch_id=batch_id,
            ids=batch_ids,
            status=BatchStatus.YET_TO_START
        ))
        priority_weight = PRIORITY_WEIGHTS[request.priority]
        batch_queue.put((priority_weight, (ingestion_id, batch_id, batch_ids)))
    with lock:
        ingestion_requests[ingestion_id] = {
            "batches": batches,
            "priority": request.priority
        }
        for batch in batches:
            current_batches[batch.batch_id] = batch
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
async def get_status(ingestion_id: str):
    if ingestion_id not in ingestion_requests:
        raise HTTPException(status_code=404, detail="Not found")
    batches = ingestion_requests[ingestion_id]["batches"]
    status = "triggered"
    return {
        "ingestion_id": ingestion_id,
        "status": status,
        "batches": batches
    }

if __name__ == "__main__":
    import uvicorn
