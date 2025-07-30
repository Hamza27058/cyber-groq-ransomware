from fastapi import FastAPI
from app.api.ask import router as ask_router
from app.api.ransomware import router as ransomware_router
app = FastAPI(
title="Cyber-Groq-Ransomware",
version="1.0.0",
description="FastAPI + GroqCloud + live ransomware intelligence",
)
app.include_router(ask_router)
@app.get("/health")
async def health():
  return {"status": "ok"}

app.include_router(ransomware_router)