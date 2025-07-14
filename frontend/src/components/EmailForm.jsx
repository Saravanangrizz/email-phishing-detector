import React, { useState } from 'react';
import axios from 'axios';

const keywords = ['verify','account','login','urgent','click','password','bank'];

const highlightKeywords = (text) => {
  const pattern = new RegExp(`(${keywords.join('|')})`, 'gi');
  return text.replace(pattern, '<mark class="bg-yellow-200">$1</mark>');
};

function EmailForm() {
  const [email, setEmail] = useState('');
  const [from, setFrom] = useState('');
  const [replyTo, setReplyTo] = useState('');
  const [result, setResult] = useState({});
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult({});
    try {
      const res = await axios.post('https://your-backend.onrender.com/predict', {
        email,
        from,
        reply_to: replyTo
      });
      setResult(res.data);
    } catch {
      setResult({ prediction: 'Error', confidence: 0, explanation: [] });
    }
    setLoading(false);
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 to-purple-100 min-h-screen flex justify-center items-center">
      <div className="bg-white rounded-2xl shadow-2xl p-10 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">Phishing Detector</h1>
        <form onSubmit={onSubmit}>
          <input
            type="text"
            placeholder="From (email)"
            className="w-full p-3 mb-3 border rounded-lg focus:outline-none"
            value={from}
            onChange={(e) => setFrom(e.target.value)}
          />
          <input
            type="text"
            placeholder="Reply-To (email)"
            className="w-full p-3 mb-3 border rounded-lg focus:outline-none"
            value={replyTo}
            onChange={(e) => setReplyTo(e.target.value)}
          />
          <textarea
            rows="6"
            placeholder="Paste email content..."
            className="w-full p-4 border rounded-xl focus:outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button
            type="submit"
            className="w-full mt-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:opacity-90 transition"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>

        {result.prediction && (
          <div className="mt-6 animate-fade-in">
            <div className={`text-center text-xl font-semibold ${result.prediction === 'Phishing' ? 'text-red-600' : 'text-green-600'}`}>
              {result.prediction} ({result.confidence}%)
            </div>
            {result.explanation.length > 0 && (
              <div className="mt-4 text-gray-700">
                <p><strong>Why:</strong> Suspicious keywords detected:</p>
                <p dangerouslySetInnerHTML={{ __html: result.explanation.join(', ') }} />
              </div>
            )}
            <div className="mt-4 text-left p-4 bg-gray-50 rounded">
              <p className="text-sm">Content with highlights:</p>
              <div
                className="prose text-sm"
                dangerouslySetInnerHTML={{ __html: highlightKeywords(email) }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default EmailForm;
