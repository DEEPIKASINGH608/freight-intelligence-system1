"use client";

import { useState, useEffect } from "react";

export default function FreightDashboard() {
  // Input State Variables
  const [cargoTons, setCargoTons] = useState<number>(150000);
  const [currentRate, setCurrentRate] = useState<number>(22.50);
  const [fuelPrice, setFuelPrice] = useState<number>(620);
  const [congestionDays, setCongestionDays] = useState<number>(3.0);
  const [demandIndex, setDemandIndex] = useState<number>(105);

  // Response Data State
  const [loading, setLoading] = useState<boolean>(false);
  const [decision, setDecision] = useState<any>(null);

  // Trigger Decision API Call
  const evaluateStrategy = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/decision/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cargo_quantity_tons: cargoTons,
          current_freight_rate: currentRate,
          bunker_fuel_price: fuelPrice,
          port_congestion_days: congestionDays,
          cargo_demand_index: demandIndex,
        }),
      });
      const data = await response.json();
      setDecision(data);
    } catch (err) {
      console.error("API Connection error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    evaluateStrategy();
  }, []);

  return (
    <main className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      {/* HEADER BAR */}
      <header className="mb-8 border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">
            Maritime Freight Intelligence System
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Predictive Rate Forecasting & Mixed-Integer Charter Optimization Engine
          </p>
        </div>
        <div className="bg-slate-800 px-4 py-2 rounded-lg border border-slate-700 text-right">
          <span className="text-xs text-slate-400 block">SYSTEM STATUS</span>
          <span className="text-xs font-semibold text-emerald-400">● ML ENGINES ONLINE</span>
        </div>
      </header>

      {/* DASHBOARD GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* LEFT PANEL: SIMULATION CONTROLS */}
        <section className="bg-slate-800/60 p-6 rounded-xl border border-slate-700 space-y-6">
          <h2 className="text-xl font-semibold text-white border-b border-slate-700 pb-2">
            Market & Route Parameters
          </h2>

          <div>
            <label className="text-sm font-medium text-slate-300 block mb-1">
              Cargo Volume Required: <span className="text-cyan-400 font-bold">{cargoTons.toLocaleString()} Tons</span>
            </label>
            <input
              type="range" min="50000" max="300000" step="10000"
              value={cargoTons} onChange={(e) => setCargoTons(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-300 block mb-1">
              Current Freight Rate: <span className="text-cyan-400 font-bold">${currentRate}/Ton</span>
            </label>
            <input
              type="range" min="10" max="50" step="0.5"
              value={currentRate} onChange={(e) => setCurrentRate(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-300 block mb-1">
              Bunker Fuel Price: <span className="text-cyan-400 font-bold">${fuelPrice}/Ton</span>
            </label>
            <input
              type="range" min="400" max="900" step="10"
              value={fuelPrice} onChange={(e) => setFuelPrice(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-300 block mb-1">
              Port Congestion Delay: <span className="text-cyan-400 font-bold">{congestionDays} Days</span>
            </label>
            <input
              type="range" min="0" max="10" step="0.5"
              value={congestionDays} onChange={(e) => setCongestionDays(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>

          <button
            onClick={evaluateStrategy}
            disabled={loading}
            className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-3 rounded-lg transition-all shadow-lg shadow-cyan-950"
          >
            {loading ? "Re-Evaluating Optimization..." : "Run Optimization & Forecast"}
          </button>
        </section>

        {/* RIGHT PANEL: DECISION SYNTHESIS & KPIS */}
        <section className="lg:col-span-2 space-y-6">
          {decision && (
            <>
              {/* ACTION BANNER */}
              <div className={`p-6 rounded-xl border ${
                decision.recommended_action.includes("CHARTER")
                  ? "bg-emerald-950/40 border-emerald-500/50 text-emerald-200"
                  : "bg-amber-950/40 border-amber-500/50 text-amber-200"
              }`}>
                <span className="text-xs uppercase font-bold tracking-wider opacity-80">RECOMMENDED STRATEGIC ACTION</span>
                <h3 className="text-3xl font-extrabold mt-1">{decision.recommended_action}</h3>
                <p className="mt-2 text-sm leading-relaxed opacity-90">{decision.reasoning}</p>
              </div>

              {/* FINANCIAL KPI CARDS */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                  <span className="text-xs text-slate-400 block">ESTIMATED LOGISTICS COST</span>
                  <span className="text-2xl font-bold text-white mt-1 block">
                    ₹{decision.financial_summary.total_estimated_cost_inr_cr} Cr
                  </span>
                  <span className="text-xs text-slate-500 mt-1 block">Base Charter + Fuel</span>
                </div>

                <div className="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                  <span className="text-xs text-slate-400 block">PROJECTED SAVINGS</span>
                  <span className="text-2xl font-bold text-emerald-400 mt-1 block">
                    ₹{decision.financial_summary.estimated_savings_inr_cr} Cr
                  </span>
                  <span className="text-xs text-emerald-500/80 mt-1 block">VS Delaying Action</span>
                </div>

                <div className="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                  <span className="text-xs text-slate-400 block">30-DAY RATE FORECAST</span>
                  <span className="text-2xl font-bold text-cyan-400 mt-1 block">
                    ${decision.financial_summary.forecast_rate_usd_ton}/ton
                  </span>
                  <span className="text-xs text-slate-400 mt-1 block">
                    Delta: {decision.financial_summary.rate_change_pct}%
                  </span>
                </div>
              </div>

              {/* MODULE DETAILS GRID */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* RISK EVALUATION */}
                <div className="bg-slate-800/40 p-5 rounded-xl border border-slate-700">
                  <h4 className="font-semibold text-white mb-3">Operational Risk Score</h4>
                  <div className="flex items-center space-x-4 mb-3">
                    <span className="text-3xl font-extrabold text-amber-400">
                      {decision.risk_module.risk_score}/100
                    </span>
                    <span className="px-2.5 py-1 text-xs rounded font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                      {decision.risk_module.risk_level} RISK
                    </span>
                  </div>
                  <ul className="text-xs text-slate-300 space-y-1">
                    {decision.risk_module.key_drivers.map((driver: string, idx: number) => (
                      <li key={idx}>• {driver}</li>
                    ))}
                  </ul>
                </div>

                {/* CHARTER OPTIMIZATION */}
                <div className="bg-slate-800/40 p-5 rounded-xl border border-slate-700">
                  <h4 className="font-semibold text-white mb-3">MILP Vessel Selection</h4>
                  <p className="text-xs text-slate-300 mb-2">
                    Selected Capacity: <span className="font-bold text-white">{decision.charter_optimization_module.total_selected_capacity_tons?.toLocaleString()} Tons</span>
                  </p>
                  <div className="space-y-2">
                    {decision.charter_optimization_module.selected_vessels?.map((v: any, idx: number) => (
                      <div key={idx} className="bg-slate-900/60 p-2.5 rounded border border-slate-800 text-xs flex justify-between">
                        <div>
                          <span className="font-bold text-slate-200">{v.name}</span>
                          <span className="text-slate-400 block">{v.capacity_dwt.toLocaleString()} DWT | {v.vessel_type}</span>
                        </div>
                        <span className="font-semibold text-cyan-400">${v.daily_charter_rate}/day</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          )}
        </section>
      </div>
    </main>
  );
}