import React from "react";

const ResultsDisplay = ({ results }) => {
  if (!results?.length) return null;

  return (
    <div className="p-4 mt-4 rounded shadow-md bg-white text-black">
      <h2 className="text-lg font-semibold mb-2">💬 Results</h2>
      <ul className="space-y-2">
        {results.map((item, index) => (
          <li key={index} className="p-2 bg-gray-100 rounded break-words whitespace-pre-wrap">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ResultsDisplay;
