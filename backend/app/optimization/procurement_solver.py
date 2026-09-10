import numpy as np
from scipy.optimize import linprog

def optimize_procurement(target_demand_tons, suppliers):
    """
    Optimizes cargo allocation across multiple suppliers using Linear Programming.
    """
    num_suppliers = len(suppliers)
    if num_suppliers == 0:
        return None

    # 1. Objective Function Coefficients (c): Cost_i = Commodity_Price_i + Freight_Rate_i
    c = [s["commodity_price_usd"] + s["freight_rate_usd"] for s in suppliers]

    # 2. Equality Constraints (A_eq * x = b_eq): Total Allocated Tons == Target Demand
    A_eq = [[1.0] * num_suppliers]
    b_eq = [target_demand_tons]

    # 3. Inequality Constraints (A_ub * x <= b_ub)
    A_ub = []
    b_ub = []

    # Supplier Maximum Allocation Share (Risk Diversification Cap)
    for i, s in enumerate(suppliers):
        if "max_allocation_pct" in s and s["max_allocation_pct"] < 1.0:
            row = [0.0] * num_suppliers
            row[i] = 1.0
            A_ub.append(row)
            b_ub.append(target_demand_tons * s["max_allocation_pct"])

    # 4. Variable Bounds (0 <= x_i <= Capacity_i)
    bounds = []
    for s in suppliers:
        min_qty = s.get("min_order_tons", 0)
        max_qty = s.get("capacity_tons", target_demand_tons)
        bounds.append((min_qty, max_qty))

    # 5. Solve LP using SciPy Highs Solver
    res = linprog(
        c,
        A_ub=A_ub if A_ub else None,
        b_ub=b_ub if b_ub else None,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs"
    )

    if not res.success:
        return {"status": "error", "message": f"Optimization failed: {res.message}"}

    # 6. Format Optimization Results
    allocations = []
    total_cost = 0.0

    for i, s in enumerate(suppliers):
        allocated_tons = round(res.x[i], 2)
        if allocated_tons > 0:
            landed_cost = c[i]
            supplier_total_cost = allocated_tons * landed_cost
            total_cost += supplier_total_cost

            allocations.append({
                "supplier_id": s.get("id", f"sup_{i+1}"),
                "supplier_name": s["name"],
                "origin": s.get("origin", "N/A"),
                "allocated_tons": allocated_tons,
                "share_of_total_pct": round((allocated_tons / target_demand_tons) * 100, 1),
                "commodity_price_usd": s["commodity_price_usd"],
                "freight_rate_usd": s["freight_rate_usd"],
                "landed_cost_per_ton_usd": round(landed_cost, 2),
                "total_cost_usd": round(supplier_total_cost, 2)
            })

    weighted_avg_landed_cost = total_cost / target_demand_tons if target_demand_tons > 0 else 0.0

    return {
        "status": "success",
        "target_demand_tons": target_demand_tons,
        "total_procurement_cost_usd": round(total_cost, 2),
        "weighted_avg_landed_cost_per_ton_usd": round(weighted_avg_landed_cost, 2),
        "allocations": allocations
    }