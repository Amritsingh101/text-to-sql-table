import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SearchCard from './components/SearchCard';
import ResultsSection from './components/ResultsSection';

const API_BASE = 'http://127.0.0.1:8000';

export default function App() {
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState(7);
  const [activeQuery, setActiveQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // Check Backend Health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/`, { method: 'GET' });
        if (res.ok) {
          setIsConnected(true);
        } else {
          setIsConnected(false);
        }
      } catch (err) {
        setIsConnected(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (searchQuery, kValue) => {
    setIsLoading(true);
    setError(null);
    setActiveQuery(searchQuery);

    try {
      const response = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery, top_k: kValue })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to search tables.');
      }

      const data = await response.json();
      setResults(data.tables || []);
    } catch (err) {
      setError(`${err.message}. Make sure the backend server is running at ${API_BASE}.`);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header isConnected={isConnected} />

      <main style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <SearchCard
          query={query}
          setQuery={setQuery}
          topK={topK}
          setTopK={setTopK}
          onSearch={handleSearch}
          isLoading={isLoading}
        />

        <ResultsSection
          activeQuery={activeQuery}
          results={results}
          isLoading={isLoading}
          error={error}
        />
      </main>

      <footer className="app-footer">
        <p>Powered by Hybrid BM25 + FAISS Dense Vector Retrieval + Cross-Encoder Reranker</p>
      </footer>
    </div>
  );
}
