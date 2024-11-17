import React from 'react';
import { useApp } from '../context/AppContext';

export function AlertsList() {
  const { alerts } = useApp();

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">Recent Alerts</h2>
      </div>
      <div className="divide-y divide-gray-200">
        {alerts.map((alert) => (
          <div key={alert.id} className="p-4">
            <div className="flex items-center justify-between mb-1">
              <p className="font-medium text-gray-900">{alert.type}</p>
              <span className="text-sm text-gray-500">{alert.time}</span>
            </div>
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">{alert.camera}</p>
              <span
                className={`px-2 py-1 text-xs font-medium rounded-full ${
                  alert.severity === 'high'
                    ? 'bg-red-100 text-red-800'
                    : alert.severity === 'medium'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-green-100 text-green-800'
                }`}
              >
                {alert.severity.charAt(0).toUpperCase() + alert.severity.slice(1)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}