/**
 * API client for the Multimodal RAG backend.
 * Centralized fetch wrapper for all endpoints.
 */

const API_BASE = "http://localhost:8000/api";

async function handleResponse(res) {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "API request failed");
  }
  return res.json();
}

/** Upload a PDF file for ingestion. */
export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });
  return handleResponse(res);
}

/** Get list of indexed document names. */
export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  return handleResponse(res);
}

/** Delete a specific document from the index. */
export async function deleteDocument(fileName) {
  const res = await fetch(`${API_BASE}/documents/${encodeURIComponent(fileName)}`, {
    method: "DELETE",
  });
  return handleResponse(res);
}

/** Ask a question about the indexed documents. */
export async function askQuestion(question) {
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handleResponse(res);
}

/** Get document and chunk counts. */
export async function getStats() {
  const res = await fetch(`${API_BASE}/stats`);
  return handleResponse(res);
}

/** Clear the entire index. */
export async function clearIndex() {
  const res = await fetch(`${API_BASE}/index`, {
    method: "DELETE",
  });
  return handleResponse(res);
}
