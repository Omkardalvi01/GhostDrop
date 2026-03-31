import { useState, useRef } from 'react';

export default function SendFiles() {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFiles((prev) => [...prev, ...Array.from(e.target.files)]);
    }
  };

  const removeFile = (indexToRemove) => {
    setFiles(files.filter((_, i) => i !== indexToRemove));
  };

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const handleSend = async () => {
    if (files.length === 0) return;
    setIsUploading(true);
    setUploadResult(null);

    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file); 
    });

    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (data.status === 'success') {
        setUploadResult({ success: true, message: `Success! Code: ${data.code}` });
        setFiles([]);
      } else {
        setUploadResult({ success: false, message: data.message || 'Upload failed.' });
      }
    } catch (error) {
      setUploadResult({ success: false, message: 'Network error occurred.' });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-surface-container-lowest dark:bg-[#0c0f10] rounded-3xl ghost-shadow overflow-hidden flex flex-col p-2 border border-outline-variant/10 dark:border-white/5">
      <div className="px-8 pb-10 pt-6">
        
        {/* Drop Zone */}
        <div 
          onClick={() => fileInputRef.current?.click()}
          className="group relative flex flex-col items-center justify-center w-full aspect-[16/9] border-2 border-dashed border-outline-variant/30 rounded-3xl bg-surface dark:bg-white/5 hover:bg-surface-container-low dark:hover:bg-white/10 transition-all cursor-pointer"
        >
          <input 
            type="file" 
            multiple 
            className="hidden" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
          />
          <div className="p-6 bg-surface-container-lowest dark:bg-white/10 rounded-full mb-4 shadow-sm group-hover:scale-105 transition-transform">
            <span className="material-symbols-outlined text-primary dark:text-[#90abff] text-4xl" style={{ fontVariationSettings: "'FILL' 1" }}>upload_file</span>
          </div>
          <h2 className="font-headline font-bold text-xl tracking-tight text-on-surface dark:text-white mb-1">Click to select files here</h2>
          <p className="font-label text-xs uppercase tracking-widest text-on-surface-variant dark:text-slate-400">Max file size: 5 MB each</p>
        </div>

        {/* File List */}
        {files.length > 0 && (
          <div className="mt-12 space-y-4">
            {files.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-4 rounded-xl bg-surface-container-low/50 dark:bg-white/5 hover:bg-primary-container/20 dark:hover:bg-white/10 group transition-colors cursor-default">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 flex items-center justify-center bg-surface-container-lowest dark:bg-white/10 rounded-lg">
                    <span className="material-symbols-outlined text-on-surface-variant dark:text-slate-400 group-hover:text-primary dark:group-hover:text-[#90abff] transition-colors">description</span>
                  </div>
                  <div>
                    <h3 className="text-on-surface dark:text-white font-semibold group-hover:text-primary dark:group-hover:text-[#90abff] transition-colors">{file.name}</h3>
                    <p className="font-label text-[10px] text-on-surface-variant dark:text-slate-500 uppercase tracking-wider">{formatSize(file.size)}</p>
                  </div>
                </div>
                <button onClick={() => removeFile(index)} className="text-on-surface-variant dark:text-slate-400 hover:text-error transition-colors p-2 z-10">
                  <span className="material-symbols-outlined text-xl">close</span>
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Settings Inputs */}
        <div className="mt-10 space-y-6">
          <div className="relative">
            <textarea 
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full bg-surface-container-high dark:bg-white/5 border-none rounded-xl px-6 py-4 font-body text-on-surface dark:text-white placeholder:text-on-surface-variant/60 dark:placeholder:text-slate-500 focus:ring-2 focus:ring-primary/20 focus:bg-surface-container-lowest dark:focus:bg-white/10 transition-all resize-none" 
              placeholder="Add a message (optional)" 
              rows="2"
            ></textarea>
          </div>
        </div>

        {/* Upload Result */}
        {uploadResult && (
          <div className={`mt-6 p-4 rounded-xl text-center font-bold ${uploadResult.success ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'}`}>
            {uploadResult.message}
          </div>
        )}

        {/* Primary Send Button */}
        <button 
          onClick={handleSend}
          disabled={files.length === 0 || isUploading}
          className={`w-full mt-10 primary-gradient text-on-primary py-5 rounded-full font-headline font-extrabold text-lg tracking-tight transition-all flex items-center justify-center space-x-3 ghost-shadow ${files.length === 0 || isUploading ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-90'}`}
        >
          <span>{isUploading ? 'Sending...' : 'Send Files'}</span>
          {!isUploading && <span className="material-symbols-outlined text-2xl">arrow_forward</span>}
        </button>
      </div>
    </div>
  );
}
