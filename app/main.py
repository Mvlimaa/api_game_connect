from fastapi import FastAPI

app = FastAPI(title="API Game Connect", version="1.0")

@app.get("/")
def root():
    return {"message": "API Game Connect Online!"}
