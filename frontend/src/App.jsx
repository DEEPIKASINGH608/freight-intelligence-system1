import { useState, useEffect } from 'react';

export default function App() {
  const [apiStatus, setApiStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);
  const [decisionData, setDecisionData] = useState(null);

  // Form & Simulator Inputs
  const [formData, setFormData] = useState({
    origin: 'Australia',
    destination: 'Paradip',
    cargo_type: 'iron_ore',
    cargo_quantity_tons: 75000,
    delivery_deadline_days: 30,
    current_freight_rate: 22.50,
    bunker_fuel_price: 620.00,
    cargo_demand_index: 105.0,
    vessel_availability_index: 92.0,
    port_congestion_days: 2.5,
    route_distance_nm: 3850.0,
    weather_risk_index: 1.1
  });

  // Check backend health on mount
  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then((res) => res.json())
      .then((data) => {
        setApiStatus(data);
        setLoading(false);
        handleEvaluate(); // Initial evaluation run
      })
      .catch((err) => {
        console.error('Error connecting to backend:', err);
        setLoading(false);
      });
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleEvaluate = () => {
    setEvaluating(true);
    fetch('http://127.0.0.1:8000/api/v1/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
      .then((res) => res.json())
      .then((data) => {
        setDecisionData(data);
        setEvaluating(false);
      })
      .catch((err) => {
        console.error('Error running evaluation:', err);
        setEvaluating(false);
      });
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', color: '#f8fafc', backgroundColor: '#0f172a', minHeight: '100vh' }}>
      {/* Header & Status */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: 0 }}>Freight Intelligence System</h1>
          <p style={{ color: '#94a3b8', margin: '0.25rem 0 0 0' }}>SIH Operational Command Center & AI Decision Engine</p>
        </div>
        <div>
          {loading ? (
            <span style={{ color: '#fbbf24' }}>Connecting...</span>
          ) : apiStatus ? (
            <span style={{ backgroundColor: '#065f46', color: '#34d399', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.875rem' }}>
              Backend Online (v{apiStatus.version || '1.0'})
            </span>
          ) : (
            <span style={{ backgroundColor: '#991b1b', color: '#fca5a5', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.875rem' }}>
              Backend Offline
            </span>
          )}
        </div>
      </div>

      <hr style={{ borderColor: '#334155', margin: '1.5rem 0' }} />

      {/* Main Grid Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem' }}>

        {/* Left Column: Parameter & What-If Simulator Inputs */}
        <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '8px', border: '1px solid #334155' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, marginBottom: '1rem', color: '#38bdf8' }}>What-If Simulator Inputs</h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Current Freight Rate ($/ton): {formData.current_freight_rate}</label>
              <input
                type="range" min="10" max="50" step="0.5"
                name="current_freight_rate" value={formData.current_freight_rate}
                onChange={handleInputChange} style={{ width: '100%' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Bunker Fuel Price ($/ton): {formData.bunker_fuel_price}</label>
              <input
                type="range" min="400" max="1000" step="10"
                name="bunker_fuel_price" value={formData.bunker_fuel_price}
                onChange={handleInputChange} style={{ width: '100%' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Port Congestion (Days): {formData.port_congestion_days}</label>
              <input
                type="range" min="0" max="10" step="0.5"
                name="port_congestion_days" value={formData.port_congestion_days}
                onChange={handleInputChange} style={{ width: '100%' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Cargo Demand Index: {formData.cargo_demand_index}</label>
              <input
                type="range" min="80" max="130" step="1"
                name="cargo_demand_index" value={formData.cargo_demand_index}
                onChange={handleInputChange} style={{ width: '100%' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Vessel Availability Index: {formData.vessel_availability_index}</label>
              <input
                type="range" min="70" max="120" step="1"
                name="vessel_availability_index" value={formData.vessel_availability_index}
                onChange={handleInputChange} style={{ width: '100%' }}
              />
            </div>

            <button
              onClick={handleEvaluate}
              disabled={evaluating}
              style={{
                backgroundColor: '#0284c7', color: '#fff', border: 'none', padding: '0.75rem',
                borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', marginTop: '0.5rem'
              }}
            >
              {evaluating ? 'Evaluating Scenario...' : 'Run Decision Engine'}
            </button>
          </div>
        </div>

        {/* Right Column: Decision Dashboard Results */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

          {decisionData ? (
            <>
              {/* Actionable Decision Banner */}
              <div style={{
                background: decisionData.recommended_action === 'CHARTER NOW' ? '#064e3b' : '#78350f',
                border: `1px solid ${decisionData.recommended_action === 'CHARTER NOW' ? '#059669' : '#d97706'}`,
                padding: '1.25rem', borderRadius: '8px'
              }}>
                <div style={{ fontSize: '0.875rem', color: '#cbd5e1', textTransform: 'uppercase' }}>Recommended Action</div>
                <div style={{ fontSize: '1.75rem', fontWeight: 'bold', margin: '0.25rem 0' }}>{decisionData.recommended_action}</div>
                <p style={{ margin: 0, fontSize: '0.95rem', color: '#e2e8f0' }}>{decisionData.reasoning}</p>
              </div>

              {/* Forecast & Interval Card */}
              <div style={{ background: '#1e293b', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
                <h3 style={{ margin: '0 0 0.75rem 0', fontSize: '1rem', color: '#38bdf8' }}>30-Day Freight Forecast & Range</h3>

                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', marginBottom: '1rem' }}>
                  <span style={{ fontSize: '2rem', fontWeight: 'bold', color: '#34d399' }}>
                    ${decisionData.forecast_module?.predicted_30d_rate_usd || decisionData.financial_summary?.forecast_rate_usd_ton}
                  </span>
                  <span style={{ color: '#94a3b8' }}>/ ton</span>
                  <span style={{ marginLeft: 'auto', fontSize: '0.875rem', color: decisionData.financial_summary?.rate_change_pct > 0 ? '#f87171' : '#34d399' }}>
                    ({decisionData.financial_summary?.rate_change_pct > 0 ? '+' : ''}{decisionData.financial_summary?.rate_change_pct}%)
                  </span>
                </div>

                {/* Prediction Interval Bar */}
                {decisionData.forecast_module?.forecast_range && (
                  <div style={{ background: '#0f172a', padding: '0.75rem', borderRadius: '6px', marginBottom: '1rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                      <span>Low: ${decisionData.forecast_module.forecast_range.lower_bound_usd}</span>
                      <span style={{ fontWeight: 'bold', color: '#cbd5e1' }}>90% Prediction Band</span>
                      <span>High: ${decisionData.forecast_module.forecast_range.upper_bound_usd}</span>
                    </div>
                    <div style={{ width: '100%', backgroundColor: '#334155', height: '6px', borderRadius: '3px' }}>
                      <div style={{ backgroundColor: '#10b981', height: '100%', width: '60%', margin: '0 auto', borderRadius: '3px' }}></div>
                    </div>
                  </div>
                )}

                {/* Statistical Proof Metrics */}
                {decisionData.forecast_module?.baseline_comparison && (
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.8%rem', borderTop: '1px solid #334155', paddingTop: '0.75rem' }}>
                    <div>
                      <span style={{ color: '#94a3b8' }}>XGBoost Model MAE:</span>
                      <div style={{ fontWeight: 'bold' }}>${decisionData.forecast_module.baseline_comparison.model_mae_usd} / ton</div>
                    </div>
                    <div>
                      <span style={{ color: '#94a3b8' }}>Persistence Baseline MAE:</span>
                      <div style={{ fontWeight: 'bold' }}>${decisionData.forecast_module.baseline_comparison.naive_persistence_mae_usd} / ton</div>
                    </div>
                  </div>
                )}
              </div>

              {/* Port Constraints Card */}
              {/* Scenario Comparison Panel */}
              {decisionData?.scenario_analysis && (
                <div style={{ background: '#1e293b', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
                  <h3 style={{ margin: '0 0 0.75rem 0', fontSize: '0.95rem', color: '#38bdf8' }}>
                    Scenario Analysis (BOOK NOW vs WAIT)
                  </h3>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.75rem', fontSize: '0.85rem' }}>
                    <div style={{ background: '#0f172a', padding: '0.5rem', borderRadius: '4px' }}>
                      <span style={{ color: '#94a3b8', display: 'block' }}>Book Today</span>
                      <strong style={{ fontSize: '1rem', color: '#f8fafc' }}>
                        ₹{decisionData.scenario_analysis.scenario_book_now_inr_cr} Cr
                      </strong>
                    </div>
                    <div style={{ background: '#0f172a', padding: '0.5rem', borderRadius: '4px' }}>
                      <span style={{ color: '#94a3b8', display: 'block' }}>Wait 30 Days</span>
                      <strong style={{ fontSize: '1rem', color: '#f8fafc' }}>
                        ₹{decisionData.scenario_analysis.scenario_wait_30d_inr_cr} Cr
                      </strong>
                    </div>
                    <div style={{ background: '#0f172a', padding: '0.5rem', borderRadius: '4px' }}>
                      <span style={{ color: '#94a3b8', display: 'block' }}>Cost Delta</span>
                      <strong style={{ fontSize: '1rem', color: '#34d399' }}>
                        ₹{decisionData.scenario_analysis.exposure_delta_inr_cr} Cr
                      </strong>
                    </div>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.5rem' }}>
                    Basis: {decisionData.scenario_analysis.basis}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div style={{ background: '#1e293b', padding: '2rem', borderRadius: '8px', textAlign: 'center', color: '#94a3b8' }}>
              Loading decision telemetry...
            </div>
          )}

        </div>

      </div>
    </div>
  );
}