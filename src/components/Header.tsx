import React from 'react';
import { Bell, Settings, Shield, Wifi, WifiOff } from 'lucide-react';
import { useApp } from '../context/AppContext';

export function Header() {
  const { socketConnected, systemHealth } = useApp();

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <Shield className="h-8 w-8 text-indigo-600" />
            <h1 className="text-2xl font-bold text-gray-900">Advanced Theft Detection</h1>
          </div>
          <div className="flex items-center space-x-4">
            {socketConnected ? (
              <Wifi className="h-5 w-5 text-green-500" />
            ) : (
              <WifiOff className="h-5 w-5 text-red-500" />
            )}
            <div className={`h-2 w-2 rounded-full ${systemHealth ? 'bg-green-500' : 'bg-red-500'}`} />
            <button className="p-2 rounded-full hover:bg-gray-100">
              <Bell className="h-5 w-5 text-gray-600" />
            </button>
            <button className="p-2 rounded-full hover:bg-gray-100">
              <Settings className="h-5 w-5 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}