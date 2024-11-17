# import sqlite3
# import os
# from datetime import datetime
# from dotenv import load_dotenv

# load_dotenv()

# class Database:
#     def __init__(self):
#         self.db_path = "theft-detection.db"
#         self.conn = sqlite3.connect(self.db_path)
#         self.conn.row_factory = sqlite3.Row  # This makes rows accessible by column name

#     async def initialize(self):
#         """Initialize the database by creating required tables"""
#         await self.setup_database()

#     async def setup_database(self):
#         """Set up database tables if they don't exist"""
#         cursor = self.conn.cursor()
        
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS alerts (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 type TEXT NOT NULL,
#                 camera TEXT NOT NULL,
#                 severity TEXT NOT NULL
#             )
#         """)
        
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS cameras (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 status TEXT NOT NULL,
#                 stream_url TEXT
#             )
#         """)
        
#         self.conn.commit()

#     async def add_alert(self, alert_type: str, camera: str, severity: str):
#         """Add a new alert to the database"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             INSERT INTO alerts (type, camera, severity)
#             VALUES (?, ?, ?)
#         """, (alert_type, camera, severity))
#         self.conn.commit()

#     async def get_recent_alerts(self, limit: int = 10):
#         """Get the most recent alerts"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             SELECT * FROM alerts
#             ORDER BY time DESC
#             LIMIT ?
#         """, (limit,))
#         return cursor.fetchall()

#     async def add_camera(self, name: str, status: str, stream_url: str = None):
#         """Add a new camera to the database"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             INSERT INTO cameras (name, status, stream_url)
#             VALUES (?, ?, ?)
#         """, (name, status, stream_url))
#         self.conn.commit()

#     async def get_cameras(self):
#         """Get all cameras"""
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM cameras")
#         return cursor.fetchall()

#     async def update_camera_status(self, camera_id: int, status: str):
#         """Update camera status"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             UPDATE cameras
#             SET status = ?
#             WHERE id = ?
#         """, (status, camera_id))
#         self.conn.commit()

#     async def delete_camera(self, camera_id: int):
#         """Delete a camera"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             DELETE FROM cameras
#             WHERE id = ?
#         """, (camera_id,))
#         self.conn.commit()

#     async def clear_old_alerts(self, days: int = 30):
#         """Clear alerts older than specified days"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             DELETE FROM alerts
#             WHERE time < datetime('now', '-? days')
#         """, (days,))
#         self.conn.commit()

#     async def get_alerts_by_camera(self, camera: str, limit: int = 10):
#         """Get alerts for a specific camera"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             SELECT * FROM alerts
#             WHERE camera = ?
#             ORDER BY time DESC
#             LIMIT ?
#         """, (camera, limit))
#         return cursor.fetchall()

#     async def get_alerts_by_severity(self, severity: str, limit: int = 10):
#         """Get alerts by severity level"""
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             SELECT * FROM alerts
#             WHERE severity = ?
#             ORDER BY time DESC
#             LIMIT ?
#         """, (severity, limit))
#         return cursor.fetchall()

#     def __del__(self):
#         """Cleanup database connection when object is destroyed"""
#         if hasattr(self, 'conn'):
#             self.conn.close()











# database.py
import aiosqlite
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "security.db"):
        self.db_path = db_path

    async def initialize(self):
        """Initialize the database with required tables"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cameras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    stream_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    camera TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()

    async def add_camera(self, name: str, status: str, stream_url: str = None):
        """Add a new camera to the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO cameras (name, status, stream_url) VALUES (?, ?, ?)",
                (name, status, stream_url)
            )
            await db.commit()

    async def delete_camera(self, camera_id: int):
        """Delete a camera from the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cameras WHERE id = ?", (camera_id,))
            await db.commit()

    async def update_camera_status(self, camera_id: int, status: str):
        """Update the status of a camera"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE cameras SET status = ? WHERE id = ?",
                (status, camera_id)
            )
            await db.commit()

    async def get_cameras(self):
        """Get all cameras from the database"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM cameras ORDER BY created_at DESC") as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def add_alert(self, alert_type: str, camera: str, severity: str):
        """Add a new alert to the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO alerts (type, camera, severity) VALUES (?, ?, ?)",
                (alert_type, camera, severity)
            )
            await db.commit()

    async def get_recent_alerts(self, limit: int = 100):
        """Get recent alerts from the database"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
