# 📥 Data-Ingestion-API-System

A FastAPI-based service to ingest data IDs with priority, split them into batches, and track ingestion status.

---

## 🚀 Features

- Accepts data with `HIGH`, `MEDIUM`, `LOW` priority
- Splits IDs into batches
- Tracks ingestion and batch status via UUIDs
- Thread-safe processing using `PriorityQueue`

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 5000  


for test file:
python -m pytest test.py -v
```
# Example Curl 

```bash 
curl -X POST http://localhost:5000/ingest `
>>   -H "Content-Type: application/json" `
>>   -d '{"ids": [1,2,3,4,5], "priority": "HIGH"}'
>> 
{"ingestion_id":"69d6688d-a931-4d71-9973-939b27e2002a"}


curl http://localhost:5000/status/69d6688d-a931-4d71-9973-939b27e2002a
{"ingestion_id":"69d6688d-a931-4d71-9973-939b27e2002a","status":"triggered","batches":[{"batch_id":"4e8e2810-13e1-459e-bd9e-65403ee9db3d","ids":[1,2,3],"status":"yet_to_start"},{"batch_id":"e003c21a-0985-4fda-ab13-9595276ef5ea","ids":[4,5],"status":"yet_to_start"}]}
