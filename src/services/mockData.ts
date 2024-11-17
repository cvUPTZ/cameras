import { Alert, Camera, Stat } from '../types';
import { Eye, AlertTriangle, Activity, Database } from 'lucide-react';

export const mockCameras: Camera[] = [
  { id: 1, name: 'Main Entrance', status: 'active', streamUrl: 'https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&q=80' },
  { id: 2, name: 'Storage Area', status: 'active', streamUrl: 'https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&q=80' },
  { id: 3, name: 'Back Door', status: 'active', streamUrl: 'https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&q=80' },
  { id: 4, name: 'Parking Lot', status: 'inactive', streamUrl: 'https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&q=80' },
];

export const mockAlerts: Alert[] = [
  { id: 1, time: new Date().toLocaleTimeString(), type: 'Motion Detected', camera: 'Camera 2', severity: 'high' },
  { id: 2, time: new Date().toLocaleTimeString(), type: 'Object Removed', camera: 'Camera 1', severity: 'medium' },
  { id: 3, time: new Date().toLocaleTimeString(), type: 'Suspicious Activity', camera: 'Camera 3', severity: 'low' },
];

export const mockStats: Stat[] = [
  { label: 'Detections Today', value: '157', icon: Eye },
  { label: 'Active Alerts', value: '3', icon: AlertTriangle },
  { label: 'System Health', value: '98%', icon: Activity },
  { label: 'Storage Used', value: '64%', icon: Database },
];