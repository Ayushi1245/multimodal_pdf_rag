export default function Header() {
  return (
    <header className="absolute top-0 right-0 p-lg z-20 flex justify-end items-center pointer-events-none">
      <div className="flex items-center gap-4 pointer-events-auto">
        <div className="flex items-center bg-surface-bright border border-outline-variant/30 rounded-full p-1 shadow-ambient-1">
          <button className="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:text-on-surface transition-colors">
             <span className="material-symbols-outlined text-[18px]">light_mode</span>
          </button>
          <button className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-on-primary shadow-sm">
             <span className="material-symbols-outlined text-[18px]">dark_mode</span>
          </button>
        </div>
        
        <div className="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center text-on-primary-container font-semibold font-headline-md shadow-ambient-1 border border-primary/20 cursor-pointer">
          A
        </div>
      </div>
    </header>
  );
}
