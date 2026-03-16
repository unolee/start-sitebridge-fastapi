import { useEffect, useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import { fetchApi } from "./api";

function Nav() {
  return (
    <nav className="flex gap-4 p-4 bg-zinc-900 text-white">
      <Link to="/" className="font-semibold hover:text-blue-400">
        Home
      </Link>
      <Link to="/about" className="font-semibold hover:text-blue-400">
        About
      </Link>
    </nav>
  );
}

function Home() {
  const [data, setData] = useState<{ message: string; timestamp: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchApi<{ message: string; timestamp: string }>("/api/hello")
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">SiteBridge + FastAPI</h1>
      <p className="text-zinc-600 mb-6">
        Your full-stack app is up and running. Edit the client and server to get started.
      </p>
      <div className="bg-zinc-100 rounded-lg p-4">
        <h2 className="text-sm font-semibold text-zinc-500 mb-2">API Response</h2>
        {error ? (
          <p className="text-red-600">Error: {error}</p>
        ) : data ? (
          <pre className="text-sm text-zinc-800">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <p className="text-zinc-400">Loading...</p>
        )}
      </div>
    </div>
  );
}

function About() {
  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">About</h1>
      <p className="text-zinc-600">
        This is a FastAPI + Vite React SPA boilerplate designed for deployment through SiteBridge.
      </p>
      <ul className="mt-4 list-disc list-inside text-zinc-600 space-y-1">
        <li>FastAPI backend with SQLite (WAL mode)</li>
        <li>React 19 with React Router</li>
        <li>Tailwind CSS v4</li>
        <li>Vite for fast development and builds</li>
        <li>GitHub Actions CI/CD pipeline</li>
      </ul>
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  );
}
