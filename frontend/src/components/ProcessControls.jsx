import React, { useState } from "react";

const ProcessControls = () => {
  const [status, setStatus] = useState("");

  const handleProcess = async (endpoint, message) => {
    try {
      setStatus(`🔄 ${message}...`);
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/${endpoint}`, {
        method: "POST",
      });

      const result = await res.json();
      if (res.ok) {
        let finalMsg = "";

        if (endpoint === "embed") {
          finalMsg = result.status;
        } else if (endpoint === "process") {
          finalMsg = `Extracted ${result.extracted.length} files and chunked ${result.chunked.length} files.`;
        } else {
          finalMsg = "✅ Success";
        }

        setStatus(`✅ ${finalMsg}`);
      } else {
        setStatus("❌ Processing failed");
      }
    } catch (err) {
      console.error(err);
      setStatus("❌ Server error");
    }
  };

  return (
    <div className="p-4 border rounded shadow-md mt-4">
      <h2 className="text-lg font-semibold mb-2">⚙️ Preprocess & Embed</h2>
      <div className="flex gap-2">
        <button
          onClick={() => handleProcess("process", "Extracting + Chunking")}
          className="px-4 py-1 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Extract + Chunk
        </button>
        <button
          onClick={() => handleProcess("embed", "Generating Embeddings")}
          className="px-4 py-1 bg-purple-500 text-white rounded hover:bg-purple-600"
        >
          Generate Embeddings
        </button>
      </div>
      {status && <p className="mt-2 text-sm">{status}</p>}
    </div>
  );
};

export default ProcessControls;
