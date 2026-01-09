'use client';

import { useState } from 'react';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const res = await fetch(
        `http://0.0.0.0:8000/chat?mess=${encodeURIComponent(message)}`,
        {
          method: 'GET',
        }
      );

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setAnswer(data.ans);
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="w-full max-w-3xl p-6 space-y-6 border border-gray-700 rounded-xl">
        <h1 className="text-2xl font-bold text-center">
          PDF Chat Assistant
        </h1>

        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask a question from the PDF..."
          className="w-full h-32 p-3 bg-gray-900 border border-gray-700 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="w-full py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-md font-semibold"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>

        {error && (
          <div className="text-red-400 text-sm">
            {error}
          </div>
        )}

        {answer && (
          <div className="p-4 bg-gray-900 border border-gray-700 rounded-md whitespace-pre-wrap">
            <h2 className="font-semibold mb-2">Answer</h2>
            {answer}
          </div>
        )}
      </div>
    </main>
  );
}
