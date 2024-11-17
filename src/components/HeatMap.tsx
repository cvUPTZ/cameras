import React from 'react';
import { Map } from 'lucide-react';

export function HeatMap() {
  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">Activity Heat Map</h2>
      </div>
      <div className="p-4">
        <div className="aspect-square bg-gray-50 rounded-lg flex items-center justify-center">
          <Map className="h-32 w-32 text-gray-400" />
        </div>
      </div>
    </div>
  );
}