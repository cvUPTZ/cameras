import React from 'react';
import { useApp } from '../context/AppContext';

export function StatsGrid() {
  const { stats } = useApp();

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.label}</p>
              <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
            </div>
            <stat.icon className="h-8 w-8 text-indigo-600" />
          </div>
        </div>
      ))}
    </div>
  );
}