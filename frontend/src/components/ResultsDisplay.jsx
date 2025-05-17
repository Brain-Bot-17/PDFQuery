import React from "react";

const ResultsDisplay = ({ results }) => {
  if (!results || results.length === 0) return null;

  return (
    <div className="p-4 border rounded shadow-md mt-4">
      <h2 className="text-lg font-semibold mb-2">💬 Results</h2>
      <ul className="space-y-2">
        {results.map((item, index) => (
          <li key={index} className="p-2 bg-gray-100 rounded">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ResultsDisplay;
