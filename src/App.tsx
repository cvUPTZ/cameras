// App.jsx
import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import { DvrLogin } from './components/DvrLogin';
import { Header } from './components/Header';
import { StatsGrid } from './components/StatsGrid';
import { CameraFeed } from './components/CameraFeed';
import { Analytics } from './components/Analytics';
import { AlertsList } from './components/AlertsList';
import { HeatMap } from './components/HeatMap';

// Separate component to use the context
function AppContent() {
  const { isAuthenticated } = useApp();

  if (!isAuthenticated) {
    return <DvrLogin />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <StatsGrid />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <CameraFeed />
            <Analytics />
          </div>
          <div className="space-y-6">
            <AlertsList />
            <HeatMap />
          </div>
        </div>
      </main>
    </div>
  );
}

// Main App component
function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;