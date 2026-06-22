export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-full flex flex-col w-64 border-r border-outline-variant/20 bg-surface-container-low z-20 shadow-sm hidden md:flex">
      <div className="p-lg pb-md border-b border-outline-variant/20">
        <div className="flex items-center gap-sm mb-1">
          <div className="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-on-primary-container" style={{ fontVariationSettings: "'FILL' 1" }}>analytics</span>
          </div>
          <div>
            <h1 className="text-lg font-headline-md font-semibold tracking-tight text-primary">Multimodal RAG</h1>
            <p className="font-label-sm text-[10px] text-on-surface-variant font-medium tracking-wide uppercase">AI Analyzer</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto py-lg px-md flex flex-col gap-lg">
        <div className="flex flex-col gap-sm">
          <h2 className="font-label-sm text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider px-sm">Document Manager</h2>
          <div className="bg-surface-container-lowest rounded-xl p-md border border-dashed border-primary/30 hover:border-primary transition-colors flex flex-col items-center justify-center text-center gap-sm group cursor-pointer shadow-ambient-1">
            <div className="w-10 h-10 rounded-full bg-primary-fixed flex items-center justify-center group-hover:bg-primary-container transition-colors">
              <span className="material-symbols-outlined text-primary">cloud_upload</span>
            </div>
            <div>
              <p className="font-label-md text-label-md text-on-surface">Upload PDF documents</p>
              <p className="font-label-sm text-[11px] text-on-surface-variant mt-1">200MB per file • PDF</p>
            </div>
            <button className="mt-sm w-full py-2 px-md rounded-lg bg-primary text-on-primary border border-transparent hover:bg-surface-tint transition-colors text-sm font-medium flex items-center justify-center gap-sm shadow-ambient-1">
              <span className="material-symbols-outlined text-[18px]">upload</span>
              Upload
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-xs">
          <div className="flex items-center justify-between px-sm mb-xs">
            <h2 className="font-label-sm text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider">Indexed Documents</h2>
            <span className="font-label-sm text-[11px] bg-primary-fixed text-primary px-2 py-0.5 rounded-full">1</span>
          </div>
          <ul className="flex flex-col gap-xs">
            <li>
              <div className="flex items-center justify-between p-sm rounded-lg bg-primary-fixed/50 text-primary border border-primary/20 group cursor-pointer">
                <div className="flex items-center gap-sm overflow-hidden">
                  <span className="material-symbols-outlined text-[18px] shrink-0">description</span>
                  <span className="font-label-md text-sm truncate">tmpjc68l4c1.pdf</span>
                </div>
                <button className="opacity-0 group-hover:opacity-100 transition-opacity hover:text-error">
                  <span className="material-symbols-outlined text-[18px]">close</span>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div className="p-md border-t border-outline-variant/20">
        <button className="w-full py-2.5 px-md rounded-lg text-on-surface-variant hover:text-error hover:bg-error-container border border-transparent hover:border-error/20 transition-all text-sm font-medium flex items-center justify-center gap-sm">
          <span className="material-symbols-outlined text-[18px]">delete_sweep</span>
          Clear Index
        </button>
      </div>
    </aside>
  );
}
