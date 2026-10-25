export default function ChatInput() {
  return (
    <div className="w-full relative shrink-0 z-10 mt-auto pt-16">
      <div className="bg-surface-bright/50 border border-outline-variant/30 rounded-2xl p-2 flex items-center relative focus-within:border-primary/50 transition-colors h-[60px] max-w-3xl mx-auto backdrop-blur-md">
        <input className="flex-1 bg-transparent border-none text-on-surface placeholder:text-on-surface-variant focus:ring-0 px-4 text-sm outline-none font-body-md" placeholder="Ask a question about your documents..." type="text" />
        <button className="w-11 h-11 bg-primary text-on-primary rounded-xl hover:bg-primary-fixed-dim transition-colors ml-2 flex items-center justify-center group shadow-md">
          <span className="material-symbols-outlined group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform text-[20px]">send</span>
        </button>
      </div>
    </div>
  );
}
