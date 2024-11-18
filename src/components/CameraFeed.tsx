import React from 'react';
import { Camera, Loader2 } from 'lucide-react';
import { useApp } from '../context/AppContext';

export function CameraFeed() {
  const { selectedCamera, setSelectedCamera, cameras, isLoading } = useApp();
  const currentCamera = cameras.find(cam => cam.id === selectedCamera);

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">Live Feed</h2>
      </div>
      <div className="aspect-video bg-gray-900 relative">
        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <Loader2 className="h-8 w-8 text-white animate-spin" />
          </div>
        ) : (
          <>
            <img 
              src={currentCamera?.stream_url}
              alt="Camera Feed"
              className="w-full h-full object-cover"
            />
            <div className="absolute bottom-4 left-4 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full">
              {currentCamera?.name}
            </div>
          </>
        )}
      </div>
      <div className="p-4 grid grid-cols-4 gap-4">
        {cameras.map((camera) => (
          <button
            key={camera.id}
            onClick={() => setSelectedCamera(camera.id)}
            disabled={isLoading}
            className={`p-3 rounded-lg text-sm font-medium ${
              selectedCamera === camera.id
                ? 'bg-indigo-600 text-white'
                : camera.status === 'active'
                ? 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            }`}
          >
            <Camera className="h-4 w-4 mb-1 mx-auto" />
            {camera.name}
          </button>
        ))}
      </div>
    </div>
  );
}