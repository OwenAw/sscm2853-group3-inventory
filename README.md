# Inventory Management Optimization: Intravenous (IV) Fluids

## 📌 Overview
This repository contains the data analysis and inventory control modeling for the **Pharmacy Department at ABC Medical Centre**. Conducted as part of the SSCM 2853 Inventory Control & Queueing Theory coursework at Universiti Teknologi Malaysia (UTM), this project evaluates historical inventory usage to recommend an optimal, data-driven inventory management policy for Intravenous (IV) Fluids.

## 🎯 Objectives
* **Demand Pattern Analysis:** Determine whether the monthly demand for IV fluids follows a static (deterministic) or probabilistic pattern using statistical testing.
* **Inventory Modeling:** Evaluate multiple models (Classic EOQ, EOQ with Planned Shortages, and Probabilistic Inventory Models) to balance holding costs, setup costs, and shortage costs.
* **Policy Recommendation:** Establish a robust inventory policy that ensures uninterrupted healthcare delivery, minimizes stockouts, and controls costs.

## 📊 Data Analysis & Key Findings
Based on 12 months of historical usage data, the demand pattern analysis revealed the following:
* **Low Variability:** The Coefficient of Variation (CV) is $0.0453$, indicating highly stable demand suitable for baseline deterministic modeling.
* **Normal Distribution:** A Shapiro-Wilk test ($p-value = 1.000$) confirmed that the monthly demand follows a normal distribution, supporting the use of a probabilistic model for safety stock calculations.
* **Significant Upward Trend:** Linear regression analysis identified a statistically significant upward demand trend of **10.66 units per month** ($R^2 = 0.7236$, $p < 0.001$).

## ⚙️ Evaluated Inventory Models
The analysis assumed a unit price of RM 18.00, a setup cost of RM 0.54 per order (3%), a holding cost of RM 1.44 per unit/year (8%), a shortage cost of RM 2.70 per unit (15%), and a 1-month lead time.

1. **Classic EOQ (Deterministic):** Yielded an optimal order quantity of 95 units and a reorder point of 998 units.
2. **EOQ with Planned Shortages:** Calculated a theoretically lower total annual cost (RM 110.18) by allowing a maximum shortage of ~41 units. *Note: Rejected in the final recommendation due to the critical nature of IV fluids in patient care.*
3. **Probabilistic Inventory Model (95% Service Level):** Balanced cost with a strict healthcare service standard by incorporating safety stock to buffer against lead-time demand variability.

## 🏆 Recommended Policy
We recommend a **Continuous Review Probabilistic Policy** to prioritize patient safety and service reliability:
* **Order Quantity (Q):** 95 units
* **Reorder Point (R):** 1,072 units
* **Safety Stock:** 74 units
* **Target Service Level:** 95%

### Practical Managerial Insights
* Implement real-time continuous review monitoring.
* Enforce strict First-Expiry-First-Out (FEFO) protocols and automated expiry alerts (at 18 months for a 24-month shelf life).
* Maintain emergency reserves of 2-3 days' demand (66–100 units) and establish multi-supplier relationships to mitigate supply chain risks.

**Institution:** Universiti Teknologi Malaysia (UTM)  
**Academic Term:** 2025/2026 Semester 2
