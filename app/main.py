
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CI/CD Security Lab"}

@app.get("/health")
def health():
    return {"status": "healthy"}
