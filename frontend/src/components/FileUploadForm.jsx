import { useState } from 'react';

export default function FileUploadForm() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState('PDF');
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');
  const [quality, setQuality] = useState('');
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", fileType);
    formData.append("width", width);
    formData.append("height", height);
    formData.append("quality", quality);

    try {
      const response = await fetch("/api/process", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white rounded shadow">
      <form onSubmit={handleSubmit}>
        <label className="block mb-2">Select File</label>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-4" />

        <label className="block mb-2">File Type</label>
        <select value={fileType} onChange={(e) => setFileType(e.target.value)} className="mb-4">
          <option value="PDF">PDF</option>
          <option value="Image">Image</option>
        </select>

        {fileType === "Image" && (
          <>
            <label className="block mb-2">Width</label>
            <input type="number" value={width} onChange={(e) => setWidth(e.target.value)} className="mb-4 w-full" />
            <label className="block mb-2">Height</label>
            <input type="number" value={height} onChange={(e) => setHeight(e.target.value)} className="mb-4 w-full" />
          </>
        )}

        {fileType === "PDF" && (
          <>
            <label className="block mb-2">Quality</label>
            <select value={quality} onChange={(e) => setQuality(e.target.value)} className="mb-4 w-full">
              <option value="screen">screen</option>
              <option value="ebook">ebook</option>
              <option value="printer">printer</option>
              <option value="prepress">prepress</option>
            </select>
          </>
        )}

        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Process</button>
      </form>

      {downloadUrl && (
        <div className="mt-4">
          <a href={downloadUrl} download className="text-green-600 underline">Download Processed File</a>
        </div>
      )}

      {error && (
        <div className="mt-4 text-red-600">
          {error}
        </div>
      )}
    </div>
  );
}