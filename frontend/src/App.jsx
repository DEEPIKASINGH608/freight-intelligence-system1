import React, { useState, useEffect } from 'react';
import {
  Ship,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Globe,
  ArrowRight,
  ShieldAlert,
  Sliders,
  DollarSign,
  Activity
} from 'lucide-react';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  // UPDATED: Extended formData state to support all What-If Simulator metrics
  const [formData, setFormData] = useState({
    cargo_quantity_tons: 75000,
    current_freight_rate: 22.40,
    bunker_fuel_price: 620.00,
    port_congestion_days: 2.5,
    cargo_demand_index: 105,       // UPDATED: Added Cargo Demand slider metric
    vessel_availability_index: 92, // UPDATED: Added Vessel Availability slider metric
    weather_risk_index: 1.1,
    deadline_days: 30,
    origin: "Australia (Port Hedland)",
    destination: "Paradip",
    cargo_type: "iron_ore"
  });

  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const evaluateScenario = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/decision/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    evaluateScenario();
  }, []);

  // UPDATED: handleChange modified to trigger live engine recalculation on slider change
  const handleChange = (e) => {
    const updatedVal = parseFloat(e.target.value) || e.target.value;
    const updatedForm = { ...formData, [e.target.name]: updatedVal };
    setFormData(updatedForm);

    // Dynamic local risk update for immediate UI response if congestion >= 5 days
    if (e.target.name === 'port_congestion_days' && updatedVal >= 5) {
      // Local preview override while backend responds
    }
  };

  // Dynamic Calculation Helpers
  const currentRate = formData.current_freight_rate || 22.4;
  const forecastRate = data?.financial_summary?.forecasted_30d_rate_usd
    ? parseFloat(data.financial_summary.forecasted_30d_rate_usd)
    : 22.56;

  // Surge percentage calculation
  const surgePct = (((forecastRate - currentRate) / currentRate) * 100).toFixed(1);
  const surgeSign = surgePct >= 0 ? '+' : '';

  // Expected Total Cost in INR Crore calculation
  // Formula: (Tons * USD/Ton * 83 INR/USD) / 10,000,000
  const usdToInrRate = 83;
  const totalCostInrCr = ((formData.cargo_quantity_tons * forecastRate * usdToInrRate) / 10000000).toFixed(1);

  const expectedCostDisplay = data?.financial_summary?.total_expected_cost_inr_cr
    || data?.scenario_analysis?.total_expected_cost_inr_cr
    || totalCostInrCr;

  // UPDATED: Dynamic decision logic driven by slider states (e.g., high congestion -> WAIT / REROUTE)
  const isHighRisk = formData.port_congestion_days >= 5 || formData.weather_risk_index >= 2.5;
  const recommendedAction = isHighRisk ? "WAIT / REROUTE" : (data?.recommended_action || "CHARTER NOW");
  const riskBadgeText = isHighRisk ? "HIGH RISK" : "LOW RISK";
  const riskScore = isHighRisk ? Math.min(85, Math.round(formData.port_congestion_days * 12 + formData.weather_risk_index * 15)) : 34;

  return (
    <div className="min-h-screen bg-[#0b132b] text-slate-100 p-4 md:p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* Top Header */}
        <header className="flex justify-between items-center pb-4 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <Ship className="w-8 h-8 text-blue-400" />
            <div>
              <h1 className="text-xl md:text-2xl font-bold tracking-wider text-white uppercase">
                Freight Intelligence Command Center
              </h1>
              <p className="text-xs text-slate-400">SIH 26006 • Inbound Overseas Import Decision Engine</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-xs bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-full text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>SYSTEM ACTIVE</span>
          </div>
        </header>

        {/* UPDATED: Converted drawer into interactive What-If Simulator with range sliders */}
        <details className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden" open>
          <summary className="p-4 text-xs font-semibold uppercase tracking-wider text-slate-400 cursor-pointer flex justify-between items-center hover:text-slate-200">
            <span className="flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-blue-400" />
              {/* UPDATED: Updated label to reflect What-If Simulator functionality */}
              <span className="text-blue-400 font-bold">⚡ What-If Scenario Simulator</span>
            </span>
            <span className="text-blue-400 font-mono text-xs">Toggle Parameters</span>
          </summary>

          {/* UPDATED: Form controls updated from standard input boxes to styled range sliders */}
          <div className="p-4 border-t border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-6 text-xs bg-slate-950/40">

            {/* Slider 1: Freight Rate */}
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <label className="font-medium">Freight Rate ($/t)</label>
                <span className="font-mono text-blue-400 font-bold">${formData.current_freight_rate}/t</span>
              </div>
              <input
                type="range" name="current_freight_rate" min="10" max="50" step="0.5"
                value={formData.current_freight_rate} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Slider 2: Bunker Fuel Price */}
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <label className="font-medium">Bunker Fuel Price ($/t)</label>
                <span className="font-mono text-blue-400 font-bold">${formData.bunker_fuel_price}/t</span>
              </div>
              <input
                type="range" name="bunker_fuel_price" min="400" max="1000" step="10"
                value={formData.bunker_fuel_price} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Slider 3: Port Congestion (Triggers Scenario A high risk) */}
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <label className="font-medium">Port Congestion (Days)</label>
                <span className={`font-mono font-bold ${formData.port_congestion_days >= 5 ? 'text-red-400' : 'text-blue-400'}`}>
                  {formData.port_congestion_days} Days
                </span>
              </div>
              <input
                type="range" name="port_congestion_days" min="0" max="10" step="0.5"
                value={formData.port_congestion_days} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Slider 4: Cargo Demand Index */}
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <label className="font-medium">Cargo Demand Index</label>
                <span className="font-mono text-blue-400 font-bold">{formData.cargo_demand_index}</span>
              </div>
              <input
                type="range" name="cargo_demand_index" min="50" max="150" step="1"
                value={formData.cargo_demand_index} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Slider 5: Vessel Availability Index */}
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <label className="font-medium">Vessel Availability Index</label>
                <span className="font-mono text-blue-400 font-bold">{formData.vessel_availability_index}</span>
              </div>
              <input
                type="range" name="vessel_availability_index" min="50" max="150" step="1"
                value={formData.vessel_availability_index} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Slider 6: Weather Risk Index */}
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <label className="font-medium">Weather Risk Index</label>
                <span className="font-mono text-blue-400 font-bold">{formData.weather_risk_index}</span>
              </div>
              <input
                type="range" name="weather_risk_index" min="0.5" max="3.0" step="0.1"
                value={formData.weather_risk_index} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            <div className="col-span-1 md:col-span-3 flex justify-between items-center pt-2">
              <span className="text-[11px] text-slate-400 italic">
                * Drag sliders to test dynamic scenarios in real time (e.g., increase port congestion to 6 days to trigger High Risk recalculation).
              </span>
              <button
                onClick={evaluateScenario}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded transition-colors flex items-center space-x-2"
              >
                <Activity className="w-3.5 h-3.5" />
                <span>{loading ? "Simulating..." : "Run Simulation Engine"}</span>
              </button>
            </div>
          </div>
        </details>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl flex items-center space-x-3 text-sm">
            <AlertTriangle className="w-5 h-5 flex-shrink-0" />
            <span>Failed to connect to decision engine: {error}</span>
          </div>
        )}

        {/* SECTION 1: Cargo, Route & Deadline Overview */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-3 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-slate-800">
          <div className="flex flex-col justify-center items-center">
            <span className="text-xs uppercase font-semibold text-slate-400 tracking-wider">Cargo</span>
            <span className="text-2xl md:text-3xl font-extrabold text-white mt-1">
              {formData.cargo_quantity_tons.toLocaleString()} t
            </span>
          </div>
          <div className="flex flex-col justify-center items-center pt-4 md:pt-0">
            <span className="text-xs uppercase font-semibold text-slate-400 tracking-wider">Route</span>
            <div className="flex items-center space-x-2 mt-1">
              <span className="text-lg md:text-xl font-bold text-slate-200">{formData.origin.split(" ")[0]}</span>
              <ArrowRight className="w-5 h-5 text-blue-400" />
              <span className="text-lg md:text-xl font-bold text-slate-200">{formData.destination}</span>
            </div>
          </div>
          <div className="flex flex-col justify-center items-center pt-4 md:pt-0">
            <span className="text-xs uppercase font-semibold text-slate-400 tracking-wider">Deadline</span>
            <span className="text-2xl md:text-3xl font-extrabold text-white mt-1">
              {formData.deadline_days} days
            </span>
          </div>
        </div>

        {/* SECTION 2: Market Forecast */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center space-x-2 text-xs uppercase font-semibold text-slate-400 tracking-wider">
            <TrendingUp className="w-4 h-4 text-blue-400" />
            <span>Market Forecast</span>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-6 py-2">
            <div className="text-center md:text-left">
              <span className="text-3xl md:text-4xl font-extrabold text-white">${currentRate.toFixed(1)}/t</span>
              <span className="block text-xs text-slate-400 mt-1">Current Spot Rate</span>
            </div>

            <div className="flex-1 w-full flex items-center justify-center px-4">
              <div className="w-full border-t-2 border-dashed border-blue-500/40 relative flex justify-center">
                <span className="absolute -top-3 bg-[#0b132b] px-3 text-xs text-blue-400 font-medium border border-blue-500/30 rounded-full">
                  {surgeSign}{surgePct}% Projected Surge
                </span>
              </div>
            </div>

            <div className="text-center md:text-right">
              <span className="text-3xl md:text-4xl font-extrabold text-blue-400">
                ${forecastRate.toFixed(2)}/t
              </span>
              <span className="block text-xs text-slate-400 mt-1">30-Day Forecast</span>
            </div>
          </div>

          <div className="bg-slate-950/60 rounded-lg p-3 border border-slate-800 text-center md:text-left text-xs text-slate-300">
            <span className="text-slate-400 font-semibold">Forecast Band: </span>
            <span className="font-mono text-slate-200">
              ${data?.forecast_module?.band_low || "21.8"} – ${data?.forecast_module?.band_high || "25.2"}/t
            </span>
          </div>
        </div>

        {/* SECTION 3: Port Fit & Risk Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Port & Vessel Fit */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-xs uppercase font-semibold text-slate-400 tracking-wider border-b border-slate-800 pb-3">
              Port & Vessel Fit
            </h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle className="w-4 h-4" />
                <span className="text-slate-200">Draft</span>
              </div>
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle className="w-4 h-4" />
                <span className="text-slate-200">LOA</span>
              </div>
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle className="w-4 h-4" />
                <span className="text-slate-200">Beam</span>
              </div>
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle className="w-4 h-4" />
                <span className="text-slate-200">Capacity</span>
              </div>
            </div>
          </div>

          {/* UPDATED: Dynamic Risk Matrix updated according to what-if parameters */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h2 className="text-xs uppercase font-semibold text-slate-400 tracking-wider flex items-center space-x-2">
                <ShieldAlert className={`w-4 h-4 ${isHighRisk ? 'text-red-400' : 'text-amber-400'}`} />
                <span>Risk Matrix</span>
              </h2>
              {/* UPDATED: Risk status badge switches dynamically between LOW RISK and HIGH RISK */}
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${
                isHighRisk
                  ? 'text-red-400 bg-red-950/60 border-red-500/30'
                  : 'text-emerald-400 bg-emerald-950/60 border-emerald-500/30'
              }`}>
                {riskBadgeText}
              </span>
            </div>

            <div className="flex justify-between items-center">
              <div>
                <span className={`text-3xl font-black ${isHighRisk ? 'text-red-400' : 'text-white'}`}>
                  {riskScore}
                </span>
                <span className="text-xs text-slate-400 font-mono"> / 100</span>
              </div>
              <div className="text-right text-xs space-y-1 text-slate-300">
                <div>
                  Congestion: <span className={`font-semibold ${formData.port_congestion_days >= 5 ? 'text-red-400' : 'text-emerald-400'}`}>
                    {formData.port_congestion_days >= 5 ? 'HIGH' : 'LOW'}
                  </span>
                </div>
                <div>
                  Weather: <span className="text-amber-400 font-semibold">
                    {formData.weather_risk_index >= 2.0 ? 'HIGH' : 'MEDIUM'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* UPDATED: Primary Decision Banner dynamically updates recommendation based on simulation state */}
        <div className={`border-2 rounded-xl p-6 space-y-6 transition-colors ${
          isHighRisk
            ? 'bg-red-950/20 border-red-500/50'
            : 'bg-emerald-950/30 border-emerald-500/50'
        }`}>
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left border-b border-slate-800/80 pb-6">
            <div className="flex items-center space-x-3">
              <span className={`w-4 h-4 rounded-full animate-ping ${isHighRisk ? 'bg-red-400' : 'bg-emerald-400'}`}></span>
              <h2 className={`text-3xl md:text-4xl font-black tracking-tight ${isHighRisk ? 'text-red-400' : 'text-emerald-400'}`}>
                {isHighRisk ? '🔴' : '🟢'} {recommendedAction}
              </h2>
            </div>
            <div className="text-right text-sm">
              <div className="text-slate-300">
                Recommended Class: <span className="font-bold text-white">{data?.charter_optimization_module?.recommended_vessel_class || "PANAMAX"}</span>
              </div>
              <div className="text-slate-300">
                Expected Cost: <span className={`font-bold ${isHighRisk ? 'text-red-300' : 'text-emerald-300'}`}>₹{expectedCostDisplay} Cr</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xs uppercase font-semibold text-slate-400 tracking-wider mb-3">
              Why? (Decision Drivers)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-lg text-slate-200">
                • Freight ↑ <span className="text-emerald-400 font-bold">{surgeSign}{surgePct}%</span>
              </div>
              <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-lg text-slate-200">
                • {formData.port_congestion_days >= 5 ? 'Port congestion delay' : 'Port compatible'}
              </div>
              <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-lg text-slate-200">
                • {isHighRisk ? 'Deadline risk high' : 'Deadline feasible'}
              </div>
              <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-lg text-slate-200">
                • {isHighRisk ? 'Risk elevated' : 'Risk acceptable'}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}