export default function ChatInput() {
  return (
    <div className="w-full mt-auto pt-sm relative shrink-0">
      <div className="bg-surface-container-lowest border border-outline-variant/30 shadow-ambient-1 rounded-2xl p-2 flex items-center relative z-10 focus-within:ring-1 focus-within:ring-primary focus-within:border-primary transition-all h-[64px]">
        <button className="p-3 text-on-surface-variant hover:text-primary transition-colors">
          <span className="material-symbols-outlined">add_circle</span>
        </button>
        <input className="flex-1 bg-transparent border-none text-on-surface placeholder:text-on-surface-variant/50 focus:ring-0 p-3 text-lg outline-none font-body-md" placeholder="Ask a question about your documents..." type="text" />
        <button className="w-12 h-12 bg-primary text-on-primary rounded-xl hover:bg-surface-tint transition-colors ml-2 flex items-center justify-center group shadow-ambient-1">
          <span className="material-symbols-outlined group-hover:translate-x-0.5 transition-transform">send</span>
        </button>
      </div>
    </div>
  );
}
