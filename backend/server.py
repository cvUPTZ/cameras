# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from main import asgi_app as app

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
   
    uvicorn.run(
        "main:asgi_app",
        host="0.0.0.0",
        port=8000,
        log_config=log_config,
        log_level="info",
        reload=True
    )