"use client";

import { useState } from "react";

type Summary = {
  meeting_overview: string;
  discussion_points: string[];
  decisions: string[];
  action_items: string[];
  open_questions: string[];
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleUpload() {
    if (!file) return;

    setLoading(true);
    setError(null);
    setSummary(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("https://meeting-summarizer-tmi0.onrender.com/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      setError("Something went wrong. Check your backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-2xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-2 tracking-tight">
          Meeting Summarizer
        </h1>
        <p className="text-slate-400 mb-1">
          Upload a recording and get a structured summary — key points,
          decisions, action items, and open questions.
        </p>
        <p className="text-slate-500 text-sm mb-8">
          Approx. processing time: ~15 min for 1 hour of audio, ~25 min for 2 hours.
        </p>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            <label className="flex-1 w-full">
              <input
                type="file"
                accept=".mp3,.wav,.m4a,.mp4,.ogg"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 cursor-pointer"
              />
            </label>
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-lg font-medium disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
            >
              {loading ? "Processing..." : "Summarize"}
            </button>
          </div>
          {loading && (
            <p className="text-slate-500 text-sm mt-3">
              This can take several minutes for longer recordings — sit tight.
            </p>
          )}
        </div>

        {error && (
          <div className="bg-red-950 border border-red-900 text-red-300 rounded-lg p-4 mb-8">
            {error}
          </div>
        )}

        {summary && (
          <div className="space-y-6">
            <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-2 text-indigo-400">
                Overview
              </h2>
              <p className="text-slate-300">{summary.meeting_overview}</p>
            </section>

            <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-2 text-indigo-400">
                Discussion Points
              </h2>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                {summary.discussion_points.map((point, i) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>
            </section>

            <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-2 text-indigo-400">
                Decisions
              </h2>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                {summary.decisions.map((d, i) => (
                  <li key={i}>{d}</li>
                ))}
              </ul>
            </section>

            <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-2 text-indigo-400">
                Action Items
              </h2>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                {summary.action_items.map((a, i) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </section>

            <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-2 text-indigo-400">
                Open Questions
              </h2>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                {summary.open_questions.map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ul>
            </section>
          </div>
        )}

        <footer className="mt-16 pt-6 border-t border-slate-800 text-slate-500 text-sm">
          Built by Ebenezer (@EbenezerDYOR)
        </footer>
      </div>
    </div>
  );
}