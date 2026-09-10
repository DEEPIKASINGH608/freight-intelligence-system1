import React from 'react';
import KPICard from '../components/common/KPICard';
import RiskBadge from '../components/common/RiskBadge';

export default function CommandCenter({ decisionData }) {
  if (!decisionData) {
    return <p style={{ color: '#94a3b8' }}>Run decision evaluation to view real-time market command center analytics.</p>;
  }

  const { scenario_analysis, financial_summary, risk_module, recommended_action, reasoning } = decisionData;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Top Banner Recommendation */}
      <div style={{
        background: recommended_action === 'CHARTER NOW' ? '#064e3b' : '#1e293b',
        border: `1px solid ${recommended_action === 'CHARTER NOW' ? '#059669' : '#334155'}`,
        padding: '1.25rem',
        borderRadius: '8px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.85rem', color: '#cbd5e1', textTransform: 'uppercase' }}>Recommended Executive Action</span>
          <RiskBadge level={risk_module?.risk_level} />
        </div>
        <h2 style={{ margin: '0.5rem 0', color: '#f8fafc' }}>{recommended_action}</h2>
        <p style={{ margin: 0, color: '#cbd5e1', fontSize: '0.9rem' }}>{reasoning}</p>
      </div>

      {/* Primary KPI Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <KPICard
          title="Current Freight Spot"
          value={`$${financial_summary?.current_rate_usd_ton}`}
          unit="/ ton"
          subtitle="Baseline Spot Market"
        />
        <KPICard
          title="30-Day Forecast"
          value={`$${financial_summary?.forecast_rate_usd_ton}`}
          unit="/ ton"
          subtitle={`${financial_summary?.rate_change_pct > 0 ? '+' : ''}${financial_summary?.rate_change_pct}% projected`}
          trendColor={financial_summary?.rate_change_pct > 0 ? '#ef4444' : '#34d399'}
        />
        <KPICard
          title="Total Cargo Exposure"
          value={`₹${scenario_analysis?.scenario_book_now_inr_cr}`}
          unit="Cr"
          subtitle="Current Charter Estimate"
        />
        <KPICard
          title="Scenario Exposure Delta"
          value={`₹${scenario_analysis?.exposure_delta_inr_cr}`}
          unit="Cr"
          subtitle="Book Now vs Wait Delta"
        />
      </div>

      {/* Scenario Analysis Detail Box */}
      <div style={{ background: '#1e293b', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 1rem 0', color: '#38bdf8', fontSize: '1rem' }}>Market Scenario Breakdown</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
          <div style={{ background: '#0f172a', padding: '0.85rem', borderRadius: '6px' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Book Today Scenario</span>
            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#f8fafc', marginTop: '0.25rem' }}>
              ₹{scenario_analysis?.scenario_book_now_inr_cr} Cr
            </div>
          </div>
          <div style={{ background: '#0f172a', padding: '0.85rem', borderRadius: '6px' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Wait 30 Days Scenario</span>
            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#f8fafc', marginTop: '0.25rem' }}>
              ₹{scenario_analysis?.scenario_wait_30d_inr_cr} Cr
            </div>
          </div>
          <div style={{ background: '#0f172a', padding: '0.85rem', borderRadius: '6px' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Exposure Variance</span>
            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#34d399', marginTop: '0.25rem' }}>
              ₹{scenario_analysis?.exposure_delta_inr_cr} Cr
            </div>
          </div>
        </div>
        <p style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.75rem', margin: 0 }}>
          Basis: {scenario_analysis?.basis}
        </p>
      </div>
    </div>
  );
}
