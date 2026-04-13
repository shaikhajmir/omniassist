import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-background text-white">
      <nav className="glass-panel sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-accent rounded-full flex items-center justify-center font-bold text-background text-xl">
            OA
          </div>
          <h1 className="text-2xl font-bold tracking-wider">OmniAssist <span className="text-accent">AI</span></h1>
        </div>
        <div className="flex items-center space-x-4 text-sm text-gray-400">
          <span className="flex items-center"><span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span> SYSTEM ONLINE</span>
        </div>
      </nav>
      <main className="p-6">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
