import React from 'react';
import { Database } from 'lucide-react';

export default function Header({ isConnected }) {
  return (
    <header className="app-header">
      <div className="brand">
        <div className="logo-icon">
          <Database size={24} />
        </div>
        <div>
          <h1>Text-to-SQL Table Finder</h1>
          <p className="subtitle">AI-Powered Schema & Table Retrieval System</p>
        </div>
      </div>
      <div className={`status-badge ${isConnected ? 'online' : 'offline'}`}>
        <span className="status-dot"></span>
        <span>{isConnected ? 'Backend Ready' : 'Backend Disconnected'}</span>
      </div>
    </header>
  );
}
