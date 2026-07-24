import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';

export default function TableCard({ rank, table }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(table);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="table-card">
      <div className="table-info">
        <div className="rank-badge">#{rank}</div>
        <span className="table-name">{table}</span>
      </div>

      <button 
        className={`copy-btn ${copied ? 'copied' : ''}`}
        onClick={handleCopy}
        title="Copy table name"
      >
        {copied ? <Check size={14} /> : <Copy size={14} />}
      </button>
    </div>
  );
}
