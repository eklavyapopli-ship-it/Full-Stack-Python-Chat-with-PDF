'use client';

import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';
interface ResMes {
  message?: string;
}

const FileUploadPage = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ResMes|null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileClick = () => {
    fileInputRef.current?.click(); // Open file picker
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setResponse(null);
    setError(null);

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch('http://localhost:8000/uploadfile/', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error(`Upload failed with status ${res.status}`);
      const data = await res.json();
      setResponse(data);
      setFile(null);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 shadow-2xl text-white flex flex-col justify-center items-center p-8 rounded-lg border-2 border-white space-y-4">
      <h3 className="text-lg font-bold">Upload PDF File</h3>

      <input
        type="file"
        accept="application/pdf"
        className="hidden"
        ref={fileInputRef}
        onChange={handleFileChange}
      />

      <div
        onClick={handleFileClick}
        className="cursor-pointer flex flex-col justify-center items-center p-6 bg-slate-700 rounded-lg hover:bg-slate-600 transition"
      >
        <Upload className="w-10 h-10 mb-2" />
        <span>{file ? file.name : 'Click to select a file'}</span>
      </div>

      {loading && <p>Uploading...</p>}
      {error && <p className="text-red-400">{error}</p>}
      {response && (
  <div className="bg-slate-800 p-2 rounded">
    {response.message && <p>{response.message}</p>}
  </div>
      )}
    </div>
  );
};

export default FileUploadPage;
