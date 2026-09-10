import React from 'react';

export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'command', label: 'Command Center' },
    { id: 'forecast', label: 'Freight Forecast' },
    { id: 'vessels', label: 'Vessel Optimization' },
    { id: 'simulator', label: 'What-If Simulator' }
  ];

  return (
    <header style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '1rem 2rem',
      backgroundColor: '#0f172a',
      borderBottom: '1px solid #334155'
    }}>
      <h2 style={{ margin: 0, color: '#38bdf8', fontSize: '1.25rem' }}>Freight Intelligence System</h2>
      <nav style={{ display: 'flex', gap: '1rem' }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              background: activeTab === tab.id ? '#1e293b' : 'transparent',
              color: activeTab === tab.id ? '#38bdf8' : '#94a3b8',
              border: activeTab === tab.id ? '1px solid #0284c7' : 'none',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '500'
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </header>
  );
}