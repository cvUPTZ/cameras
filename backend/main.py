#main.py
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
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class DvrConfig(BaseModel):
    ip: str
    username: str
    password: str

# Create FastAPI app
app = FastAPI()

# Configure CORS for FastAPI first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Socket.IO
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['*'],
    logger=True,
    engineio_logger=True
)

# Create ASGI app by wrapping the FastAPI app
asgi_app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=app
)
# Initialize components
detector = TheftDetector()
db = Database()
camera_manager = CameraManager()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    await db.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await camera_manager.close()

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_status', {'status': 'connected'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@app.post("/dvr/configure")
async def configure_dvr(config: DvrConfig):
    try:
        await camera_manager.initialize(config.ip, config.username, config.password)
        return {"status": "success", "connected": True, "message": "DVR configured successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alerts")
async def get_alerts():
    alerts = await db.get_recent_alerts()
    return {"alerts": alerts}

@app.get("/cameras")
async def get_cameras():
    cameras = await camera_manager.get_camera_list()
    return {"cameras": cameras}

@app.post("/analyze")
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
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/socket-health")
async def socket_health():
    return {
        "status": "healthy",
        "socket_connected": True,
        "timestamp": datetime.now().isoformat()
    }
    
    
@app.get("/stream/{camera_id}/start")
async def start_stream(camera_id: int):
    success = await camera_manager.start_stream(camera_id)
    if success:
        return {"status": "success", "message": "Stream started"}
    return {"status": "error", "message": "Failed to start stream"}

@app.get("/stream/{camera_id}/stop")
async def stop_stream(camera_id: int):
    success = await camera_manager.stop_stream(camera_id)
    if success:
        return {"status": "success", "message": "Stream stopped"}
    return {"status": "error", "message": "Failed to stop stream"}

@app.get("/camera/{camera_id}/snapshot")
async def get_snapshot(camera_id: int):
    snapshot = await camera_manager.get_snapshot(camera_id)
    if snapshot:
        return {"status": "success", "data": snapshot}
    return {"status": "error", "message": "Failed to get snapshot"}

@app.get("/health")
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
                "socketio": sio is not None
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }