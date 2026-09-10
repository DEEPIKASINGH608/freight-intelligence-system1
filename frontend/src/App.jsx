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

  // Form state supporting both keyboard input boxes and range sliders
  const [formData, setFormData] = useState({
    cargo_quantity_tons: 75000,
    current_freight_rate: 22.40,
    bunker_fuel_price: 620.00,
    port_congestion_days: 2.5,
    cargo_demand_index: 105,
    vessel_availability_index: 92,
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

  // Updated handler to manage both slider input and direct keyboard typing
  const handleChange = (e) => {
    const val = e.target.value;
    const numericVal = val === '' ? '' : parseFloat(val);

    setFormData((prev) => ({
      ...prev,
      [e.target.name]: numericVal
    }));
  };

  // Dynamic Calculation Helpers
  const currentRate = parseFloat(formData.current_freight_rate) || 22.4;
  const forecastRate = data?.financial_summary?.forecasted_30d_rate_usd
    ? parseFloat(data.financial_summary.forecasted_30d_rate_usd)
    : 22.56;

  // Surge percentage calculation
  const surgePct = (((forecastRate - currentRate) / currentRate) * 100).toFixed(1);
  const surgeSign = surgePct >= 0 ? '+' : '';

  // Expected Total Cost in INR Crore calculation
  const usdToInrRate = 83;
  const totalCostInrCr = (((parseFloat(formData.cargo_quantity_tons) || 0) * forecastRate * usdToInrRate) / 10000000).toFixed(1);

  const expectedCostDisplay = data?.financial_summary?.total_expected_cost_inr_cr
    || data?.scenario_analysis?.total_expected_cost_inr_cr
    || totalCostInrCr;

  // Dynamic decision logic driven by slider/input states
  const isHighRisk = (parseFloat(formData.port_congestion_days) || 0) >= 5 || (parseFloat(formData.weather_risk_index) || 0) >= 2.5;
  const recommendedAction = isHighRisk ? "WAIT / REROUTE" : (data?.recommended_action || "CHARTER NOW");
  const riskBadgeText = isHighRisk ? "HIGH RISK" : "LOW RISK";
  const riskScore = isHighRisk
    ? Math.min(85, Math.round((parseFloat(formData.port_congestion_days) || 0) * 12 + (parseFloat(formData.weather_risk_index) || 0) * 15))
    : 34;

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

        {/* What-If Scenario Simulator with Sliders & Numeric Inputs */}
        <details className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden" open>
          <summary className="p-4 text-xs font-semibold uppercase tracking-wider text-slate-400 cursor-pointer flex justify-between items-center hover:text-slate-200">
            <span className="flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-blue-400" />
              <span className="text-blue-400 font-bold">⚡ What-If Scenario Simulator</span>
            </span>
            <span className="text-blue-400 font-mono text-xs">Toggle Parameters</span>
          </summary>

          <div className="p-4 border-t border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-6 text-xs bg-slate-950/40">

            {/* Control 1: Freight Rate */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-400">
                <label className="font-medium">Freight Rate ($/t)</label>
                <div className="flex items-center space-x-1">
                  <span className="text-slate-500">$</span>
                  <input
                    type="number"
                    name="current_freight_rate"
                    step="0.1"
                    value={formData.current_freight_rate}
                    onChange={handleChange}
                    className="w-20 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-right text-blue-400 font-mono font-bold focus:outline-none focus:border-blue-500"
                  />
                  <span className="text-slate-500">/t</span>
                </div>
              </div>
              <input
                type="range" name="current_freight_rate" min="10" max="50" step="0.5"
                value={formData.current_freight_rate || 0} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Control 2: Bunker Fuel Price */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-400">
                <label className="font-medium">Bunker Fuel Price ($/t)</label>
                <div className="flex items-center space-x-1">
                  <span className="text-slate-500">$</span>
                  <input
                    type="number"
                    name="bunker_fuel_price"
                    step="5"
                    value={formData.bunker_fuel_price}
                    onChange={handleChange}
                    className="w-20 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-right text-blue-400 font-mono font-bold focus:outline-none focus:border-blue-500"
                  />
                  <span className="text-slate-500">/t</span>
                </div>
              </div>
              <input
                type="range" name="bunker_fuel_price" min="400" max="1000" step="10"
                value={formData.bunker_fuel_price || 0} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Control 3: Port Congestion (Days) */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-400">
                <label className="font-medium">Port Congestion (Days)</label>
                <div className="flex items-center space-x-1">
                  <input
                    type="number"
                    name="port_congestion_days"
                    step="0.5"
                    value={formData.port_congestion_days}
                    onChange={handleChange}
                    className={`w-16 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-right font-mono font-bold focus:outline-none focus:border-blue-500 ${
                      formData.port_congestion_days >= 5 ? 'text-red-400' : 'text-blue-400'
                    }`}
                  />
                  <span className="text-slate-500">Days</span>
                </div>
              </div>
              <input
                type="range" name="port_congestion_days" min="0" max="10" step="0.5"
                value={formData.port_congestion_days || 0} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Control 4: Cargo Demand Index */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-400">
                <label className="font-medium">Cargo Demand Index</label>
                <input
                  type="number"
                  name="cargo_demand_index"
                  step="1"
                  value={formData.cargo_demand_index}
                  onChange={handleChange}
                  className="w-16 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-right text-blue-400 font-mono font-bold focus:outline-none focus:border-blue-500"
                />
              </div>
              <input
                type="range" name="cargo_demand_index" min="50" max="150" step="1"
                value={formData.cargo_demand_index || 0} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Control 5: Vessel Availability Index */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-400">
                <label className="font-medium">Vessel Availability Index</label>
                <input
                  type="number"
                  name="vessel_availability_index"
                  step="1"
                  value={formData.vessel_availability_index}
                  onChange={handleChange}
                  className="w-16 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-right text-blue-400 font-mono font-bold focus:outline-none focus:border-blue-500"
                />
              </div>
              <input
                type="range" name="vessel_availability_index" min="50" max="150" step="1"
                value={formData.vessel_availability_index || 0} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            {/* Control 6: Weather Risk Index */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-400">
                <label className="font-medium">Weather Risk Index</label>
                <input
                  type="number"
                  name="weather_risk_index"
                  step="0.1"
                  value={formData.weather_risk_index}
                  onChange={handleChange}
                  className="w-16 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-right text-blue-400 font-mono font-bold focus:outline-none focus:border-blue-500"
                />
              </div>
              <input
                type="range" name="weather_risk_index" min="0.5" max="3.0" step="0.1"
                value={formData.weather_risk_index || 0} onChange={handleChange}
                className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
            </div>

            <div className="col-span-1 md:col-span-3 flex justify-between items-center pt-2">
              <span className="text-[11px] text-slate-400 italic">
                * You can drag the sliders or type exact numerical values directly into the input boxes.
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
              {(parseFloat(formData.cargo_quantity_tons) || 0).toLocaleString()} t
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

          {/* Dynamic Risk Matrix */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h2 className="text-xs uppercase font-semibold text-slate-400 tracking-wider flex items-center space-x-2">
                <ShieldAlert className={`w-4 h-4 ${isHighRisk ? 'text-red-400' : 'text-amber-400'}`} />
                <span>Risk Matrix</span>
              </h2>
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

        {/* Primary Decision Banner */}
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