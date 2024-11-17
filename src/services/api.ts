import { config } from '../config';
import { Camera, Alert, Stat } from '../types';

export async function analyzeFrame(imageData: File) {
  const formData = new FormData();
  formData.append('file', imageData);

  try {
    const response = await fetch(`${config.API_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    console.error('Error analyzing frame:', error);
    throw error;
  }
}

export async function checkHealth() {
  try {
    const response = await fetch(`${config.API_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
}

export async function startCameraStream(cameraId: number) {
  try {
    const response = await fetch(`${config.API_URL}/stream/${cameraId}/start`);
    return await response.json();
  } catch (error) {
    console.error('Error starting camera stream:', error);
    throw error;
  }
}

export async function stopCameraStream(cameraId: number) {
  try {
    const response = await fetch(`${config.API_URL}/stream/${cameraId}/stop`);
    return await response.json();
  } catch (error) {
    console.error('Error stopping camera stream:', error);
    throw error;
  }
}