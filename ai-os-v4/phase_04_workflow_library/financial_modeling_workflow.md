# Financial Modeling Workflow Specification

## 1. Purpose & Objective
Construct 3-statement financial models, discounted cash flow (DCF) valuations, sensitivity analyses, and budget variance forecasts.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Historical financial statements (Income Statement, Balance Sheet, Cash Flow), chart of accounts, growth assumptions.
- **Trigger Conditions**: Quarterly financial planning or investment valuation trigger.

## 3. Participating Agent Roles & Responsibilities
- **Financial Analyst**: Builds financial model tabs, formula links, DCF calculations, and sensitivity tables.
- **Chief Financial Officer Agent**: Validates capital structure, discount rate assumptions, and strategic growth drivers.
- **Risk Auditor**: Audits formula integrity, scenario edge cases, and compliance with GAAP/IFRS principles.

## 4. Step-by-Step Execution Sequence

### Step 1: Historical Financial Ingestion & Cleanup
- **Inputs**: 3-year historical financial statements, trial balance data.
- **Actions**: Normalize account groupings, verify historical Balance Sheet balancing (Assets = Liabilities + Equity).
- **Outputs**: Historical Financial Baseline Matrix.
- **Verification**: Balance Sheet equation holds 100% across all historical periods.

### Step 2: Revenue & Operational Expense Modeling
- **Inputs**: Sales pipeline forecasts, headcount growth plans, OPEX assumptions.
- **Actions**: Build driver-based revenue projections (volume x price) and OPEX formulas linked to headcount assumptions.
- **Outputs**: Revenue & OPEX Projection Module.
- **Verification**: Financial Analyst verification of driver logic.

### Step 3: 3-Statement Integration & Cash Flow Modeling
- **Inputs**: Revenue/OPEX modules, working capital assumptions, CAPEX schedules.
- **Actions**: Integrate Income Statement, Balance Sheet, and Statement of Cash Flows with dynamic debt/cash sweeps.
- **Outputs**: Integrated 3-Statement Financial Model.
- **Verification**: Balance sheet balances dynamically across all 5 forecast years.

### Step 4: Valuation & Sensitivity Scenario Analysis
- **Inputs**: 3-statement model, Weighted Average Cost of Capital (WACC), terminal growth rates.
- **Actions**: Perform Discounted Cash Flow (DCF) valuation, build sensitivity matrices across WACC vs growth rates.
- **Outputs**: DCF Valuation & Sensitivity Matrix Report.
- **Verification**: Risk Auditor verification of cell formula integrity.

### Step 5: Executive Summary & Board Reporting
- **Inputs**: Completed model, valuation summary, sensitivity tables.
- **Actions**: Draft executive summary dashboard, visualize revenue bridges, compile board presentation pack.
- **Outputs**: Executive Financial Model Binder & Deck.
- **Verification**: CFO Agent sign-off on valuation targets.

## 5. Decision Gates & Branching Rules
- Gate 1: Balance Sheet must balance perfectly across all 5 forecast years before valuation calculation.
- Gate 2: WACC calculation requires formal CFO sign-off.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Circular reference in debt interest calculation -> Action: Implement iterative calculation flag or lag interest expense by 1 period.
- Failure Mode 2: Unrealistic terminal growth rate assumption -> Action: Cap terminal growth at long-term GDP growth rate (2-3%).

## 7. Artifact Delivery & Output Standard
Integrated 3-Statement Model Spreadsheet, DCF Valuation Report, Sensitivity Matrix, and Executive Board Deck.
