import React from 'react';
import { Search, X, ArrowRight, Loader2 } from 'lucide-react';

const SAMPLE_QUERIES = [
  { label: 'find user details named "anshul"', query: 'find the user details named "anshul".' },
  { label: 'customer transactions & history', query: 'show customer transaction and order history' },
  { label: 'employee salary & department', query: 'get employee salary and department details' },
  { label: 'product stock & categories', query: 'list product categories and current stock levels' }
];

export default function SearchCard({ 
  query, 
  setQuery, 
  topK, 
  setTopK, 
  onSearch, 
  isLoading 
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), topK);
    }
  };

  const handleSampleClick = (sampleQuery) => {
    setQuery(sampleQuery);
    onSearch(sampleQuery, topK);
  };

  return (
    <section className="search-card">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <div className="search-input-wrapper">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              className="search-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your query (e.g., 'find the user details named anshul')"
              autoComplete="off"
              required
            />
            {query && (
              <button 
                type="button" 
                className="clear-btn" 
                onClick={() => setQuery('')}
                title="Clear input"
              >
                <X size={18} />
              </button>
            )}
          </div>

          <div className="top-k-wrapper">
            <label htmlFor="top-k">Top K:</label>
            <input
              id="top-k"
              type="number"
              className="top-k-input"
              min="1"
              max="15"
              value={topK}
              onChange={(e) => setTopK(parseInt(e.target.value, 10) || 7)}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? (
              <>
                <span>Searching...</span>
                <Loader2 size={18} className="spinner-icon" style={{ animation: 'spin 1s linear infinite' }} />
              </>
            ) : (
              <>
                <span>Find Tables</span>
                <ArrowRight size={18} />
              </>
            )}
          </button>
        </div>
      </form>

      <div className="quick-examples">
        <span className="example-label">Sample Queries:</span>
        <div className="pills">
          {SAMPLE_QUERIES.map((item, idx) => (
            <button
              key={idx}
              type="button"
              className="pill-btn"
              onClick={() => handleSampleClick(item.query)}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
