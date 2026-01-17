from fastapi import FastAPI
import uvicorn
from App.routes import document

app = FastAPI(title="AI Assistant Chatbot API")

app.include_router(document.router)

@app.get("/")
async def root():
    return {"message": "AI Assistant API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)