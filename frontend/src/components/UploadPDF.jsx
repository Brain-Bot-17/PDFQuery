import React, { useState } from "react";

const UploadPDF = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);


    try {
      setStatus("Uploading...");
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();
      if (res.ok) {
        setStatus(`✅ Uploaded: ${result.filename}`);
      } else {
        setStatus("❌ Upload failed");
      }
    } catch (error) {
      console.error(error);
      setStatus("❌ Server error");
    }
  };

  return (
    <div className="p-4 border rounded shadow-md">
      <h2 className="text-lg font-semibold mb-2">📤 Upload PDF</h2>
      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button
        onClick={handleUpload}
        className="mt-2 px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Upload
      </button>
      {status && <p className="mt-2 text-sm">{status}</p>}
    </div>
  );
};

export default UploadPDF;
