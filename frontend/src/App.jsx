import React, { useState } from "react";
import UploadPDF from "./components/UploadPDF";
import ProcessControls from "./components/ProcessControls";
import QueryDocs from "./components/QueryDocs";
import ResultsDisplay from "./components/ResultsDisplay";

export default function App() {
  const [results, setResults] = useState([]);

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold mb-4 text-center">📚 PDFQuery </h1>
      <UploadPDF />
      <ProcessControls />
      <QueryDocs onResults={setResults} />
      <ResultsDisplay results={results} />
    </div>
  );
}
