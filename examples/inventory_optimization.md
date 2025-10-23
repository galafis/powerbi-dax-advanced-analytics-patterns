# Inventory Optimization - Real-World Example

## Business Context

A manufacturing and distribution company needs to optimize inventory levels across multiple warehouses to minimize holding costs while maintaining service levels.

## Challenges

- **Stockouts**: Lost sales due to insufficient inventory
- **Overstock**: Excess capital tied up in slow-moving items
- **Seasonal Demand**: Product demand varies by season
- **Lead Times**: Varying supplier lead times
- **Multiple Locations**: Inventory spread across 15 warehouses

## Objective

- Optimize inventory levels by product and location
- Reduce holding costs by 15%
- Maintain 95% service level
- Implement ABC analysis for inventory prioritization
- Forecast demand and reorder points

## Dataset Structure

### Tables
```
Inventory[Product ID, Location, Current Stock, Unit Cost]
Sales[Order ID, Date, Product ID, Quantity Sold, Location]
Products[Product ID, Name, Category, Lead Time Days, Shelf Life]
Calendar[Date, Year, Quarter, Month, Week, Day]
Suppliers[Supplier ID, Name, Lead Time Days, Reliability %]
Targets[Product ID, Safety Stock, Reorder Point, Max Stock]
```

### Relationships
```
Calendar[Date] 1:N Sales[Order Date]
Products[Product ID] 1:N Sales[Product ID]
Products[Product ID] 1:N Inventory[Product ID]
Suppliers[Supplier ID] 1:N Products[Supplier ID]
```

## Key Metrics & Analysis

### 1. Inventory Performance

```dax
// Current Inventory Value
Inventory Value = 
SUMX(
    'Inventory',
    'Inventory'[Current Stock] * 'Inventory'[Unit Cost]
)

// Days of Inventory on Hand (DOH)
Days of Inventory = 
VAR AvgDailySales = 
    DIVIDE(
        CALCULATE(
            SUM('Sales'[Quantity]),
            DATESINPERIOD(
                'Calendar'[Date],
                MAX('Calendar'[Date]),
                -30,
                DAY
            )
        ),
        30,
        0
    )
VAR CurrentStock = SUM('Inventory'[Current Stock])
RETURN
    DIVIDE(CurrentStock, AvgDailySales, 0)

// Inventory Turnover Ratio
Inventory Turnover = 
VAR AnnualSales = 
    CALCULATE(
        SUM('Sales'[Quantity]),
        DATESINPERIOD(
            'Calendar'[Date],
            MAX('Calendar'[Date]),
            -365,
            DAY
        )
    )
VAR AvgInventory = AVERAGE('Inventory'[Current Stock])
RETURN
    DIVIDE(AnnualSales, AvgInventory, 0)

// Inventory Holding Cost (Annual)
Holding Cost Annual = 
VAR AvgInventoryValue = [Inventory Value]
VAR HoldingCostRate = 0.25  // 25% of inventory value per year
RETURN
    AvgInventoryValue * HoldingCostRate
```

**Current Performance**:
- Total inventory value: $4.2M
- Average DOH: 45 days (target: 35 days)
- Inventory turnover: 8.1x per year (industry avg: 10x)
- Annual holding cost: $1.05M

### 2. ABC Classification

```dax
// Annual Sales Volume by Product
Annual Sales Volume = 
CALCULATE(
    SUM('Sales'[Quantity]),
    DATESINPERIOD(
        'Calendar'[Date],
        MAX('Calendar'[Date]),
        -365,
        DAY
    )
)

// Annual Sales Value
Annual Sales Value = 
CALCULATE(
    SUMX(
        'Sales',
        'Sales'[Quantity] * RELATED('Products'[Unit Price])
    ),
    DATESINPERIOD(
        'Calendar'[Date],
        MAX('Calendar'[Date]),
        -365,
        DAY
    )
)

// Product Rank by Value
Product Rank by Value = 
RANKX(
    ALL('Products'[Product Name]),
    [Annual Sales Value],
    ,
    DESC,
    DENSE
)

// Cumulative % of Sales
Cumulative Sales % = 
VAR CurrentRank = [Product Rank by Value]
VAR ProductsUpToCurrent = 
    FILTER(
        ALL('Products'[Product Name]),
        [Product Rank by Value] <= CurrentRank
    )
RETURN
    DIVIDE(
        CALCULATE([Annual Sales Value], ProductsUpToCurrent),
        CALCULATE([Annual Sales Value], ALL('Products')),
        0
    )

// ABC Classification
ABC Class = 
VAR CumulativePct = [Cumulative Sales %]
RETURN
    SWITCH(
        TRUE(),
        CumulativePct <= 0.70, "A - High Priority",
        CumulativePct <= 0.90, "B - Medium Priority",
        "C - Low Priority"
    )
```

**ABC Distribution**:
- **Class A** (20% of SKUs): 70% of sales value → Daily monitoring, tight control
- **Class B** (30% of SKUs): 20% of sales value → Weekly monitoring, moderate control  
- **Class C** (50% of SKUs): 10% of sales value → Monthly monitoring, loose control

### 3. Demand Forecasting

```dax
// 30-Day Moving Average Demand
MA 30 Day Demand = 
AVERAGEX(
    DATESINPERIOD(
        'Calendar'[Date],
        LASTDATE('Calendar'[Date]),
        -30,
        DAY
    ),
    CALCULATE(SUM('Sales'[Quantity]))
)

// Seasonal Index
Seasonal Index = 
VAR CurrentMonth = MONTH(MAX('Calendar'[Date]))
VAR CurrentMonthAvg = 
    CALCULATE(
        AVERAGE('Sales'[Quantity]),
        FILTER(
            ALL('Calendar'),
            MONTH('Calendar'[Date]) = CurrentMonth
        )
    )
VAR OverallAvg = 
    CALCULATE(
        AVERAGE('Sales'[Quantity]),
        ALL('Calendar')
    )
RETURN
    DIVIDE(CurrentMonthAvg, OverallAvg, 1)

// Seasonally Adjusted Forecast
Forecast Next Month = 
VAR BaseForecast = [MA 30 Day Demand]
VAR NextMonth = MONTH(MAX('Calendar'[Date])) + 1
VAR SeasonalFactor = 
    CALCULATE(
        [Seasonal Index],
        FILTER(
            ALL('Calendar'),
            MONTH('Calendar'[Date]) = NextMonth
        )
    )
RETURN
    BaseForecast * SeasonalFactor * 30  // Monthly forecast

// Forecast Accuracy
Forecast Accuracy = 
VAR Actual = SUM('Sales'[Quantity])
VAR Forecast = [MA 30 Day Demand]
VAR Error = ABS(Actual - Forecast)
VAR MAPE = DIVIDE(Error, Actual, 0)  // Mean Absolute Percentage Error
RETURN
    1 - MAPE
```

**Forecast Performance**:
- 30-day MA forecast accuracy: 87%
- Seasonal adjustment improves accuracy by 8%
- Best accuracy: Class A products (92%)
- Worst accuracy: Class C products (73%)

### 4. Reorder Point Optimization

```dax
// Average Daily Demand
Avg Daily Demand = 
VAR Last90Days = 
    CALCULATE(
        SUM('Sales'[Quantity]),
        DATESINPERIOD(
            'Calendar'[Date],
            MAX('Calendar'[Date]),
            -90,
            DAY
        )
    )
RETURN
    DIVIDE(Last90Days, 90, 0)

// Demand Variability (Std Dev)
Demand Std Dev = 
VAR Last90Days = 
    CALCULATETABLE(
        'Calendar',
        DATESINPERIOD(
            'Calendar'[Date],
            MAX('Calendar'[Date]),
            -90,
            DAY
        )
    )
RETURN
    STDEVX.S(
        Last90Days,
        CALCULATE(SUM('Sales'[Quantity]))
    )

// Safety Stock (95% service level)
Safety Stock = 
VAR ServiceLevel = 0.95  // 95% service level
VAR ZScore = 1.65  // Z-score for 95% service level
VAR LeadTimeDays = MAX('Products'[Lead Time Days])
VAR StdDev = [Demand Std Dev]
RETURN
    ZScore * StdDev * SQRT(LeadTimeDays)

// Reorder Point
Reorder Point = 
VAR AvgDemand = [Avg Daily Demand]
VAR LeadTime = MAX('Products'[Lead Time Days])
VAR SafetyStock = [Safety Stock]
RETURN
    (AvgDemand * LeadTime) + SafetyStock

// Economic Order Quantity (EOQ)
EOQ = 
VAR AnnualDemand = [Annual Sales Volume]
VAR OrderingCost = 50  // Cost per order
VAR HoldingCostPerUnit = RELATED('Products'[Unit Cost]) * 0.25
RETURN
    SQRT(
        DIVIDE(
            (2 * AnnualDemand * OrderingCost),
            HoldingCostPerUnit,
            0
        )
    )

// Current Stock vs Reorder Point
Stock Status = 
VAR CurrentStock = SUM('Inventory'[Current Stock])
VAR ReorderPt = [Reorder Point]
VAR SafetyStock = [Safety Stock]
RETURN
    SWITCH(
        TRUE(),
        CurrentStock <= SafetyStock, "🔴 Critical - Order Immediately",
        CurrentStock <= ReorderPt, "🟡 Below Reorder Point",
        CurrentStock <= ReorderPt * 1.5, "🟢 Optimal",
        "⚠️ Overstock"
    )
```

### 5. Stockout Risk Analysis

```dax
// Days Until Stockout
Days Until Stockout = 
VAR CurrentStock = SUM('Inventory'[Current Stock])
VAR AvgDailyDemand = [Avg Daily Demand]
RETURN
    DIVIDE(CurrentStock, AvgDailyDemand, 0)

// Stockout Risk Level
Stockout Risk = 
VAR DaysUntilStockout = [Days Until Stockout]
VAR LeadTime = MAX('Products'[Lead Time Days])
RETURN
    SWITCH(
        TRUE(),
        DaysUntilStockout <= LeadTime, "🔴 High Risk (< Lead Time)",
        DaysUntilStockout <= LeadTime * 2, "🟡 Medium Risk",
        "🟢 Low Risk"
    )

// Potential Lost Sales
Potential Lost Sales = 
VAR CurrentStock = SUM('Inventory'[Current Stock])
VAR AvgDailyDemand = [Avg Daily Demand]
VAR DaysUntilStockout = [Days Until Stockout]
VAR LeadTime = MAX('Products'[Lead Time Days])
VAR UnitPrice = MAX('Products'[Unit Price])
RETURN
    IF(
        DaysUntilStockout < LeadTime,
        (LeadTime - DaysUntilStockout) * AvgDailyDemand * UnitPrice,
        0
    )

// Fill Rate (Service Level)
Fill Rate = 
VAR OrdersFilled = 
    CALCULATE(
        COUNTROWS('Sales'),
        'Sales'[Quantity] <= RELATED('Inventory'[Current Stock])
    )
VAR TotalOrders = COUNTROWS('Sales')
RETURN
    DIVIDE(OrdersFilled, TotalOrders, 0)
```

**Current Risk Status**:
- 12 products in critical stockout risk
- Potential lost sales: $45,000 if not addressed
- Current fill rate: 92% (target: 95%)
- Average days until stockout: 28 days

### 6. Overstock Analysis

```dax
// Excess Inventory Value
Excess Inventory Value = 
VAR CurrentStock = SUM('Inventory'[Current Stock])
VAR OptimalStock = [Reorder Point] * 2  // 2x reorder point as max
VAR ExcessUnits = MAX(CurrentStock - OptimalStock, 0)
VAR UnitCost = MAX('Inventory'[Unit Cost])
RETURN
    ExcessUnits * UnitCost

// Slow-Moving Items (< 1 turn per quarter)
Slow Moving Flag = 
VAR QuarterlyTurnover = [Inventory Turnover] / 4
RETURN
    IF(QuarterlyTurnover < 1, "🐌 Slow Moving", "✓ Normal")

// Dead Stock (No sales in 90 days)
Dead Stock = 
VAR Last90DaysSales = 
    CALCULATE(
        SUM('Sales'[Quantity]),
        DATESINPERIOD(
            'Calendar'[Date],
            MAX('Calendar'[Date]),
            -90,
            DAY
        )
    )
RETURN
    IF(Last90DaysSales = 0, "💀 Dead Stock", "✓ Active")

// Markdown Recommendation
Markdown Recommendation = 
VAR DaysOfInventory = [Days of Inventory]
VAR SlowMoving = [Slow Moving Flag]
RETURN
    SWITCH(
        TRUE(),
        DaysOfInventory > 90, "30% Markdown",
        DaysOfInventory > 60, "20% Markdown",
        DaysOfInventory > 45, "10% Markdown",
        "No Markdown Needed"
    )
```

**Overstock Issues**:
- Excess inventory value: $380,000
- 45 slow-moving SKUs
- 8 dead stock items (recommend clearance)
- Potential markdown revenue: $285,000

## Optimization Scenarios

### Scenario 1: Reduce Safety Stock

```dax
// Current Holding Cost
Current Holding Cost = [Holding Cost Annual]

// Optimized Safety Stock (90% service level)
Optimized Safety Stock = 
VAR ServiceLevel = 0.90
VAR ZScore = 1.28
VAR LeadTimeDays = MAX('Products'[Lead Time Days])
VAR StdDev = [Demand Std Dev]
RETURN
    ZScore * StdDev * SQRT(LeadTimeDays)

// Cost Savings
Safety Stock Savings = 
VAR CurrentSS = [Safety Stock]
VAR OptimizedSS = [Optimized Safety Stock]
VAR Reduction = CurrentSS - OptimizedSS
VAR UnitCost = MAX('Inventory'[Unit Cost])
VAR HoldingRate = 0.25
RETURN
    Reduction * UnitCost * HoldingRate
```

**Impact**: 
- Reduce safety stock by 15%
- Annual savings: $157,500
- Service level: 95% → 90% (acceptable trade-off)

### Scenario 2: Implement JIT for Class C

```dax
// JIT Potential Savings
JIT Savings = 
VAR ClassC_Value = 
    CALCULATE(
        [Inventory Value],
        'Products'[ABC Class] = "C - Low Priority"
    )
VAR ReductionPct = 0.50  // Reduce by 50%
VAR HoldingRate = 0.25
RETURN
    ClassC_Value * ReductionPct * HoldingRate
```

**Impact**:
- Reduce Class C inventory by 50%
- Annual savings: $52,500
- Minimal risk (low sales impact)

## Dashboard Design

### 1. Inventory Overview
- KPI Cards: Total Value, DOH, Turnover, Holding Cost
- Trend: Inventory levels over time
- ABC Pie Chart: Inventory distribution

### 2. Reorder Dashboard
- Table: Products below reorder point
- Stockout risk heatmap
- Recommended order quantities

### 3. Optimization Opportunities
- Overstock items (markdown candidates)
- Dead stock list
- Excess inventory value by category

### 4. Performance Metrics
- Fill rate trend
- Forecast accuracy
- Service level achievement

## Key Recommendations

### Immediate Actions (This Week)
1. **Place orders** for 12 critical stockout items
2. **Markdown** 8 dead stock items (30% discount)
3. **Transfer inventory** between warehouses to balance stock

### Short-term (This Month)
1. **Implement dynamic reorder points** based on seasonality
2. **Reduce safety stock** for Class B/C items
3. **Set up automated alerts** for stockout risk

### Long-term (This Quarter)
1. **JIT implementation** for Class C items
2. **Vendor consolidation** to reduce lead times
3. **Demand forecasting improvement** using machine learning

## Expected Results

### Cost Reduction
- Holding cost reduction: $210,000 annually (20%)
- Dead stock recovery: $285,000 (one-time)
- Total savings Year 1: $495,000

### Service Improvement
- Fill rate: 92% → 96%
- Stockout reduction: 60%
- Customer satisfaction: +8 points

### Operational Efficiency
- DOH: 45 → 35 days
- Inventory turnover: 8.1x → 10.4x
- Warehouse space freed: 15%

## DAX Patterns Used
- ✅ Statistical Analysis
- ✅ Time Intelligence
- ✅ Moving Averages
- ✅ ABC Classification (Pareto)
- ✅ What-If Analysis
- ✅ Dynamic KPIs

## Implementation Roadmap

**Month 1**: 
- Deploy dashboard
- Train team
- Implement alerts

**Month 2-3**:
- Optimize reorder points
- Reduce safety stock
- Clear dead stock

**Month 4-6**:
- JIT for Class C
- Automate ordering
- Review and refine

## Success Metrics

Track monthly:
- ✅ Inventory value
- ✅ Days of inventory
- ✅ Fill rate
- ✅ Holding cost
- ✅ Stockout incidents
- ✅ Excess inventory value
