import { useState, useEffect } from 'react';

export default function App() {
  const [apiStatus, setApiStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then((res) => res.json())
      .then((data) => {
        setApiStatus(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error connecting to backend:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', color: '#f8fafc', backgroundColor: '#0f172a', minHeight: '100vh' }}>
      <h1>Freight Intelligence System</h1>
      <hr style={{ borderColor: '#334155', margin: '1rem 0' }} />

      <h2>Backend Connection Status</h2>
      {loading ? (
        <p>Connecting to FastAPI backend...</p>
      ) : apiStatus ? (
        <div style={{ background: '#1e293b', padding: '1rem', borderRadius: '8px', border: '1px solid #475569' }}>
          <p><strong>Status:</strong> {apiStatus.status}</p>
          <p><strong>System:</strong> {apiStatus.system}</p>
          <p><strong>Version:</strong> {apiStatus.version}</p>
        </div>
      ) : (
        <p style={{ color: '#ef4444' }}>Unable to reach backend at http://127.0.0.1:8000</p>
      )}
    </div>
  );
}