export default function StatsGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl mx-auto mt-8 z-10 relative px-4">
      <div className="bg-surface-container-lowest border border-outline-variant/30 shadow-ambient-2 rounded-2xl p-6 flex flex-col items-center justify-center relative group hover:border-primary/50 transition-colors h-[140px]">
        <div className="absolute left-6 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-surface-bright flex items-center justify-center">
          <span className="material-symbols-outlined text-on-surface-variant">description</span>
        </div>
        <div className="flex flex-col items-center ml-8">
          <span className="text-3xl font-headline-xl font-bold text-on-surface tracking-tight mb-1">2</span>
          <span className="font-label-sm text-[11px] font-bold text-on-surface uppercase tracking-wider mb-1">Documents</span>
          <span className="font-label-sm text-xs text-on-surface-variant">Uploaded</span>
        </div>
      </div>
      <div className="bg-surface-container-lowest border-2 border-primary shadow-[0_0_20px_rgba(139,92,246,0.15)] rounded-2xl p-6 flex flex-col items-center justify-center relative group h-[140px]">
        <div className="absolute left-6 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
          <span className="material-symbols-outlined text-primary">layers</span>
        </div>
        <div className="flex flex-col items-center ml-8">
          <span className="text-3xl font-headline-xl font-bold text-on-surface tracking-tight mb-1">5</span>
          <span className="font-label-sm text-[11px] font-bold text-on-surface uppercase tracking-wider mb-1">Indexed Chunks</span>
          <span className="font-label-sm text-xs text-on-surface-variant">Processed</span>
        </div>
      </div>
      <div className="bg-surface-container-lowest border border-outline-variant/30 shadow-ambient-2 rounded-2xl p-6 flex flex-col items-center justify-center relative group hover:border-primary/50 transition-colors h-[140px]">
        <div className="absolute left-6 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-surface-bright flex items-center justify-center">
          <span className="material-symbols-outlined text-on-surface-variant">help</span>
        </div>
        <div className="flex flex-col items-center ml-8">
          <span className="text-3xl font-headline-xl font-bold text-on-surface tracking-tight mb-1">0</span>
          <span className="font-label-sm text-[11px] font-bold text-on-surface uppercase tracking-wider mb-1">Questions Asked</span>
          <span className="font-label-sm text-xs text-on-surface-variant">Today</span>
        </div>
      </div>
    </div>
  );
}
