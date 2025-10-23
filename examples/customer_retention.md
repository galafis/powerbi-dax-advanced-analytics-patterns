# Customer Retention Analysis - Real-World Example

## Business Context

An e-commerce company wants to understand customer behavior over time, measure retention rates, and identify opportunities to improve customer lifetime value.

## Objective

- Track customer cohorts from their first purchase
- Measure retention rates month-over-month
- Calculate customer lifetime value (CLV)
- Identify at-risk customers
- Optimize marketing spend

## Dataset Structure

### Tables
- **Sales**: Order-level transactions
- **Customers**: Customer master data
- **Calendar**: Date dimension
- **Marketing**: Marketing campaigns and costs

### Key Columns
```
Sales[Order ID]
Sales[Order Date]
Sales[Customer ID]
Sales[Sales Amount]
Sales[Profit]

Customers[Customer ID]
Customers[Registration Date]
Customers[Segment]
Customers[Email]
```

## Cohort Analysis Framework

### Step 1: Define Cohorts

```dax
// First Purchase Date (defines cohort)
First Purchase Date = 
CALCULATE(
    MIN('Sales'[Order Date]),
    ALL('Sales'),
    VALUES('Sales'[Customer ID])
)

// Cohort Month
Cohort Month = 
FORMAT([First Purchase Date], "YYYY-MM")

// Cohort Size
Cohort Size = 
CALCULATE(
    DISTINCTCOUNT('Sales'[Customer ID]),
    FILTER(
        ALL('Sales'[Order Date]),
        FORMAT('Sales'[Order Date], "YYYY-MM") = [Cohort Month]
    )
)
```

### Step 2: Calculate Retention

```dax
// Cohort Age (Months Since First Purchase)
Cohort Age Months = 
DATEDIFF(
    [First Purchase Date],
    MAX('Sales'[Order Date]),
    MONTH
)

// Retention Rate
Retention Rate % = 
VAR CohortCustomers = [Cohort Size]
VAR ActiveCustomers = 
    CALCULATE(
        DISTINCTCOUNT('Sales'[Customer ID]),
        USERELATIONSHIP('Sales'[Order Date], 'Calendar'[Date])
    )
RETURN
    DIVIDE(ActiveCustomers, CohortCustomers, 0)

// Churn Rate
Churn Rate % = 1 - [Retention Rate %]
```

### Step 3: Revenue Analysis

```dax
// Cohort Lifetime Value
Cohort LTV = 
VAR CohortCustomers = 
    FILTER(
        ALL('Sales'[Customer ID]),
        [Cohort Month] = MAX('Calendar'[Month Year])
    )
RETURN
    CALCULATE(
        DIVIDE(
            SUM('Sales'[Sales Amount]),
            DISTINCTCOUNT('Sales'[Customer ID])
        ),
        CohortCustomers
    )

// Average Revenue Per Customer (ARPC)
ARPC = 
DIVIDE(
    SUM('Sales'[Sales Amount]),
    DISTINCTCOUNT('Sales'[Customer ID]),
    0
)

// Cumulative Revenue per Cohort
Cumulative Revenue = 
VAR CohortCustomers = 
    FILTER(
        ALL('Sales'[Customer ID]),
        [Cohort Month] = MAX('Calendar'[Month Year])
    )
RETURN
    CALCULATE(
        SUM('Sales'[Sales Amount]),
        CohortCustomers,
        'Sales'[Order Date] <= MAX('Calendar'[Date])
    )
```

## Cohort Matrix Visualization

### Retention Matrix

| Cohort Month | Month 0 | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 |
|--------------|---------|---------|---------|---------|---------|----------|
| 2024-01      | 100%    | 45%     | 38%     | 35%     | 28%     | 22%      |
| 2024-02      | 100%    | 48%     | 42%     | 38%     | 31%     | -        |
| 2024-03      | 100%    | 52%     | 45%     | 40%     | -       | -        |
| 2024-04      | 100%    | 50%     | 44%     | -       | -       | -        |

### Revenue Matrix

| Cohort Month | Month 0 | Month 1 | Month 2 | Month 3 | Cumulative |
|--------------|---------|---------|---------|---------|------------|
| 2024-01      | $85     | $45     | $38     | $32     | $520       |
| 2024-02      | $92     | $48     | $41     | $35     | $485       |
| 2024-03      | $88     | $52     | $44     | -       | $410       |

## Key Metrics & Insights

### 1. Overall Retention Performance

```dax
// 30-Day Retention
30-Day Retention = 
CALCULATE(
    [Retention Rate %],
    'Parameters'[Months After Cohort] = 1
)

// 90-Day Retention
90-Day Retention = 
CALCULATE(
    [Retention Rate %],
    'Parameters'[Months After Cohort] = 3
)

// 1-Year Retention
1-Year Retention = 
CALCULATE(
    [Retention Rate %],
    'Parameters'[Months After Cohort] = 12
)
```

**Findings**:
- 30-day retention: 48% (industry benchmark: 40-60%)
- 90-day retention: 38% (good)
- 1-year retention: 22% (needs improvement)

### 2. Cohort Quality Analysis

```dax
// Best Performing Cohort
Best Cohort = 
VAR BestCohortLTV = 
    MAXX(
        VALUES('Calendar'[Month Year]),
        [Cohort LTV]
    )
RETURN
    CALCULATE(
        MAX('Calendar'[Month Year]),
        FILTER(
            VALUES('Calendar'[Month Year]),
            [Cohort LTV] = BestCohortLTV
        )
    )

// Cohort Performance vs Average
Cohort vs Avg = 
VAR CurrentLTV = [Cohort LTV]
VAR AvgLTV = CALCULATE(AVERAGE('Sales'[Sales Amount]), ALL('Calendar'))
RETURN
    DIVIDE(CurrentLTV - AvgLTV, AvgLTV, 0)
```

**Findings**:
- March 2024 cohort: Best performing (+18% vs average)
- Attributed to improved onboarding process
- January cohorts typically underperform (post-holiday effect)

### 3. Customer Behavior Patterns

```dax
// Repeat Purchase Rate
Repeat Purchase Rate = 
VAR TotalCustomers = DISTINCTCOUNT('Sales'[Customer ID])
VAR RepeatCustomers = 
    COUNTROWS(
        FILTER(
            VALUES('Sales'[Customer ID]),
            CALCULATE(DISTINCTCOUNT('Sales'[Order ID])) > 1
        )
    )
RETURN
    DIVIDE(RepeatCustomers, TotalCustomers, 0)

// Average Days Between Purchases
Avg Days Between Purchases = 
AVERAGEX(
    FILTER(
        VALUES('Sales'[Customer ID]),
        CALCULATE(DISTINCTCOUNT('Sales'[Order ID])) > 1
    ),
    VAR FirstOrder = CALCULATE(MIN('Sales'[Order Date]))
    VAR LastOrder = CALCULATE(MAX('Sales'[Order Date]))
    VAR OrderCount = CALCULATE(DISTINCTCOUNT('Sales'[Order ID]))
    RETURN
        DIVIDE(
            DATEDIFF(FirstOrder, LastOrder, DAY),
            OrderCount - 1,
            0
        )
)

// Purchase Frequency
Purchase Frequency = 
DIVIDE(
    DISTINCTCOUNT('Sales'[Order ID]),
    DISTINCTCOUNT('Sales'[Customer ID]),
    0
)
```

**Findings**:
- Repeat purchase rate: 35%
- Average days between purchases: 42 days
- Average purchase frequency: 2.3 orders per customer

### 4. Customer Lifetime Value Prediction

```dax
// Predicted 12-Month LTV
Predicted LTV 12M = 
VAR AvgOrderValue = DIVIDE(SUM('Sales'[Sales Amount]), DISTINCTCOUNT('Sales'[Order ID]), 0)
VAR PurchaseFreq = [Purchase Frequency]
VAR RetentionRate = [90-Day Retention]
VAR Months = 12
RETURN
    AvgOrderValue * PurchaseFreq * RetentionRate * Months

// Customer Segment by LTV
LTV Segment = 
VAR PredictedLTV = [Predicted LTV 12M]
RETURN
    SWITCH(
        TRUE(),
        PredictedLTV >= 500, "💎 VIP (>$500)",
        PredictedLTV >= 250, "⭐ Premium ($250-500)",
        PredictedLTV >= 100, "✓ Standard ($100-250)",
        "○ Basic (<$100)"
    )
```

## At-Risk Customer Identification

```dax
// Days Since Last Purchase
Days Since Last Purchase = 
DATEDIFF(
    CALCULATE(MAX('Sales'[Order Date])),
    MAX('Calendar'[Date]),
    DAY
)

// At-Risk Flag
At-Risk Customer = 
VAR DaysSincePurchase = [Days Since Last Purchase]
VAR AvgDaysBetween = [Avg Days Between Purchases]
RETURN
    IF(
        DaysSincePurchase > (AvgDaysBetween * 1.5),
        "🚨 At Risk",
        "✓ Active"
    )

// Churn Probability
Churn Probability = 
VAR DaysSincePurchase = [Days Since Last Purchase]
VAR AvgDaysBetween = [Avg Days Between Purchases]
VAR Ratio = DIVIDE(DaysSincePurchase, AvgDaysBetween, 0)
RETURN
    SWITCH(
        TRUE(),
        Ratio < 1, 0.10,
        Ratio < 1.5, 0.30,
        Ratio < 2, 0.60,
        Ratio < 3, 0.85,
        0.95
    )
```

## Retention Strategies by Segment

### High-Value Customers (VIP)
- **Action**: Exclusive perks, dedicated support
- **Target Retention**: 80%+
- **Investment**: $50-100 per customer

### At-Risk Customers
- **Action**: Win-back campaign, discount offers
- **Target**: Reduce churn by 20%
- **Investment**: $15-30 per customer

### New Customers (Month 0-3)
- **Action**: Onboarding emails, first-purchase discounts
- **Target**: 50% 90-day retention
- **Investment**: $10-20 per customer

## Dashboard Design

### Cohort Retention Matrix
- Heatmap showing retention % by cohort and month
- Color-coded: Green (>50%), Yellow (30-50%), Red (<30%)

### Customer Lifecycle
- Funnel visualization: Acquisition → Activation → Retention → Revenue
- Conversion rates at each stage

### At-Risk Customers
- Table with customer list, days since purchase, churn probability
- Action buttons: Send email, Apply discount

## ROI Calculations

```dax
// Customer Acquisition Cost (CAC)
CAC = 
DIVIDE(
    SUM('Marketing'[Campaign Cost]),
    COUNTROWS(VALUES('Customers'[Customer ID])),
    0
)

// LTV to CAC Ratio
LTV to CAC Ratio = 
DIVIDE([Cohort LTV], [CAC], 0)

// Payback Period (Months)
Payback Period = 
DIVIDE(
    [CAC],
    [ARPC],
    0
)

// ROI on Retention Campaign
Retention ROI = 
VAR CampaignCost = SUM('Marketing'[Retention Campaign Cost])
VAR CustomersRetained = 
    CALCULATE(
        DISTINCTCOUNT('Sales'[Customer ID]),
        'Marketing'[Campaign Type] = "Retention"
    )
VAR RevenueFromRetained = 
    CALCULATE(
        SUM('Sales'[Sales Amount]),
        'Marketing'[Campaign Type] = "Retention"
    )
RETURN
    DIVIDE(RevenueFromRetained - CampaignCost, CampaignCost, 0)
```

**Findings**:
- CAC: $45
- Average LTV: $220
- LTV:CAC Ratio: 4.9:1 (healthy - target >3:1)
- Payback period: 2.8 months
- Retention campaign ROI: 320%

## Key Recommendations

1. **Improve Month 1-3 Retention**:
   - Implement automated onboarding email series
   - Offer second-purchase discount (15% off)
   - Expected impact: +10% retention

2. **VIP Program**:
   - Create loyalty program for top 10% customers
   - Offer exclusive access, early releases
   - Expected LTV increase: +25%

3. **Win-Back Campaign**:
   - Target customers inactive >60 days
   - Personalized recommendations
   - Expected reactivation: 15-20%

4. **Cohort-Specific Strategies**:
   - Holiday cohorts: Lower retention, adjust expectations
   - Spring cohorts: Higher quality, invest more

## DAX Patterns Used
- ✅ Cohort Analysis
- ✅ Time Intelligence
- ✅ Customer Segmentation
- ✅ Statistical Analysis
- ✅ Dynamic KPIs

## Next Steps

1. Implement dashboard in Power BI
2. Set up automated alerts for at-risk customers
3. A/B test retention strategies
4. Build predictive churn model
5. Integrate with CRM system
