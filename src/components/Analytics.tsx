import React from 'react';
import { BarChart3 } from 'lucide-react';

export function Analytics() {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-medium text-gray-900">Analytics Overview</h2>
        <button className="text-indigo-600 hover:text-indigo-700 font-medium text-sm">
          View Details
        </button>
      </div>
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
        <BarChart3 className="h-32 w-32 text-gray-400" />
      </div>
    </div>
  );
}