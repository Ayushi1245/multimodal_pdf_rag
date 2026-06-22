export default function StatsGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-lg w-full">
      <div className="bg-surface-container-lowest border border-outline-variant/10 shadow-ambient-1 rounded-2xl p-lg flex flex-col items-center justify-center relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-fixed/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <span className="text-4xl font-headline-xl font-bold text-on-surface mb-2 tracking-tight">1</span>
        <span className="font-label-sm text-xs font-semibold text-on-surface-variant uppercase tracking-wider">Documents</span>
      </div>
      <div className="bg-surface-container-lowest border border-outline-variant/10 shadow-ambient-1 rounded-2xl p-lg flex flex-col items-center justify-center relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-secondary-fixed/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <span className="text-4xl font-headline-xl font-bold text-on-surface mb-2 tracking-tight">2</span>
        <span className="font-label-sm text-xs font-semibold text-on-surface-variant uppercase tracking-wider">Indexed Chunks</span>
      </div>
      <div className="bg-surface-container-lowest border border-outline-variant/10 shadow-ambient-1 rounded-2xl p-lg flex flex-col items-center justify-center relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-fixed/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <span className="text-4xl font-headline-xl font-bold text-on-surface mb-2 tracking-tight">0</span>
        <span className="font-label-sm text-xs font-semibold text-on-surface-variant uppercase tracking-wider">Questions Asked</span>
      </div>
    </div>
  );
}
