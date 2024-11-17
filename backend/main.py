# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from inference import TheftDetector
import asyncio
from typing import Dict
import json
import socketio
from datetime import datetime
from database import Database
from camera_manager import CameraManager
from models import DvrCredentials, AlertData
import os
from dotenv import load_dotenv

load_dotenv()

# Define allowed origins
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server default port
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # In case you use a different port
    "*"  # Or any other origins you need
]

# Create the FastAPI app first
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO setup with explicit CORS configuration
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=ALLOWED_ORIGINS,  # Use the same origins here
    logger=True,
    engineio_logger=True
)

# Create the ASGI app
asgi_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)


# Global instances
detector = TheftDetector()
db = Database()
camera_manager = CameraManager()
dvr_config = {
    "ip": os.getenv('DVR_IP'),
    "username": os.getenv('DVR_USERNAME'),
    "password": os.getenv('DVR_PASSWORD')
}

@app.on_event("startup")
async def startup_event():
    await db.initialize()
    try:
        await camera_manager.initialize(
            dvr_config["ip"],
            dvr_config["username"],
            dvr_config["password"]
        )
    except Exception as e:
        print(f"Failed to initialize camera manager: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await camera_manager.close()

@app.post("/api/configure-dvr")
async def configure_dvr(credentials: DvrCredentials):
    try:
        await camera_manager.close()
        await camera_manager.initialize(
            credentials.ip,
            credentials.username,
            credentials.password
        )
        dvr_config.update({
            "ip": credentials.ip,
            "username": credentials.username,
            "password": credentials.password
        })
        cameras = await camera_manager.get_camera_list()
        return {
            "status": "success",
            "message": "DVR configured successfully",
            "cameras": cameras
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to configure DVR: {str(e)}"
        )

@app.get("/api/cameras")
async def get_cameras():
    try:
        cameras = await camera_manager.get_camera_list()
        return {"cameras": cameras}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get camera list: {str(e)}"
        )

@app.post("/api/analyze")
async def analyze_frame(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        results = detector.process_frame(frame)
        
        return {
            "status": "success",
            "data": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    try:
        cameras = await camera_manager.get_camera_list()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "detector": detector is not None,
                "database": db is not None,
                "cameras": len(cameras),
                "socketio": sio is not None,
                "dvr_configured": all([
                    dvr_config["ip"],
                    dvr_config["username"],
                    dvr_config["password"]
                ])
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_status', {'status': 'connected'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")