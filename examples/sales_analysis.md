# Sales Analysis - Real-World Example

## Business Context

A retail company wants to analyze sales performance across multiple dimensions: time, geography, products, and customers. The goal is to identify trends, opportunities, and areas for improvement.

## Dataset Structure

### Tables
- **Sales**: Transaction-level data (Order ID, Date, Customer ID, Product ID, Quantity, Amount, Cost)
- **Calendar**: Date dimension (Date, Year, Quarter, Month, Week, Day, IsWorkingDay)
- **Products**: Product master (Product ID, Name, Category, Subcategory)
- **Customers**: Customer master (Customer ID, Name, Segment, Region)
- **Geography**: Geographic hierarchy (Country, Region, City)

### Relationships
```
Calendar[Date] 1:N Sales[Order Date]
Products[Product ID] 1:N Sales[Product ID]
Customers[Customer ID] 1:N Sales[Customer ID]
Geography[Region] 1:N Customers[Region]
```

## Key Business Questions

### 1. Revenue Performance
**Question**: How are sales performing compared to last year and target?

**DAX Measures**:
```dax
// Current Sales
Total Sales = SUM('Sales'[Sales Amount])

// Previous Year Sales
PY Sales = 
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)

// YoY Growth
YoY Growth % = 
DIVIDE([Total Sales] - [PY Sales], [PY Sales], 0)

// Sales Target
Sales Target = SUM('Targets'[Target Amount])

// Variance to Target
Variance to Target = [Total Sales] - [Sales Target]
Variance % = DIVIDE([Variance to Target], [Sales Target], 0)
```

**Visual**: Line chart showing Total Sales, PY Sales, and Target over time

**Insight**: 
- Q3 2024 shows 15% YoY growth
- Currently 8% above target
- Strong performance in East region driving overall results

### 2. Product Performance
**Question**: Which products are top performers? What's the 80/20 distribution?

**DAX Measures**:
```dax
// Product Rank
Product Rank = 
RANKX(
    ALL('Products'[Product Name]),
    [Total Sales],
    ,
    DESC,
    DENSE
)

// Cumulative % (Pareto)
Cumulative % = 
VAR CurrentRank = [Product Rank]
VAR ProductsUpToCurrent = 
    FILTER(
        ALL('Products'[Product Name]),
        [Product Rank] <= CurrentRank
    )
RETURN
    DIVIDE(
        CALCULATE([Total Sales], ProductsUpToCurrent),
        CALCULATE([Total Sales], ALL('Products')),
        0
    )

// ABC Classification
ABC Class = 
SWITCH(
    TRUE(),
    [Cumulative %] <= 0.70, "A - Critical",
    [Cumulative %] <= 0.90, "B - Important",
    "C - Standard"
)
```

**Visual**: Pareto chart with products on X-axis, sales bars, and cumulative % line

**Insight**:
- Top 20% of products (45 items) generate 78% of revenue
- Focus inventory management on Class A products
- Class C products may be candidates for discontinuation

### 3. Customer Retention
**Question**: How well are we retaining customers month-over-month?

**DAX Measures**:
```dax
// Retention Rate
Retention Rate = 
VAR CustomersLastMonth = 
    CALCULATE(
        DISTINCTCOUNT('Sales'[Customer ID]),
        DATEADD('Calendar'[Date], -1, MONTH)
    )
VAR RetainedCustomers = 
    CALCULATE(
        DISTINCTCOUNT('Sales'[Customer ID]),
        FILTER(
            'Sales',
            'Sales'[Customer ID] IN 
                CALCULATETABLE(
                    VALUES('Sales'[Customer ID]),
                    DATEADD('Calendar'[Date], -1, MONTH)
                )
        )
    )
RETURN
    DIVIDE(RetainedCustomers, CustomersLastMonth, 0)

// Churn Rate
Churn Rate = 1 - [Retention Rate]

// Customer Lifetime Value
Customer LTV = 
DIVIDE(
    [Total Sales],
    DISTINCTCOUNT('Sales'[Customer ID]),
    0
)
```

**Visual**: Line chart showing retention rate and churn rate over time

**Insight**:
- Average retention rate: 82%
- Churn increased to 22% in March (investigate cause)
- Implement win-back campaign for churned customers

### 4. Seasonality Analysis
**Question**: What are our seasonal patterns and how should we plan inventory?

**DAX Measures**:
```dax
// Monthly Average
Monthly Avg Sales = 
CALCULATE(
    AVERAGE('Sales'[Sales Amount]),
    ALL('Calendar')
)

// Seasonality Index
Seasonality Index = 
VAR CurrentMonth = MONTH(MAX('Calendar'[Date]))
VAR CurrentMonthAvg = 
    CALCULATE(
        AVERAGE('Sales'[Sales Amount]),
        FILTER(
            ALL('Calendar'),
            MONTH('Calendar'[Date]) = CurrentMonth
        )
    )
RETURN
    DIVIDE(CurrentMonthAvg, [Monthly Avg Sales], 1)

// 3-Month Moving Average
3M MA = 
AVERAGEX(
    DATESINPERIOD(
        'Calendar'[Date],
        LASTDATE('Calendar'[Date]),
        -3,
        MONTH
    ),
    [Total Sales]
)
```

**Visual**: Column chart with monthly sales and 3M MA line

**Insight**:
- Strong seasonality: November-December (holiday season) 40% above average
- January-February dip (post-holiday)
- Plan inventory increases in Q4

### 5. Regional Performance
**Question**: Which regions are performing best and where should we focus expansion?

**DAX Measures**:
```dax
// Regional Rank
Regional Rank = 
RANKX(
    ALL('Geography'[Region]),
    [Total Sales],
    ,
    DESC
)

// Regional Market Share
Regional Share = 
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL('Geography'[Region])),
    0
)

// Regional Growth
Regional YoY Growth = 
VAR CurrentSales = [Total Sales]
VAR PYSales = [PY Sales]
RETURN
    DIVIDE(CurrentSales - PYSales, PYSales, 0)
```

**Visual**: Map visualization with bubble size = sales, color = growth rate

**Insight**:
- East region: #1 in sales ($2.5M) but slowing growth (3%)
- West region: #3 in sales but fastest growth (25%)
- South region: Underperforming, needs strategic review

## Dashboard Design

### Executive Dashboard
1. **KPI Cards**: Total Sales, YoY Growth, Target Achievement, Customer Count
2. **Trend Chart**: Sales over time (actual vs target vs PY)
3. **Regional Map**: Sales by geography
4. **Top 10 Products**: Bar chart

### Detailed Analysis
1. **Pareto Analysis**: Product contribution chart
2. **Cohort Analysis**: Customer retention matrix
3. **Seasonality**: Monthly patterns with forecast
4. **Drill-through**: Product details, Customer details

## Key Findings & Recommendations

### Findings
1. ✅ Overall sales growing 12% YoY
2. ✅ 8% above target consistently
3. ⚠️ Customer churn increased in Q1
4. ⚠️ High concentration in top 20% of products
5. ✅ West region showing strong growth potential

### Recommendations
1. **Immediate Actions**:
   - Investigate Q1 churn spike
   - Launch customer retention campaign
   - Increase marketing in West region

2. **Strategic Initiatives**:
   - Diversify product portfolio to reduce concentration risk
   - Develop region-specific strategies
   - Implement seasonal inventory planning

3. **Next Analysis**:
   - Deep-dive into customer segments
   - Profitability analysis (not just revenue)
   - Competitor benchmarking

## DAX Patterns Used
- ✅ Time Intelligence (YTD, YoY, MoM)
- ✅ Ranking & Top N
- ✅ Moving Averages
- ✅ Pareto Analysis
- ✅ Cohort Analysis
- ✅ Dynamic KPIs

## Files Required
- `dax_patterns/time_intelligence.dax`
- `dax_patterns/ranking.dax`
- `dax_patterns/moving_averages.dax`
- `dax_patterns/pareto.dax`
- `dax_patterns/cohort_analysis.dax`
- `dax_patterns/dynamic_kpis.dax`
