/**
 * React Context for global application state.
 * Provides: documents, chat history, stats, processing state, and actions.
 */

import { createContext, useContext, useState, useCallback, useEffect } from "react";
import * as api from "./api";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [documents, setDocuments] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [stats, setStats] = useState({ document_count: 0, chunk_count: 0 });
  const [isProcessing, setIsProcessing] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState(null);

  // ── Fetch initial data ──
  const refreshData = useCallback(async () => {
    try {
      const [docRes, statsRes] = await Promise.all([
        api.getDocuments(),
        api.getStats(),
      ]);
      setDocuments(docRes.documents || []);
      setStats(statsRes);
      setError(null);
    } catch (err) {
      setError("Cannot connect to API. Start the backend with: python api.py");
    }
  }, []);

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  // ── Actions ──

  const uploadFile = useCallback(async (file) => {
    setIsProcessing(true);
    setError(null);
    try {
      const result = await api.uploadPDF(file);
      await refreshData();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsProcessing(false);
    }
  }, [refreshData]);

  const deleteDocument = useCallback(async (fileName) => {
    try {
      await api.deleteDocument(fileName);
      await refreshData();
    } catch (err) {
      setError(err.message);
    }
  }, [refreshData]);

  const askQuestion = useCallback(async (question) => {
    // Add user message immediately
    setChatHistory((prev) => [...prev, { role: "user", content: question }]);
    setIsAsking(true);

    try {
      const result = await api.askQuestion(question);
      setChatHistory((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
          sources: result.sources,
          image_refs: result.image_refs,
        },
      ]);
      // Update stats (questions asked is derived from chatHistory length)
      await refreshData();
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${err.message}`, sources: [], image_refs: [] },
      ]);
    } finally {
      setIsAsking(false);
    }
  }, [refreshData]);

  const clearAllData = useCallback(async () => {
    try {
      await api.clearIndex();
      setChatHistory([]);
      await refreshData();
    } catch (err) {
      setError(err.message);
    }
  }, [refreshData]);

  const questionsAsked = chatHistory.filter((m) => m.role === "user").length;

  const value = {
    documents,
    chatHistory,
    stats: { ...stats, questions_asked: questionsAsked },
    isProcessing,
    isAsking,
    error,
    uploadFile,
    deleteDocument,
    askQuestion,
    clearAllData,
    refreshData,
    setError,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
