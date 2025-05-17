import React, { useState } from "react";

const QueryDocs = ({ onResults }) => {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");

  const handleQuery = async () => {
    if (!query) return;

    try {
      setStatus("🔍 Searching...");
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const result = await res.json();
      if (res.ok) {
        setStatus(`✅ Found ${result.results.length} results`);
        onResults(result.results);
      } else {
        setStatus("❌ Query failed");
      }
    } catch (err) {
      console.error(err);
      setStatus("❌ Server error");
    }
  };

  return (
    <div className="p-4 border rounded shadow-md mt-4">
      <h2 className="text-lg font-semibold mb-2">🔍 Query Documents</h2>
      <input
        type="text"
        className="w-full px-3 py-2 border rounded"
        placeholder="Enter your query..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        onClick={handleQuery}
        className="mt-2 px-4 py-1 bg-indigo-500 text-white rounded hover:bg-indigo-600"
      >
        Search
      </button>
      {status && <p className="mt-2 text-sm">{status}</p>}
    </div>
  );
};

export default QueryDocs;
