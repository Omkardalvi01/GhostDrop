import { useState, useEffect } from 'react';
import SendFiles from './components/SendFiles';
import ReceiveFiles from './components/ReceiveFiles';

function App() {
  const [mode, setMode] = useState('send');
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  return (
    <div className="bg-surface dark:bg-black text-on-surface dark:text-[#dadddf] font-body min-h-screen flex flex-col selection:bg-primary-container/30 transition-colors duration-300">
      
      {/* TopAppBar */}
      <nav className="fixed top-0 w-full z-50 bg-[#06092f]/80 backdrop-blur-xl shadow-[0_12px_32px_rgba(0,0,0,0.06)] bg-gradient-to-b from-[#0b0e38] to-transparent">
        <div className="flex justify-between items-center px-8 h-20 w-full">
          <div className="flex items-center">
            <span className="text-2xl font-bold tracking-tighter text-[#90abff] font-headline">GhostDrop</span>
          </div>
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsDark(!isDark)}
              className="p-2.5 text-slate-400 hover:bg-white/5 transition-all duration-300 rounded-full flex items-center justify-center"
            >
              {isDark ? (
                 <span className="material-symbols-outlined">light_mode</span>
              ) : (
                 <span className="material-symbols-outlined">dark_mode</span>
              )}
            </button>
            <button className="p-2.5 text-slate-400 hover:bg-white/5 transition-all duration-300 rounded-full">
              <span className="material-symbols-outlined">help</span>
            </button>
          </div>
        </div>
      </nav>

      <main className="flex-grow flex justify-center px-6 pt-32 pb-16">
        <div className="w-full max-w-xl">
          {/* Context Switcher */}
          <div className="flex justify-center mb-12">
            <div className="bg-surface-container-low dark:bg-white/5 p-1.5 rounded-full flex items-center gap-1">
              <button 
                onClick={() => setMode('send')}
                className={`px-8 py-2.5 rounded-full text-sm font-semibold transition-all ${
                  mode === 'send' 
                    ? 'bg-surface-container-lowest dark:bg-white/10 text-primary dark:text-[#90abff] shadow-sm' 
                    : 'text-on-surface-variant hover:text-on-surface dark:text-slate-400 dark:hover:text-white'
                }`}
              >
                Send
              </button>
              <button 
                onClick={() => setMode('receive')}
                className={`px-8 py-2.5 rounded-full text-sm font-semibold transition-all ${
                  mode === 'receive' 
                    ? 'bg-surface-container-lowest dark:bg-white/10 text-primary dark:text-[#90abff] shadow-sm' 
                    : 'text-on-surface-variant hover:text-on-surface dark:text-slate-400 dark:hover:text-white'
                }`}
              >
                Receive
              </button>
            </div>
          </div>

          {mode === 'send' ? <SendFiles /> : <ReceiveFiles />}
          
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full bg-[#06092f] border-t border-[#42456c]/15 pt-8 pb-12">
        <div className="flex flex-col md:flex-row justify-between items-center px-12 max-w-7xl mx-auto">
          <div className="flex flex-col gap-2 mb-6 md:mb-0">
            <span className="text-lg font-bold text-[#90abff] font-headline">GhostDrop</span>
            <span className="text-sm font-body text-slate-500 uppercase tracking-widest">© 2024 GhostDrop. Ethereal Precision.</span>
          </div>
          <div className="flex gap-8">
            <a href="#" className="text-sm font-body text-slate-500 uppercase tracking-widest hover:text-[#90abff] transition-colors focus:outline-none">Privacy</a>
            <a href="#" className="text-sm font-body text-slate-500 uppercase tracking-widest hover:text-[#90abff] transition-colors focus:outline-none">Terms</a>
            <a href="#" className="text-sm font-body text-slate-500 uppercase tracking-widest hover:text-[#90abff] transition-colors focus:outline-none">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
