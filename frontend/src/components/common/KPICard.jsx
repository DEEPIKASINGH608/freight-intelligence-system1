import React from 'react';

export default function KPICard({ title, value, unit, subtitle, trendColor = '#34d399' }) {
  return (
    <div style={{
      background: '#1e293b',
      padding: '1.25rem',
      borderRadius: '8px',
      border: '1px solid #334155',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }}>
      <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontWeight: '500' }}>{title}</span>
      <div style={{ fontSize: '1.75rem', fontWeight: 'bold', color: '#f8fafc', margin: '0.5rem 0' }}>
        {value} {unit && <span style={{ fontSize: '0.9rem', color: '#64748b', fontWeight: 'normal' }}>{unit}</span>}
      </div>
      {subtitle && (
        <span style={{ fontSize: '0.75rem', color: trendColor }}>
          {subtitle}
        </span>
      )}
    </div>
  );
}

