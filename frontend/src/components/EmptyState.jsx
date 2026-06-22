export default function EmptyState() {
  return (
    <div className="flex-1 bg-surface-container-lowest rounded-3xl border border-dashed border-outline-variant/30 shadow-ambient-1 flex flex-col items-center justify-center p-12 text-center relative overflow-hidden min-h-[300px]">
      <div className="relative z-10 flex flex-col items-center max-w-lg">
        <div className="w-20 h-20 mb-lg bg-surface-container-low rounded-2xl flex items-center justify-center border border-outline-variant/20 shadow-sm">
          <span className="material-symbols-outlined text-[40px] text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>auto_stories</span>
        </div>
        <h3 className="font-headline-md text-xl font-semibold text-on-surface mb-3">Upload a PDF in the sidebar to get started.</h3>
        <p className="font-body-md text-on-surface-variant leading-relaxed">Once processed, ask any question about your documents — the AI will analyze the text, images, and charts to provide detailed insights.</p>
      </div>
    </div>
  );
}
