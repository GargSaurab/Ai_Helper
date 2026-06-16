from fastapi import FastAPI
import uvicorn

from app.api.api_router import api_router

app = FastAPI(
    title="CodingHelperAI",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
