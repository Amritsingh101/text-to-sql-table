import React from 'react';
import TableCard from './TableCard';

export default function ResultsSection({ activeQuery, results, isLoading, error }) {
  if (!activeQuery && !isLoading && !error && results.length === 0) {
    return null;
  }

  return (
    <section className="results-section">
      <div className="results-header">
        <h2>Relevant Tables</h2>
        {activeQuery && (
          <span className="query-badge">Query: "{activeQuery}"</span>
        )}
      </div>

      {isLoading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Running Hybrid Search (BM25 + FAISS Embeddings) & Cross-Encoder Reranking...</p>
        </div>
      )}

      {error && (
        <div className="error-banner">
          <strong>Error:</strong> {error}
        </div>
      )}

      {!isLoading && !error && results.length > 0 && (
        <div className="results-grid">
          {results.map((item, index) => (
            <TableCard
              key={index}
              rank={index + 1}
              table={typeof item === 'string' ? item : item.table}
            />
          ))}
        </div>
      )}

      {!isLoading && !error && activeQuery && results.length === 0 && (
        <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
          No relevant tables found for this query.
        </p>
      )}
    </section>
  );
}
