import React, { useState } from 'react';
import axios from 'axios';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await axios.post('/token', new URLSearchParams({ username, password }));
      localStorage.setItem('aifolio_token', res.data.access_token);
      onLogin();
    } catch (err) {
      setError('Invalid credentials.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-700">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-3xl font-bold mb-6 text-center text-gray-900">AIFOLIO Login</h2>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Username</label>
          <input
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            autoFocus
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 mb-2">Password</label>
          <input
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-blue-600 to-blue-400 text-white font-bold py-2 rounded hover:from-blue-700 hover:to-blue-500 transition"
        >
          Login
        </button>
      </form>
    </div>
  );
}
