import { useState, useRef } from 'react';

export default function ReceiveFiles() {
  const [code, setCode] = useState(['', '', '', '']);
  const [isDownloading, setIsDownloading] = useState(false);
  const [resultMessage, setResultMessage] = useState(null);
  const inputsRef = useRef([]);

  const handleChange = (index, value) => {
    if (!/^\d*$/.test(value)) return;
    
    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);

    if (value && index < 3) {
      inputsRef.current[index + 1].focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      inputsRef.current[index - 1].focus();
    }
  };

  const handleDownload = async () => {
    const fullCode = code.join('');
    if (fullCode.length !== 4) return;
    
    setIsDownloading(true);
    setResultMessage(null);

    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
      const response = await fetch(`${API_BASE}/download?code=${fullCode}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setResultMessage({ success: true, message: 'Downloading ' + data.files.length + ' file(s)...' });
        
        // Loop through each generated URL and trigger a native browser download
        data.files.forEach((fileObj, index) => {
          setTimeout(() => {
            const a = document.createElement('a');
            a.href = fileObj.url;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
          }, index * 500); // 500ms stagger avoids browser popup blockers
        });
      } else {
        setResultMessage({ success: false, message: data.message || 'Download failed.' });
      }
    } catch (error) {
      setResultMessage({ success: false, message: 'Network error occurred.' });
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="glass-card rounded-3xl p-10 border border-outline-variant/10 shadow-[0_20px_40px_rgba(12,15,16,0.05)] relative overflow-hidden bg-surface-container-lowest">
      <div className="mb-12">
        <span className="font-label text-xs uppercase tracking-[0.2em] text-on-surface-variant dark:text-slate-400 block mb-2">Secure Retrieval</span>
        <h1 className="text-4xl font-extrabold font-headline tracking-tight text-on-surface dark:text-white leading-tight">
          Enter Code to<br/>Receive Assets.
        </h1>
      </div>

      <div className="space-y-10 z-10 relative">
        <div className="flex justify-between gap-4">
          {[0, 1, 2, 3].map((index) => (
            <div key={index} className="flex-1 aspect-square max-w-[80px]">
              <input 
                ref={(el) => inputsRef.current[index] = el}
                type="text" 
                maxLength="1"
                value={code[index]}
                onChange={(e) => handleChange(index, e.target.value)}
                onKeyDown={(e) => handleKeyDown(index, e)}
                placeholder="0"
                className="w-full h-full text-center text-3xl font-bold font-headline rounded-xl bg-surface-container-high dark:bg-white/5 border-none focus:ring-2 focus:ring-primary focus:bg-surface-container-lowest dark:focus:bg-white/10 transition-all text-on-surface dark:text-white"
              />
            </div>
          ))}
        </div>

        {resultMessage && (
          <div className={`p-4 rounded-xl text-center font-bold ${resultMessage.success ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'}`}>
            {resultMessage.message}
          </div>
        )}

        <button 
          onClick={handleDownload}
          disabled={code.join('').length !== 4 || isDownloading}
          className={`w-full primary-gradient py-5 rounded-xl flex items-center justify-center gap-3 text-on-primary font-bold tracking-tight transition-opacity group ${code.join('').length !== 4 || isDownloading ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-90'}`}
        >
          <span className="material-symbols-outlined text-xl">download</span>
          {isDownloading ? 'Downloading...' : 'Download All Files'}
          {!isDownloading && <span className="material-symbols-outlined text-lg opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all">arrow_forward</span>}
        </button>
      </div>

      {/* Subtle Decorative Background Element */}
      <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>

      {/* Help/Information Text */}
      <p className="text-center mt-8 text-on-surface-variant dark:text-slate-500 font-label text-xs tracking-wide relative z-10">
        Codes are valid for 24 hours. Need help? <a href="#" className="text-primary dark:text-[#90abff] hover:underline">Contact Support</a>
      </p>
    </div>
  );
}
