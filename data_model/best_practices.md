# Data Modeling Best Practices for Power BI

## Overview

A well-designed data model is the foundation of high-performing Power BI reports. This guide covers best practices for building efficient, scalable data models.

## Star Schema Design

### What is Star Schema?

Star schema is the optimal design pattern for Power BI, consisting of:
- **Fact Tables**: Contain measures/metrics (Sales, Orders, Inventory)
- **Dimension Tables**: Contain descriptive attributes (Products, Customers, Calendar)

### Benefits
- ✅ Simple and intuitive
- ✅ Fast query performance
- ✅ Easy to understand and maintain
- ✅ Optimized for BI tools

### Star Schema Example

```
        ┌─────────────┐
        │  Calendar   │
        │  (Dimension)│
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │    Sales    │ ◄────┐
        │    (Fact)   │      │
        └──────┬──────┘      │
               │             │
        ┌──────▼──────┐      │
        │  Products   │      │
        │  (Dimension)│      │
        └─────────────┘      │
                             │
        ┌─────────────┐      │
        │  Customers  │ ─────┘
        │  (Dimension)│
        └─────────────┘
```

## Fact Tables

### Characteristics
- Contain numeric measures (sales amount, quantity, cost)
- Have foreign keys to dimension tables
- Typically large (millions of rows)
- Grain: One row per transaction/event

### Best Practices

1. **Keep Fact Tables Narrow**
   - Only include foreign keys and measures
   - Remove descriptive columns (move to dimensions)
   - Use integer keys instead of strings

2. **Use Integer Keys**
   ```dax
   // Good: Integer surrogate key
   Sales[ProductKey] (Integer)
   
   // Bad: String natural key
   Sales[ProductSKU] (Text)
   ```

3. **Pre-Aggregate When Possible**
   - For very large datasets, consider daily/monthly aggregations
   - Balance between detail and performance

4. **Avoid Calculated Columns in Fact Tables**
   - Use measures instead
   - Exception: If needed for relationships or filtering

### Example Fact Table Structure

**Sales Fact Table**
```
OrderID (Integer, Key)
OrderDate (Date, FK to Calendar)
CustomerID (Integer, FK to Customers)
ProductID (Integer, FK to Products)
StoreID (Integer, FK to Stores)
Quantity (Integer)
SalesAmount (Decimal)
Cost (Decimal)
Discount (Decimal)
```

## Dimension Tables

### Characteristics
- Contain descriptive attributes
- Relatively small (thousands of rows)
- Wide (many columns acceptable)
- One-to-many relationship to facts

### Best Practices

1. **Create Hierarchies**
   ```
   Products
   ├── Category
   │   └── Subcategory
   │       └── Product Name
   
   Geography
   ├── Country
   │   └── State
   │       └── City
   ```

2. **Include All Descriptive Attributes**
   - Product name, color, size, category
   - Customer name, segment, region
   - Store name, type, location

3. **Use Meaningful Names**
   - "Product Name" not "ProductNm"
   - "Customer Segment" not "CustSeg"

4. **Sort Columns Correctly**
   - Months sorted chronologically, not alphabetically
   - Use "Sort By Column" feature

### Example Dimension Tables

**Products Dimension**
```
ProductID (Integer, Key)
ProductSKU (Text)
ProductName (Text)
Category (Text)
Subcategory (Text)
Brand (Text)
Color (Text)
Size (Text)
UnitCost (Decimal)
UnitPrice (Decimal)
```

**Customers Dimension**
```
CustomerID (Integer, Key)
CustomerName (Text)
Email (Text)
Segment (Text)
Country (Text)
Region (Text)
City (Text)
RegistrationDate (Date)
```

## Calendar/Date Table

### Why Essential?
- Required for time intelligence functions
- Enables period comparisons (YoY, MoM)
- Provides consistent date attributes

### Best Practices

1. **Always Create a Calendar Table**
   ```dax
   Calendar = 
   ADDCOLUMNS(
       CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31)),
       "Year", YEAR([Date]),
       "Quarter", "Q" & QUARTER([Date]),
       "Month", FORMAT([Date], "MMM"),
       "MonthNumber", MONTH([Date]),
       "MonthYear", FORMAT([Date], "MMM YYYY"),
       "WeekNumber", WEEKNUM([Date]),
       "DayOfWeek", FORMAT([Date], "ddd"),
       "DayOfWeekNumber", WEEKDAY([Date]),
       "IsWorkingDay", IF(WEEKDAY([Date]) IN {2,3,4,5,6}, TRUE, FALSE)
   )
   ```

2. **Mark as Date Table**
   - Right-click table → "Mark as Date Table"
   - Select the Date column

3. **Include Fiscal Calendar** (if applicable)
   ```dax
   "FiscalYear", 
   IF(
       MONTH([Date]) >= 7,  // Fiscal year starts July
       YEAR([Date]),
       YEAR([Date]) - 1
   )
   ```

4. **Create Useful Flags**
   ```dax
   "IsToday", [Date] = TODAY()
   "IsYTD", [Date] <= TODAY()
   "IsLastMonth", MONTH([Date]) = MONTH(TODAY()) - 1
   ```

## Relationships

### Relationship Types

1. **One-to-Many (Preferred)**
   - Dimension (1) to Fact (Many)
   - Example: Products (1) → Sales (Many)

2. **Many-to-Many (Avoid)**
   - Requires bridge table
   - Performance impact
   - Complex behavior

### Relationship Best Practices

1. **Single Direction Filtering**
   - One-to-Many: Single direction
   - Bi-directional only when absolutely necessary

2. **Active vs Inactive Relationships**
   - One active relationship per table pair
   - Use USERELATIONSHIP() for inactive relationships

3. **Integer Keys for Performance**
   ```
   // Good
   Products[ProductID] (Integer) → Sales[ProductID] (Integer)
   
   // Bad
   Products[SKU] (Text) → Sales[SKU] (Text)
   ```

### Example: Multiple Date Relationships

```
Sales Table has:
- OrderDate
- ShipDate
- DueDate

Solution:
- Active relationship: OrderDate → Calendar[Date]
- Inactive relationships: ShipDate, DueDate → Calendar[Date]

Usage:
Shipped Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    USERELATIONSHIP(Sales[ShipDate], Calendar[Date])
)
```

## Performance Optimization

### 1. Reduce Model Size

**Remove Unnecessary Columns**
```dax
// In Power Query, remove columns not needed for analysis
// Keep only: Keys, Measures, Filter attributes
```

**Use Integers Instead of Strings**
```dax
// Replace text IDs with integer surrogate keys
// Example: CustomerID (Integer) instead of Email (Text)
```

**Disable Auto Date/Time**
```
File → Options → Data Load
Uncheck "Auto date/time"
```

### 2. Optimize Data Types

| Data Type | Size | Use Case |
|-----------|------|----------|
| Integer | 4 bytes | Keys, Quantities |
| Decimal | 8 bytes | Amounts, Prices |
| Date | 8 bytes | Dates only (no time) |
| DateTime | 8 bytes | Timestamps |
| Text | Variable | Descriptions |
| Boolean | 1 byte | Flags |

### 3. Use Measures, Not Calculated Columns

**Bad (Calculated Column)**
```dax
// Calculated for every row, stored in model
Profit = Sales[Amount] - Sales[Cost]
```

**Good (Measure)**
```dax
// Calculated on-demand, not stored
Profit = SUM(Sales[Amount]) - SUM(Sales[Cost])
```

### 4. Avoid High Cardinality Columns

- Don't use email addresses or long text fields as keys
- Replace with integer surrogate keys
- Move to separate lookup table if needed

### 5. Use Aggregations (For Very Large Models)

```dax
// Create aggregated table for fast queries
Sales_Monthly = 
SUMMARIZECOLUMNS(
    'Calendar'[Year],
    'Calendar'[Month],
    'Products'[Category],
    "Sales", SUM('Sales'[Amount]),
    "Quantity", SUM('Sales'[Quantity])
)
```

## Common Anti-Patterns to Avoid

### 1. ❌ Flat Tables (No Star Schema)

**Problem**: Single table with all data
```
Sales_and_Products_and_Customers_All_In_One
├── OrderID
├── CustomerName
├── CustomerEmail
├── CustomerSegment
├── ProductName
├── ProductCategory
├── SalesAmount
└── ... (100+ columns)
```

**Solution**: Split into star schema with separate dimension tables

### 2. ❌ Many-to-Many Relationships

**Problem**: Direct M:N relationship
```
Products ←→ Sales ←→ Campaigns
```

**Solution**: Create bridge table
```
Products → Product_Campaign_Bridge ← Campaigns
                 ↓
               Sales
```

### 3. ❌ Bi-Directional Filtering Everywhere

**Problem**: All relationships set to bi-directional
**Impact**: Slower performance, unexpected results
**Solution**: Use single direction; enable bi-directional only when necessary

### 4. ❌ Calculated Columns in Fact Tables

**Problem**: Adds to model size, calculated for every row
**Solution**: Use measures or Power Query for transformations

### 5. ❌ Missing Calendar Table

**Problem**: Using Date field directly from fact table
**Solution**: Always create dedicated Calendar table

## Advanced Patterns

### Role-Playing Dimensions

**Scenario**: Multiple date fields in fact table

```
Calendar Table (Role-Playing)
├── Used as: Order Date (Active)
├── Used as: Ship Date (Inactive)
└── Used as: Due Date (Inactive)

Measures:
Sales by Order Date = SUM(Sales[Amount])
Sales by Ship Date = CALCULATE(SUM(Sales[Amount]), USERELATIONSHIP(Sales[ShipDate], Calendar[Date]))
```

### Parent-Child Hierarchies

**Scenario**: Employee reporting structure

```dax
// Create hierarchy path
Employee Path = 
PATH(Employees[EmployeeID], Employees[ManagerID])

// Calculate at specific level
Level 2 Manager = 
PATHITEM([Employee Path], 2, TEXT)
```

### Slowly Changing Dimensions (SCD)

**Type 1**: Overwrite (No history)
```
ProductName: "Widget" → "Super Widget"
```

**Type 2**: Add new row (Keep history)
```
Row 1: ProductID=1, Name="Widget", ValidFrom=2023-01-01, ValidTo=2024-01-01
Row 2: ProductID=1, Name="Super Widget", ValidFrom=2024-01-01, ValidTo=9999-12-31
```

## Model Documentation Checklist

- [ ] Data source documented
- [ ] Table purposes documented
- [ ] Relationship directions documented
- [ ] Key measures documented with DAX
- [ ] Refresh schedule defined
- [ ] Row counts tracked
- [ ] Performance benchmarks recorded

## Validation Queries

```dax
// Check for missing relationships
EVALUATE
ADDCOLUMNS(
    FILTER(
        INFO.TABLES(),
        NOT ISEMPTY(FILTER(INFO.RELATIONSHIPS(), [To_Table] = EARLIER([Name])))
    ),
    "HasRelationships", 
    COUNTROWS(FILTER(INFO.RELATIONSHIPS(), [To_Table] = EARLIER([Name])))
)

// Check data types
EVALUATE INFO.COLUMNS()

// Check cardinality
EVALUATE
ADDCOLUMNS(
    INFO.TABLES(),
    "RowCount", [Rows],
    "ColumnCount", COUNTROWS(FILTER(INFO.COLUMNS(), [Table_Name] = EARLIER([Name])))
)
```

## Resources

- **Star Schema**: Ralph Kimball - "The Data Warehouse Toolkit"
- **DAX Performance**: SQLBI - "The Definitive Guide to DAX"
- **Power BI Optimization**: Microsoft Docs - Power BI Performance Best Practices
- **DAX Studio**: Free tool for performance analysis

## Summary

✅ **Do**:
- Use star schema design
- Create proper Calendar table
- Use integer keys
- Keep fact tables narrow
- Use measures over calculated columns
- Document your model

❌ **Don't**:
- Use flat tables
- Create many-to-many relationships directly
- Use bi-directional filtering unnecessarily
- Store calculations in columns
- Use high-cardinality keys
- Skip the Calendar table
