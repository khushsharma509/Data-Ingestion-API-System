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
