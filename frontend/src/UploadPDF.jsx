import React, { useState } from 'react';

export default function UploadPDF() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a PDF file first.');
      return;
    }
    setMessage('Uploading...');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        setMessage('Upload successful! Processing...');
      } else {
        setMessage('Upload failed.');
      }
    } catch (err) {
      setMessage('Error uploading file.');
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white shadow rounded mt-6">
      <h2 className="text-xl font-semibold mb-4">Upload PDF</h2>
      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        className="border p-2 rounded w-full"
      />
      <button
        onClick={handleUpload}
        className="mt-4 bg-primary text-white px-4 py-2 rounded hover:bg-blue-900 transition"
      >
        Upload
      </button>
      {message && <p className="mt-2 text-sm text-gray-600">{message}</p>}
    </div>
  );
}
