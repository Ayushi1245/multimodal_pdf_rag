import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import StatsGrid from "./components/StatsGrid";
import EmptyState from "./components/EmptyState";

export default function App() {
  return (
    <>
      <Sidebar />
      <div className="flex-1 md:ml-72 flex flex-col h-screen relative bg-surface overflow-hidden">
        <Header />
        
        {/* Background Image Area */}
        <div className="absolute top-0 left-0 w-full h-[50vh] z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-surface/80 to-surface z-10 pointer-events-none"></div>
          <img src="/assets/bg-mountain.png" alt="Mountain Background" className="w-full h-full object-cover object-top opacity-80" />
        </div>

        <main className="flex-1 overflow-y-auto overflow-x-hidden flex flex-col relative z-10">
          <div className="w-full min-h-full flex flex-col pt-24 pb-8">
            
            {/* Hero Section */}
            <div className="flex flex-col items-center justify-center text-center px-6 relative z-10 mt-8 mb-4">
              <img src="/assets/crystal-ball.png" alt="Crystal Ball" className="w-20 h-20 mb-4 object-contain drop-shadow-[0_0_15px_rgba(167,139,250,0.5)]" />
              <h1 className="text-5xl font-headline-xl font-bold text-white tracking-tight mb-4 drop-shadow-md">
                Multimodal <span className="text-primary-inverse text-[#a78bfa]">RAG</span>
              </h1>
              <p className="text-on-surface-variant text-base max-w-lg leading-relaxed drop-shadow-sm font-medium">
                Upload PDFs with text, images & charts — ask anything.<br />
                Powered by <span className="text-[#a78bfa]">Groq</span>.
              </p>
            </div>

            <StatsGrid />
            <EmptyState />
            
          </div>
        </main>
      </div>
    </>
  );
}
