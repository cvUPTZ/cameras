#inference.py
from roboflow import Roboflow
import cv2
import numpy as np
from config import (
    ROBOFLOW_API_KEY,
    MODEL_WORKSPACE,
    MODEL_NAME,
    MODEL_VERSION,
    CONFIDENCE_THRESHOLD,
    OVERLAP_THRESHOLD
)

class TheftDetector:
    def __init__(self):
        rf = Roboflow(api_key=ROBOFLOW_API_KEY)
        self.model = rf.workspace(MODEL_WORKSPACE).project(MODEL_NAME).version(MODEL_VERSION).model
        
        # Initialize object tracking - using KCF tracker instead of CSRT
        self.tracked_objects = {}
        self.last_frame = None
        
    def preprocess_frame(self, frame):
        """Preprocess frame before inference"""
        if frame is None:
            return None
            
        # Convert to RGB if needed
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            
        return frame
        
    def detect_objects(self, frame):
        """Perform object detection on a frame"""
        frame = self.preprocess_frame(frame)
        if frame is None:
            return []
            
        # Get predictions from Roboflow model
        predictions = self.model.predict(frame, confidence=CONFIDENCE_THRESHOLD, overlap=OVERLAP_THRESHOLD)
        
        # Convert predictions to a standardized format
        detections = []
        for pred in predictions:
            detection = {
                'class': pred['class'],
                'confidence': pred['confidence'],
                'bbox': {
                    'x': pred['x'],
                    'y': pred['y'],
                    'width': pred['width'],
                    'height': pred['height']
                }
            }
            detections.append(detection)
            
        return detections
        
    def track_objects(self, frame, detections):
        """Track detected objects across frames using KCF tracker"""
        current_objects = {}
        
        # Initialize tracking for new objects
        for detection in detections:
            bbox = detection['bbox']
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            
            # Create tracker for each object
            tracker = cv2.legacy.TrackerKCF_create()
            tracker.init(frame, (int(x), int(y), int(w), int(h)))
            
            object_id = len(self.tracked_objects)
            current_objects[object_id] = {
                'tracker': tracker,
                'class': detection['class'],
                'bbox': bbox,
                'confidence': detection['confidence']
            }
            
        # Update existing trackers
        for obj_id, obj_info in self.tracked_objects.items():
            success, bbox = obj_info['tracker'].update(frame)
            if success:
                current_objects[obj_id] = obj_info
                current_objects[obj_id]['bbox'] = {
                    'x': float(bbox[0]),
                    'y': float(bbox[1]),
                    'width': float(bbox[2]),
                    'height': float(bbox[3])
                }
                
        self.tracked_objects = current_objects
        return current_objects
        
    def analyze_movement(self, current_objects):
        """Analyze object movement patterns for suspicious activity"""
        suspicious_activities = []
        
        for obj_id, obj_info in current_objects.items():
            # Check for rapid movement
            if obj_id in self.tracked_objects:
                prev_bbox = self.tracked_objects[obj_id]['bbox']
                curr_bbox = obj_info['bbox']
                
                # Calculate displacement
                dx = curr_bbox['x'] - prev_bbox['x']
                dy = curr_bbox['y'] - prev_bbox['y']
                displacement = np.sqrt(dx*dx + dy*dy)
                
                # Define suspicious movement threshold
                if displacement > 50:  # Adjust threshold as needed
                    suspicious_activities.append({
                        'object_id': obj_id,
                        'type': 'rapid_movement',
                        'confidence': obj_info['confidence']
                    })
                    
        return suspicious_activities
        
    def process_frame(self, frame):
        """Process a single frame for theft detection"""
        # Detect objects
        detections = self.detect_objects(frame)
        
        # Track objects
        tracked_objects = self.track_objects(frame, detections)
        
        # Analyze movements
        suspicious_activities = self.analyze_movement(tracked_objects)
        
        # Store frame for next iteration
        self.last_frame = frame
        
        return {
            'detections': detections,
            'tracked_objects': tracked_objects,
            'suspicious_activities': suspicious_activities
        }