import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import StatsGrid from "./components/StatsGrid";
import EmptyState from "./components/EmptyState";
import ChatInput from "./components/ChatInput";

export default function App() {
  return (
    <>
      <Sidebar />
      <div className="flex-1 md:ml-64 flex flex-col h-screen relative bg-surface-bright">
        <Header />
        <main className="flex-1 overflow-y-auto p-lg md:p-xl flex flex-col items-center relative w-full">
          <div className="w-full max-w-5xl flex flex-col h-full gap-lg relative z-0 mx-auto">
            <StatsGrid />
            <EmptyState />
            <ChatInput />
          </div>
        </main>
      </div>
    </>
  );
}
