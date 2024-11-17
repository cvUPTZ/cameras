import asyncio
import aiohttp
import base64
import json
from typing import Dict, Optional
from datetime import datetime

class DahuaCamera:
    def __init__(self, ip: str, username: str, password: str, channel: int = 1):
        self.ip = ip
        self.username = username
        self.password = password
        self.channel = channel
        self.session: Optional[aiohttp.ClientSession] = None
        self.auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        
    async def connect(self):
        """Initialize connection to the camera"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers={
                "Authorization": f"Basic {self.auth}",
                "Content-Type": "application/json"
            })
        
    async def disconnect(self):
        """Close the camera connection"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def get_stream_url(self) -> str:
        """Get RTSP stream URL for the camera"""
        return f"rtsp://{self.username}:{self.password}@{self.ip}/cam/realmonitor?channel={self.channel}&subtype=0"
        
    async def get_snapshot(self) -> bytes:
        """Get a snapshot from the camera"""
        if not self.session:
            await self.connect()
            
        url = f"http://{self.ip}/cgi-bin/snapshot.cgi?channel={self.channel}"
        async with self.session.get(url) as response:
            return await response.read()
            
    async def get_status(self) -> dict:
        """Get camera status"""
        if not self.session:
            await self.connect()
            
        url = f"http://{self.ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
        async with self.session.get(url) as response:
            data = await response.text()
            return {item.split("=")[0]: item.split("=")[1] 
                   for item in data.strip().split("\n") if "=" in item}

class DahuaDVR:
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        self.cameras: Dict[int, DahuaCamera] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self):
        """Initialize connection to the DVR and discover cameras"""
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Basic {base64.b64encode(f'{self.username}:{self.password}'.encode()).decode()}",
            "Content-Type": "application/json"
        })
        
        # Get channel information
        url = f"http://{self.ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
        async with self.session.get(url) as response:
            data = await response.text()
            info = {item.split("=")[0]: item.split("=")[1] 
                   for item in data.strip().split("\n") if "=" in item}
            
            # Initialize cameras based on available channels
            for channel in range(1, int(info.get("ChannelNum", 1)) + 1):
                self.cameras[channel] = DahuaCamera(
                    self.ip,
                    self.username,
                    self.password,
                    channel
                )
                
    async def get_camera(self, channel: int) -> Optional[DahuaCamera]:
        """Get camera by channel number"""
        return self.cameras.get(channel)
        
    async def get_all_cameras(self) -> Dict[int, DahuaCamera]:
        """Get all available cameras"""
        return self.cameras
        
    async def close(self):
        """Close all connections"""
        for camera in self.cameras.values():
            await camera.disconnect()
            
        if self.session:
            await self.session.close()
            
class CameraManager:
    def __init__(self):
        self.dvr: Optional[DahuaDVR] = None
        self.active_streams: Dict[int, asyncio.Task] = {}
        
    async def initialize(self, dvr_ip: str, username: str, password: str):
        """Initialize the camera manager with DVR credentials"""
        self.dvr = DahuaDVR(dvr_ip, username, password)
        await self.dvr.initialize()
        
    async def get_camera_list(self) -> list:
        """Get list of all available cameras"""
        if not self.dvr:
            return []
            
        cameras = []
        for channel, camera in (await self.dvr.get_all_cameras()).items():
            status = await camera.get_status()
            cameras.append({
                "id": channel,
                "name": f"Camera {channel}",
                "status": "active" if status.get("deviceStatus") == "OK" else "inactive",
                "streamUrl": await camera.get_stream_url()
            })
        return cameras
        
    async def start_stream(self, channel: int) -> bool:
        """Start streaming from a specific camera"""
        if not self.dvr:
            return False
            
        camera = await self.dvr.get_camera(channel)
        if not camera:
            return False
            
        await camera.connect()
        return True
        
    async def stop_stream(self, channel: int) -> bool:
        """Stop streaming from a specific camera"""
        if not self.dvr:
            return False
            
        camera = await self.dvr.get_camera(channel)
        if not camera:
            return False
            
        await camera.disconnect()
        return True
        
    async def get_snapshot(self, channel: int) -> Optional[bytes]:
        """Get a snapshot from a specific camera"""
        if not self.dvr:
            return None
            
        camera = await self.dvr.get_camera(channel)
        if not camera:
            return None
            
        return await camera.get_snapshot()
        
    async def close(self):
        """Close all connections"""
        if self.dvr:
            await self.dvr.close()