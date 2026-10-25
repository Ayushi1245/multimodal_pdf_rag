import ChatInput from "./ChatInput";

export default function EmptyState() {
  return (
    <div className="w-full max-w-4xl mx-auto mt-6 bg-surface-container-lowest/80 backdrop-blur-xl border border-outline-variant/30 shadow-ambient-2 rounded-2xl flex flex-col items-center justify-end relative overflow-hidden min-h-[300px] p-6 z-10 mb-8">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-[70%] opacity-90">
        <div className="w-20 h-24 bg-gradient-to-br from-white/20 to-white/5 rounded-t-lg rounded-br-lg flex flex-col p-3 shadow-lg backdrop-blur-md border border-white/20 relative before:absolute before:-top-[1px] before:-right-[1px] before:w-6 before:h-6 before:bg-surface-container-lowest/80 before:border-l before:border-b before:border-white/20 before:rounded-bl-lg">
          <div className="w-full h-1.5 bg-primary/40 rounded-full mb-2 mt-2"></div>
          <div className="w-3/4 h-1.5 bg-primary/40 rounded-full mb-3"></div>
          <div className="w-full h-10 bg-primary/20 rounded mt-auto flex items-center justify-center p-1 border border-primary/20">
             <span className="material-symbols-outlined text-primary text-[20px]">image</span>
          </div>
        </div>
      </div>
      
      <ChatInput />
      
      <p className="mt-4 text-[13px] text-on-surface-variant text-center max-w-lg">
        Once processed, ask any question about your documents —<br/>
        text, images, charts, tables, anything!
      </p>
    </div>
  );
}
