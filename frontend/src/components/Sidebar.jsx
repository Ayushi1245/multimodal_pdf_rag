export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-full flex flex-col w-72 border-r border-outline-variant/20 bg-surface-container-lowest z-20 shadow-xl hidden md:flex">
      <div className="p-xl pb-md border-b border-outline-variant/10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-sm">
            <div className="w-10 h-10 rounded-full flex items-center justify-center shrink-0">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C11.4 2 11 2.4 11 3V4.1C8.2 4.6 6 6.8 5.1 9.6L4.1 9.3C3.5 9.1 2.9 9.5 2.8 10.1C2.7 10.7 3.1 11.3 3.7 11.4L4.8 11.7C4.8 12 4.8 12.3 4.8 12.7L3.7 13C3.1 13.2 2.7 13.8 2.8 14.4C2.9 15 3.5 15.4 4.1 15.2L5.1 14.9C6 17.7 8.2 19.9 11 20.4V21.5C11 22.1 11.4 22.5 12 22.5C12.6 22.5 13 22.1 13 21.5V20.4C15.8 19.9 18 17.7 18.9 14.9L19.9 15.2C20.5 15.4 21.1 15 21.2 14.4C21.3 13.8 20.9 13.2 20.3 13L19.2 12.7C19.2 12.4 19.2 12.1 19.2 11.8L20.3 11.5C20.9 11.3 21.3 10.7 21.2 10.1C21.1 9.5 20.5 9.1 19.9 9.3L18.9 9.6C18 6.8 15.8 4.6 13 4.1V3C13 2.4 12.6 2 12 2ZM12 6C15.3 6 18 8.7 18 12C18 15.3 15.3 18 12 18C8.7 18 6 15.3 6 12C6 8.7 8.7 6 12 6ZM12 8C9.8 8 8 9.8 8 12C8 14.2 9.8 16 12 16C14.2 16 16 14.2 16 12C16 9.8 14.2 8 12 8Z" fill="#8b5cf6"/>
                <circle cx="12" cy="12" r="2" fill="#8b5cf6"/>
                <circle cx="12" cy="5" r="1.5" fill="#c4b5fd"/>
                <circle cx="12" cy="19" r="1.5" fill="#c4b5fd"/>
                <circle cx="5" cy="12" r="1.5" fill="#c4b5fd"/>
                <circle cx="19" cy="12" r="1.5" fill="#c4b5fd"/>
              </svg>
            </div>
            <h1 className="text-md font-headline-md font-semibold text-on-surface">Document Manager</h1>
          </div>
          <button className="text-on-surface-variant hover:text-primary transition-colors">
             <span className="material-symbols-outlined text-[20px]">menu</span>
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto py-lg px-xl flex flex-col gap-lg">
        <div className="flex flex-col gap-sm">
          <h2 className="font-label-sm text-[11px] font-semibold text-on-surface-variant/80 uppercase tracking-wider mb-2">Upload PDF Documents</h2>
          <div className="bg-surface-container-lowest rounded-xl p-md border border-dashed border-outline-variant/60 hover:border-primary/50 transition-colors flex flex-col items-center justify-center text-center gap-sm group cursor-pointer shadow-ambient-1 h-[200px]">
            <div className="mb-2">
              <span className="material-symbols-outlined text-primary text-[40px]">cloud_upload</span>
            </div>
            <p className="font-label-md text-sm text-on-surface-variant mb-1">Drag & drop your PDFs here</p>
            <p className="font-label-sm text-xs text-on-surface-variant mb-4">or</p>
            <button className="py-2.5 px-6 rounded-lg bg-primary text-on-primary hover:bg-primary-fixed-dim transition-colors text-sm font-medium shadow-ambient-1 mb-4">
              Upload PDF
            </button>
            <p className="font-label-sm text-[11px] text-on-surface-variant/70">Max file size: 200MB per PDF</p>
          </div>
        </div>

        <div className="flex flex-col gap-xs mt-4">
          <h2 className="font-label-sm text-[11px] font-semibold text-on-surface-variant/80 uppercase tracking-wider mb-2">Indexed Documents</h2>
          <ul className="flex flex-col gap-3">
            <li>
              <div className="flex items-center justify-between p-3 rounded-lg bg-surface-bright border border-outline-variant/30 group">
                <div className="flex items-start gap-3 overflow-hidden">
                  <div className="bg-white rounded flex items-center justify-center shrink-0 w-8 h-10 p-1 relative">
                    <span className="material-symbols-outlined text-error text-[20px]">picture_as_pdf</span>
                    <span className="absolute bottom-0 right-0 text-[8px] font-bold text-white bg-error px-0.5 rounded-sm">PDF</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="font-label-md text-sm truncate text-on-surface font-medium">tmpJC68l4c4.pdf</span>
                    <span className="text-[11px] text-on-surface-variant">Indexed on 16 Jul 2025</span>
                  </div>
                </div>
                <div className="flex gap-1 shrink-0">
                  <button className="text-on-surface-variant hover:text-on-surface transition-colors">
                     <span className="material-symbols-outlined text-[18px]">more_vert</span>
                  </button>
                  <button className="text-error/80 hover:text-error transition-opacity">
                    <span className="material-symbols-outlined text-[18px]">delete</span>
                  </button>
                </div>
              </div>
            </li>
            <li>
              <div className="flex items-center justify-between p-3 rounded-lg bg-surface-bright border border-outline-variant/30 group">
                <div className="flex items-start gap-3 overflow-hidden">
                  <div className="bg-white rounded flex items-center justify-center shrink-0 w-8 h-10 p-1 relative">
                    <span className="material-symbols-outlined text-error text-[20px]">picture_as_pdf</span>
                    <span className="absolute bottom-0 right-0 text-[8px] font-bold text-white bg-error px-0.5 rounded-sm">PDF</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="font-label-md text-sm truncate text-on-surface font-medium">tmp482i4z_d.pdf</span>
                    <span className="text-[11px] text-on-surface-variant">Indexed on 16 Jul 2025</span>
                  </div>
                </div>
                <div className="flex gap-1 shrink-0">
                  <button className="text-on-surface-variant hover:text-on-surface transition-colors">
                     <span className="material-symbols-outlined text-[18px]">more_vert</span>
                  </button>
                  <button className="text-error/80 hover:text-error transition-opacity">
                    <span className="material-symbols-outlined text-[18px]">delete</span>
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div className="px-xl pb-md pt-2">
        <button className="w-full py-2.5 px-md rounded-lg text-primary border border-primary/30 hover:bg-primary/10 transition-all text-sm font-medium flex items-center justify-center gap-sm mb-6">
          <span className="material-symbols-outlined text-[18px]">delete</span>
          Clear Index
        </button>
        
        <div className="bg-surface-bright rounded-lg p-3 flex items-center justify-between border border-outline-variant/20">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-on-surface-variant text-[20px]">database</span>
            <div className="flex flex-col">
              <span className="text-[10px] text-on-surface-variant uppercase tracking-wider">Vector DB Status</span>
              <span className="text-xs text-on-surface font-medium">ChromaDB Connected</span>
            </div>
          </div>
          <div className="w-2.5 h-2.5 rounded-full bg-secondary shadow-[0_0_8px_rgba(16,185,129,0.5)]"></div>
        </div>
      </div>
    </aside>
  );
}
