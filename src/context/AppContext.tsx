import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { Alert, Camera, Stat } from '../types';
import { checkHealth, startCameraStream, stopCameraStream } from '../services/api';
import { mockCameras, mockStats } from '../services/mockData';
import { config } from '../config';
import { io, Socket } from 'socket.io-client';

interface DvrConfig {
  ip: string;
  username: string;
  password: string;
}

interface AppContextType {
  selectedCamera: number;
  setSelectedCamera: (id: number) => void;
  alerts: Alert[];
  cameras: Camera[];
  stats: Stat[];
  systemHealth: boolean;
  isLoading: boolean;
  socketConnected: boolean;
  dvrConnected: boolean;
  updateDvrConfig: (config: DvrConfig) => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [selectedCamera, setSelectedCamera] = useState<number>(1);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [cameras] = useState<Camera[]>(mockCameras);
  const [stats] = useState<Stat[]>(mockStats);
  const [systemHealth, setSystemHealth] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [socketConnected, setSocketConnected] = useState(false);
  const [dvrConnected, setDvrConnected] = useState(false);
  const [socket, setSocket] = useState<Socket | null>(null);

  const updateDvrConfig = async (dvrConfig: DvrConfig) => {
    try {
      const response = await fetch(`${config.API_URL}/dvr/configure`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dvrConfig),
      });

      if (!response.ok) {
        throw new Error('Failed to update DVR configuration');
      }

      const data = await response.json();
      setDvrConnected(data.connected);
      return data;
    } catch (error) {
      console.error('Error updating DVR config:', error);
      setDvrConnected(false);
      throw error;
    }
  };

  // Initialize Socket.IO connection
  useEffect(() => {
    let retryCount = 0;
    const maxRetries = 5;
    const retryDelay = 5000;

    const connectSocket = () => {
      try {
        const newSocket = io(config.API_URL, {
          transports: ['websocket', 'polling'],  // Allow fallback to polling
          path: '/socket.io/',
          reconnectionAttempts: maxRetries,
          reconnectionDelay: retryDelay,
          autoConnect: true,
          timeout: 10000,
          withCredentials: true  // Add this
        });

        newSocket.on('connect', () => {
          console.log('Socket.IO connected');
          setSocketConnected(true);
          retryCount = 0;
        });

        newSocket.on('disconnect', () => {
          console.log('Socket.IO disconnected');
          setSocketConnected(false);
        });

        newSocket.on('connect_error', (error) => {
          console.error('Socket.IO connection error:', error);
          setSocketConnected(false);
          
          if (retryCount < maxRetries) {
            retryCount++;
            setTimeout(connectSocket, retryDelay);
          }
        });

        newSocket.on('connection_status', (data) => {
          console.log('Connection status:', data);
        });

        newSocket.on('alert', (data) => {
          if (data.type === 'alert') {
            setAlerts(prev => [data.alert, ...prev].slice(0, 10));
          }
        });

        setSocket(newSocket);

        return newSocket;
      } catch (error) {
        console.error('Socket initialization error:', error);
        if (retryCount < maxRetries) {
          retryCount++;
          setTimeout(connectSocket, retryDelay);
        }
        return null;
      }
    };

    const newSocket = connectSocket();

    return () => {
      if (newSocket) {
        newSocket.disconnect();
      }
      setSocket(null);
    };
  }, []);

  // Check system health periodically
  useEffect(() => {
    let isSubscribed = true;

    const checkSystemHealth = async () => {
      try {
        const health = await checkHealth();
        if (isSubscribed) {
          setSystemHealth(health.status === 'healthy');
        }
      } catch (error) {
        console.error('Health check error:', error);
        if (isSubscribed) {
          setSystemHealth(false);
        }
      } finally {
        if (isSubscribed) {
          setIsLoading(false);
        }
      }
    };

    checkSystemHealth();
    const interval = setInterval(checkSystemHealth, 30000);

    return () => {
      isSubscribed = false;
      clearInterval(interval);
    };
  }, []);

  // Handle camera selection
  const handleCameraSelect = useCallback(async (id: number) => {
    try {
      setIsLoading(true);
      // Stop current camera stream
      if (selectedCamera) {
        await stopCameraStream(selectedCamera);
      }
      // Start new camera stream
      await startCameraStream(id);
      setSelectedCamera(id);
    } catch (error) {
      console.error('Error switching cameras:', error);
    } finally {
      setIsLoading(false);
    }
  }, [selectedCamera]);

  return (
    <AppContext.Provider 
      value={{ 
        selectedCamera, 
        setSelectedCamera: handleCameraSelect, 
        alerts, 
        cameras, 
        stats,
        systemHealth,
        isLoading,
        socketConnected,
        dvrConnected,
        updateDvrConfig
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}