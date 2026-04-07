import React from 'react';

const GlassPanel = ({ children, className }) => (
  <div className={`bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl ${className}`}>
    {children}
  </div>
);

export default function VideoEditor() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-6 font-sans selection:bg-[#ffef00] selection:text-black">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-black italic uppercase tracking-tighter">
          NEXUS<span className="text-[#ffef00]">.CUT</span>
        </h1>
        <button className="bg-[#ffef00] text-black px-8 py-2 rounded-full font-bold hover:shadow-[0_0_20px_rgba(255,239,0,0.4)] transition-all">
          RENDER
        </button>
      </div>

      <div className="grid grid-cols-12 gap-6 h-[70vh]">
        {/* Инструменты AI */}
        <GlassPanel className="col-span-3 p-6 flex flex-col gap-4">
          <h2 className="text-[#ffef00] font-bold text-sm tracking-widest uppercase">AI Magic</h2>
          {['Auto-Subtitle', 'Smart Crop', 'Color Grade', 'Deepfake Audio'].map(tool => (
            <button key={tool} className="w-full text-left p-4 rounded-xl border border-white/5 hover:bg-white/10 transition-colors bg-white/5">
              {tool}
            </button>
          ))}
        </GlassPanel>

        {/* Плеер */}
        <GlassPanel className="col-span-9 relative overflow-hidden flex items-center justify-center">
          <div className="w-full h-full bg-gradient-to-br from-white/5 to-transparent flex items-center justify-center">
             <div className="text-white/20 uppercase font-black text-6xl">Preview</div>
             {/* Сюда вставится 3D-элемент или Canvas видео */}
          </div>
        </GlassPanel>
      </div>

      {/* Таймлайн */}
      <GlassPanel className="mt-6 h-32 w-full p-4 flex items-center relative overflow-hidden">
        <div className="absolute top-0 left-1/4 h-full w-[2px] bg-[#ffef00] z-10 shadow-[0_0_10px_#ffef00]"></div>
        <div className="flex gap-2 opacity-30">
          {[...Array(20)].map((_, i) => (
            <div key={i} className="w-16 h-12 bg-white/20 rounded-md"></div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
