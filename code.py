#!/usr/bin/env python3
"""
Inventory Analysis for Group 3: Intravenous (IV) Fluids
With corrected holding cost interpretation and expiry control analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from scipy import stats

# Paths
BASE_DIR = "/home/ding/OneDrive/SSCM2853-ICQT/Group Assignment"
RESULT_DIR = os.path.join(BASE_DIR, "Result")
FIGURE_DIR = os.path.join(BASE_DIR, "Inventory Control", "Figure")
os.makedirs(RESULT_DIR, exist_ok=True)

# Read data
df = pd.read_excel(os.path.join(BASE_DIR, "Hospital_Inventory_Varied_Demand_With_Prices.xlsx"))

# Group 3: Intravenous (IV) Fluids
group3 = df[df['Group'] == 3].iloc[0]
item_name = group3['Inventory Category']
unit_price = group3['Unit Purchasing Price (RM)']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
demand_data = [int(group3[m]) for m in months]

print(f"Item: {item_name}")
print(f"Unit Price: RM {unit_price}")
print(f"Monthly Demand: {demand_data}")

# ============================================================
# COST PARAMETERS (from assignment)
# ============================================================
# NOTE: In standard inventory theory, holding cost rates are typically ANNUAL
# The assignment states "8% of the average purchasing cost" without specifying period
# We interpret this as ANNUAL rate (standard practice in Taha's textbook)

avg_demand = np.mean(demand_data)
D_monthly = avg_demand
D_annual = D_monthly * 12

# Setup cost is per order (not time-dependent)
K = 0.03 * unit_price  # RM 0.54 per order

# HOLDING COST - TWO INTERPRETATIONS:
# Interpretation A: 8% is MONTHLY rate (as previously calculated)
h_monthly_interp = 0.08 * unit_price  # RM 1.44 per unit per month
h_annual_interpA = h_monthly_interp * 12  # RM 17.28 per unit per year (96% of value)

# Interpretation B: 8% is ANNUAL rate (standard textbook interpretation)
h_annual_interpB = 0.08 * unit_price  # RM 1.44 per unit per year
h_monthly_interpB = h_annual_interpB / 12  # RM 0.12 per unit per month

# Shortage cost is per unit (one-time penalty)
p = 0.15 * unit_price  # RM 2.70 per unit

print(f"\n=== COST PARAMETERS ===")
print(f"Setup Cost (K): RM {K:.2f} per order")
print(f"Unit Price: RM {unit_price:.2f}")
print(f"\nInterpretation A (Monthly Rate):")
print(f"  Holding Cost: RM {h_monthly_interp:.2f} per unit per month = RM {h_annual_interpA:.2f} per unit per year")
print(f"  Annual holding rate: {h_annual_interpA/unit_price*100:.0f}% of unit value")
print(f"\nInterpretation B (Annual Rate - STANDARD):")
print(f"  Holding Cost: RM {h_annual_interpB:.2f} per unit per year = RM {h_monthly_interpB:.2f} per unit per month")
print(f"  Annual holding rate: {h_annual_interpB/unit_price*100:.0f}% of unit value")
print(f"\nShortage Cost (p): RM {p:.2f} per unit")

# ============================================================
# JUSTIFICATION FOR HOLDING COST INTERPRETATION
# ============================================================
print("\n" + "="*60)
print("HOLDING COST INTERPRETATION JUSTIFICATION")
print("="*60)
print("""
Standard inventory theory (Taha, 2023) defines holding cost as an ANNUAL rate.
Typical holding costs range from 15-35% of item value per year for most industries.

For medical supplies:
- Storage costs: 5-10% annually
- Insurance: 1-3% annually  
- Obsolescence/expiry: 5-15% annually
- Capital cost: 5-10% annually
- Total: typically 15-35% annually

Interpretation A (monthly): 96% annual rate is EXCESSIVE
- Implies nearly the full value of inventory is lost per year to holding
- Not realistic for any industry

Interpretation B (annual): 8% annual rate is REASONABLE
- Lower bound for medical supplies
- Conservative estimate appropriate for analysis
- Aligns with standard textbook methodology

CONCLUSION: We adopt Interpretation B (8% as ANNUAL rate) as the standard approach.
""")

# Use annual interpretation for calculations
h_annual = h_annual_interpB
h_monthly = h_monthly_interpB

# ============================================================
# 1. DEMAND ANALYSIS (unchanged)
# ============================================================
print("\n" + "="*60)
print("1. DEMAND PATTERN ANALYSIS")
print("="*60)

mean_demand = np.mean(demand_data)
std_demand = np.std(demand_data, ddof=1)
cv = std_demand / mean_demand
min_demand = np.min(demand_data)
max_demand = np.max(demand_data)
range_demand = max_demand - min_demand

print(f"Mean Demand: {mean_demand:.2f} units/month")
print(f"Standard Deviation: {std_demand:.2f}")
print(f"Coefficient of Variation (CV): {cv:.4f}")
print(f"Min Demand: {min_demand}")
print(f"Max Demand: {max_demand}")
print(f"Range: {range_demand}")

# Normality test
shapiro_stat, shapiro_p = stats.shapiro(demand_data)
print(f"\nShapiro-Wilk Test:")
print(f"  Statistic: {shapiro_stat:.4f}")
print(f"  p-value: {shapiro_p:.4f}")

# Trend analysis
from scipy.stats import linregress
x = np.arange(1, 13)
slope, intercept, r_value, p_value, std_err = linregress(x, demand_data)
print(f"\nTrend Analysis:")
print(f"  Slope: {slope:.2f} units/month")
print(f"  R-squared: {r_value**2:.4f}")

# ============================================================
# 2. CLASSIC EOQ MODEL - CORRECTED
# ============================================================
print("\n" + "="*60)
print("2. CLASSIC EOQ MODEL (CORRECTED - Annual Holding Cost)")
print("="*60)

EOQ = np.sqrt(2 * K * D_annual / h_annual)
t0_years = EOQ / D_annual
t0_months = t0_years * 12
n_orders = D_annual / EOQ
TCU_EOQ = (K * D_annual / EOQ) + (h_annual * EOQ / 2)

print(f"Annual Demand (D): {D_annual:.0f} units/year")
print(f"EOQ (Q*): {EOQ:.2f} units")
print(f"Cycle Time: {t0_years:.4f} years = {t0_months:.2f} months")
print(f"Number of Orders/Year: {n_orders:.2f}")
print(f"Total Annual Cost (TCU): RM {TCU_EOQ:.2f}")

# ============================================================
# 3. EOQ WITH PLANNED SHORTAGES - CORRECTED
# ============================================================
print("\n" + "="*60)
print("3. EOQ WITH PLANNED SHORTAGES (CORRECTED)")
print("="*60)

EOQ_short = np.sqrt(2 * K * D_annual / h_annual) * np.sqrt((h_annual + p) / p)
S_star = (h_annual / (h_annual + p)) * EOQ_short
MIL = EOQ_short - S_star
TCU_short = (K * D_annual / EOQ_short) + (h_annual * MIL**2 / (2 * EOQ_short)) + (p * S_star**2 / (2 * EOQ_short))

print(f"EOQ with Shortages (Q*): {EOQ_short:.2f} units")
print(f"Maximum Shortage (S*): {S_star:.2f} units")
print(f"Maximum Inventory Level (MIL): {MIL:.2f} units")
print(f"Total Annual Cost (TCU): RM {TCU_short:.2f}")
print(f"Cost Savings vs Classic EOQ: RM {TCU_EOQ - TCU_short:.2f} ({(TCU_EOQ - TCU_short)/TCU_EOQ*100:.1f}%)")

# ============================================================
# 4. PROBABILISTIC MODEL - CORRECTED
# ============================================================
print("\n" + "="*60)
print("4. PROBABILISTIC INVENTORY MODEL (CORRECTED)")
print("="*60)

lead_time = 1  # month
D_lead = mean_demand * lead_time
std_lead = std_demand * np.sqrt(lead_time)

print(f"Lead Time: {lead_time} month")
print(f"Expected Demand During Lead Time: {D_lead:.2f}")
print(f"Std Dev During Lead Time: {std_lead:.2f}")

# Safety stock analysis
service_levels = [0.90, 0.95, 0.99]
z_values = {0.90: 1.282, 0.95: 1.645, 0.99: 2.326}

print(f"\nSafety Stock Analysis:")
for sl in service_levels:
    z = z_values[sl]
    safety_stock = z * std_lead
    ROP = D_lead + safety_stock
    print(f"  {sl*100:.0f}% Service Level (z={z}):")
    print(f"    Safety Stock: {safety_stock:.2f} units")
    print(f"    Reorder Point (R): {ROP:.2f} units")

# Iterative probabilistic model
print(f"\nIterative Probabilistic Model Solution:")
K_order = K
h_m = h_monthly  # Use monthly holding cost for monthly model
p_shortage = p

# Step 0
y1 = np.sqrt(2 * K_order * D_monthly / h_m)
print(f"  Initial y1 = {y1:.2f}")

R0 = 0
for i in range(1, 15):
    z_R = (R0 - D_lead) / std_lead
    S = std_lead * stats.norm.pdf(z_R) + (D_lead - R0) * (1 - stats.norm.cdf(z_R))
    
    y = np.sqrt(2 * D_monthly * (K_order + p_shortage * S) / h_m)
    
    target_prob = h_m * y / (p_shortage * D_monthly)
    if target_prob >= 1:
        R = D_lead
    else:
        R = D_lead + std_lead * stats.norm.ppf(1 - target_prob)
    
    print(f"  Iteration {i}: S={S:.4f}, y={y:.2f}, R={R:.2f}")
    
    if abs(R - R0) < 0.01:
        break
    R0 = R

print(f"\nOptimal Policy:")
print(f"  Order Quantity (y*): {y:.2f} units")
print(f"  Reorder Point (R*): {R:.2f} units")
print(f"  Safety Stock: {R - D_lead:.2f} units")

# ============================================================
# 5. EXPIRY CONTROL ANALYSIS
# ============================================================
print("\n" + "="*60)
print("5. EXPIRY CONTROL ANALYSIS")
print("="*60)

# IV Fluids typically have shelf life of 2-3 years
shelf_life_months = 24  # Assume 2 years for IV fluids
max_inventory = EOQ  # Maximum inventory level
turnover_rate = D_annual / EOQ

print(f"Assumed Shelf Life: {shelf_life_months} months")
print(f"Maximum Inventory (EOQ): {max_inventory:.0f} units")
print(f"Inventory Turnover Rate: {turnover_rate:.1f} times/year")
print(f"Average Inventory: {EOQ/2:.0f} units")
print(f"Days of Supply in Inventory: {EOQ/D_monthly*30:.0f} days")

# FIFO compliance
print(f"\nFIFO Analysis:")
print(f"  With EOQ of {EOQ:.0f} units and monthly demand of {D_monthly:.0f}:")
print(f"  Inventory is depleted in {EOQ/D_monthly:.1f} months")
print(f"  Well within {shelf_life_months}-month shelf life")

# ============================================================
# 6. COMPARISON TABLE
# ============================================================
print("\n" + "="*60)
print("6. MODEL COMPARISON (CORRECTED)")
print("="*60)

comparison = f"""
{'='*70}
CORRECTED ANALYSIS RESULTS - Group 3: {item_name}
{'='*70}

HOLDING COST INTERPRETATION
----------------------------
The assignment states "Holding Cost: 8% of the average purchasing cost"
Standard inventory theory (Taha, 2023) defines holding cost as ANNUAL rate.
A monthly rate of 8% would equal 96% annually - excessive for any industry.
Therefore, we adopt 8% as the ANNUAL holding cost rate.

Holding Cost (Annual): RM {h_annual:.2f} per unit per year
Holding Cost (Monthly): RM {h_monthly:.2f} per unit per month

CLASSIC EOQ MODEL
------------------
EOQ (Q*): {EOQ:.2f} units
Cycle Time: {t0_months:.2f} months
Orders per Year: {n_orders:.2f}
Total Annual Cost: RM {TCU_EOQ:.2f}

EOQ WITH PLANNED SHORTAGES
---------------------------
EOQ (Q*): {EOQ_short:.2f} units
Maximum Shortage (S*): {S_star:.2f} units
Maximum Inventory Level (MIL): {MIL:.2f} units
Total Annual Cost: RM {TCU_short:.2f}

PROBABILISTIC MODEL
--------------------
Reorder Point (R*): {R:.2f} units
Order Quantity (y*): {y:.2f} units
Safety Stock (95% SL): {R - D_lead:.2f} units

EXPIRY CONTROL
---------------
Shelf Life Assumption: {shelf_life_months} months
Inventory Turnover: {turnover_rate:.1f} times/year
FIFO Compliance: Inventory depleted in {EOQ/D_monthly:.1f} months (within shelf life)
"""

with open(os.path.join(RESULT_DIR, "analysis_results.txt"), "w") as f:
    f.write(comparison)

# ============================================================
# 7. GENERATE UPDATED PLOTS
# ============================================================
print("\n" + "="*60)
print("7. GENERATING UPDATED PLOTS")
print("="*60)

# Plot 1: EOQ Cost Curves (Corrected)
fig, ax = plt.subplots(figsize=(10, 6))
q_range = np.linspace(EOQ * 0.3, EOQ * 2.5, 100)
holding_cost = h_annual * q_range / 2
ordering_cost = K * D_annual / q_range
total_cost = holding_cost + ordering_cost

ax.plot(q_range, holding_cost, 'g--', linewidth=2, label='Holding Cost (Annual)')
ax.plot(q_range, ordering_cost, 'r:', linewidth=2, label='Ordering Cost')
ax.plot(q_range, total_cost, 'b-', linewidth=2.5, label='Total Cost')
ax.axvline(x=EOQ, color='purple', linestyle='-.', linewidth=1.5, label=f'EOQ = {EOQ:.0f}')
ax.set_xlabel('Order Quantity (Q)', fontsize=12)
ax.set_ylabel('Annual Cost (RM)', fontsize=12)
ax.set_title('EOQ Cost Analysis (Annual Holding Cost)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, 'eoq_cost_curves.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: eoq_cost_curves.png (updated)")

# Plot 2: Inventory Sawtooth (Corrected)
fig, ax = plt.subplots(figsize=(12, 5))
cycles = 6
cycle_time_months = t0_months
for i in range(cycles):
    start = i * cycle_time_months
    ax.plot([start, start + cycle_time_months], [EOQ, 0], 'b-', linewidth=2)
    ax.plot([start], [EOQ], 'ro', markersize=8)

ax.axhline(y=D_monthly, color='green', linestyle='--', alpha=0.5, label=f'Monthly Demand = {D_monthly:.0f}')
ax.set_xlabel('Time (months)', fontsize=12)
ax.set_ylabel('Inventory Level', fontsize=12)
ax.set_title('Inventory Level Over Time (EOQ Model)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.set_xlim(0, cycles * cycle_time_months)
ax.set_ylim(0, EOQ * 1.2)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, 'inventory_sawtooth.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: inventory_sawtooth.png (updated)")

# Save numerical results
results_df = pd.DataFrame({
    'Parameter': ['Unit Price', 'Mean Monthly Demand', 'Std Dev', 'CV',
                  'K (Setup)', 'h (Annual)', 'h (Monthly)', 'p (Shortage)',
                  'EOQ', 'Cycle Time (months)', 'Orders/Year', 'TCU',
                  'EOQ (Shortages)', 'S*', 'MIL', 'TCU Shortages',
                  'y* (Probabilistic)', 'R*', 'Safety Stock'],
    'Value': [unit_price, mean_demand, std_demand, cv,
              K, h_annual, h_monthly, p,
              EOQ, t0_months, n_orders, TCU_EOQ,
              EOQ_short, S_star, MIL, TCU_short,
              y, R, R - D_lead]
})
results_df.to_csv(os.path.join(RESULT_DIR, "numerical_results.csv"), index=False)

print("\nAnalysis Complete!")
