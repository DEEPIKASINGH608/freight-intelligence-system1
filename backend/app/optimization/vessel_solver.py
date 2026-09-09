from ortools.linear_solver import pywraplp

class VesselOptimizationSolver:
    def __init__(self):
        pass

    def solve_vessel_chartering(
        self,
        cargo_required_tons: float,
        available_vessels: list,
        route_distance_nm: float,
        fuel_price_usd_ton: float,
        delivery_deadline_days: float,
        port_congestion_days: float = 2.0
    ) -> dict:
        """
        Solves Mixed-Integer Linear Programming (MILP) for optimal vessel selection using Google OR-Tools.
        """
        # Create SCIP integer programming solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            raise Exception("Google OR-Tools SCIP solver unavailable.")

        num_vessels = len(available_vessels)
        x = {} # Binary decision variables x[i]

        vessel_costs = []
        vessel_transit_times = []

        for i, v in enumerate(available_vessels):
            # 1. Create binary decision variable
            x[i] = solver.BoolVar(f'charter_vessel_{i}')

            # 2. Calculate transit & total operational days
            speed_knots = v.get('speed_knots', 14.0)
            transit_hours = route_distance_nm / speed_knots
            transit_days = transit_hours / 24.0

            # Total turnaround = 2 * transit (roundtrip) + port loading/unloading + congestion
            total_days = (transit_days * 2.0) + 3.0 + port_congestion_days
            vessel_transit_times.append(total_days)

            # 3. Calculate Total Voyage Cost ($)
            charter_cost = total_days * v['daily_charter_rate']
            fuel_cost = (transit_days * 2.0) * v['fuel_consumption_ton_day'] * fuel_price_usd_ton
            total_vessel_cost = charter_cost + fuel_cost
            vessel_costs.append(total_vessel_cost)

            # 4. Enforce Deadline Constraint: If vessel exceeds deadline, force x[i] = 0
            if total_days > delivery_deadline_days:
                solver.Add(x[i] == 0)

        # Constraint 1: Cargo Demand Satisfaction
        solver.Add(solver.Sum([x[i] * available_vessels[i]['capacity_dwt'] for i in range(num_vessels)]) >= cargo_required_tons)

        # Objective Function: Minimize Total Logistics Cost
        objective = solver.Objective()
        for i in range(num_vessels):
            objective.SetCoefficient(x[i], vessel_costs[i])
        objective.SetMinimization()

        # Solve MILP Model
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            selected_vessels = []
            total_capacity = 0.0
            total_cost_usd = 0.0
            max_delivery_days = 0.0

            for i in range(num_vessels):
                if x[i].solution_value() > 0.5:
                    v = available_vessels[i]
                    selected_vessels.append({
                        "id": v.get("id"),
                        "name": v["name"],
                        "vessel_type": v.get("vessel_type", "Capesize"),
                        "capacity_dwt": v["capacity_dwt"],
                        "daily_charter_rate": v["daily_charter_rate"],
                        "voyage_cost_usd": round(vessel_costs[i], 2),
                        "estimated_days": round(vessel_transit_times[i], 1)
                    })
                    total_capacity += v["capacity_dwt"]
                    total_cost_usd += vessel_costs[i]
                    max_delivery_days = max(max_delivery_days, vessel_transit_times[i])

            # Convert USD cost to INR Crores for business representation ($1 = ₹83, 1 Cr = 10,000,000)
            total_cost_inr_cr = round((total_cost_usd * 83.0) / 10000000.0, 2)
            capacity_utilization_pct = round(min(100.0, (cargo_required_tons / total_capacity) * 100), 1) if total_capacity > 0 else 0

            return {
                "status": "OPTIMAL",
                "selected_vessels": selected_vessels,
                "total_selected_capacity_tons": total_capacity,
                "cargo_required_tons": cargo_required_tons,
                "capacity_utilization_pct": capacity_utilization_pct,
                "total_cost_usd": round(total_cost_usd, 2),
                "total_cost_inr_cr": total_cost_inr_cr,
                "max_delivery_days": round(max_delivery_days, 1),
                "shortfall_tons": max(0.0, cargo_required_tons - total_capacity)
            }
        else:
            return {
                "status": "INFEASIBLE",
                "message": "Insufficient vessel capacity or deadline constraints too strict.",
                "selected_vessels": [],
                "total_cost_inr_cr": 0.0,
                "shortfall_tons": cargo_required_tons
            }