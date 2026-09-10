import React from 'react';

export default function RiskBadge({ level }) {
  const getBadgeStyle = () => {
    switch (level?.toUpperCase()) {
      case 'HIGH':
        return { bg: '#7f1d1d', border: '#ef4444', text: '#fca5a5' };
      case 'MEDIUM':
        return { bg: '#78350f', border: '#f59e0b', text: '#fde68a' };
      case 'LOW':
      default:
        return { bg: '#064e3b', border: '#10b981', text: '#a7f3d0' };
    }
  };

  const style = getBadgeStyle();

  return (
    <span style={{
      backgroundColor: style.bg,
      border: `1px solid ${style.border}`,
      color: style.text,
      padding: '0.25rem 0.6rem',
      borderRadius: '4px',
      fontSize: '0.75rem',
      fontWeight: 'bold',
      textTransform: 'uppercase',
      display: 'inline-block'
    }}>
      {level || 'LOW'} RISK
    </span>
  );
}