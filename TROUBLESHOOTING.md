# Troubleshooting Guide

## Common Issues and Solutions

### DAX Formula Issues

#### Issue: Measure returns BLANK or unexpected results

**Symptoms:**
- Measure shows (Blank) in visuals
- Results don't match expectations
- Totals incorrect

**Common Causes & Solutions:**

1. **Filter Context Issues**
   ```dax
   // Problem: Not considering filter context
   Wrong = SUM(Sales[Amount])
   
   // Solution: Use CALCULATE to modify filter context
   Correct = 
   CALCULATE(
       SUM(Sales[Amount]),
       // Add appropriate filters
   )
   ```

2. **Missing Relationships**
   - Check if tables are properly related
   - Verify relationship direction (single vs bi-directional)
   - Ensure active relationships exist

3. **Data Type Mismatches**
   ```dax
   // Problem: Comparing different data types
   Wrong = IF(Sales[Date] = "2024-01-01", 1, 0)
   
   // Solution: Convert to proper type
   Correct = IF(Sales[Date] = DATE(2024, 1, 1), 1, 0)
   ```

#### Issue: "A circular dependency was detected"

**Symptoms:**
- Error when creating or modifying measure
- Measure references itself directly or indirectly

**Solution:**
```dax
// Problem: Circular reference
Measure A = [Measure B]
Measure B = [Measure A]

// Solution: Break the circular chain
// Use a different calculation approach
// Or consolidate into a single measure
```

#### Issue: "The expression refers to multiple columns"

**Symptoms:**
- Error when using table column in scalar context

**Solution:**
```dax
// Problem: Using table column where scalar expected
Wrong = IF(Products[Category] = "Electronics", 1, 0)

// Solution: Use SELECTEDVALUE or MAX/MIN for single value
Correct = IF(SELECTEDVALUE(Products[Category]) = "Electronics", 1, 0)
```

### Performance Issues

#### Issue: Dashboard loads slowly

**Diagnosis:**
1. Use DAX Studio to analyze query performance
2. Check query execution time
3. Identify bottlenecks

**Solutions:**

1. **Avoid Calculated Columns in Large Tables**
   ```dax
   // Bad: Calculated column (stored in model)
   Profit Column = Sales[Amount] - Sales[Cost]
   
   // Good: Measure (calculated on-demand)
   Profit = SUM(Sales[Amount]) - SUM(Sales[Cost])
   ```

2. **Use Variables to Avoid Redundant Calculations**
   ```dax
   // Bad: Calculates SUM three times
   Bad Measure = 
   IF(
       SUM(Sales[Amount]) > 1000,
       SUM(Sales[Amount]) * 0.9,
       SUM(Sales[Amount])
   )
   
   // Good: Calculates once
   Good Measure = 
   VAR TotalSales = SUM(Sales[Amount])
   RETURN
       IF(TotalSales > 1000, TotalSales * 0.9, TotalSales)
   ```

3. **Optimize Relationships**
   - Use integer keys instead of text
   - Avoid many-to-many relationships
   - Use single-direction filtering when possible

4. **Reduce Model Size**
   - Remove unnecessary columns
   - Disable auto date/time hierarchy
   - Use appropriate data types

#### Issue: Specific measure is slow

**Tools:** DAX Studio

1. **Analyze Query Plan**
   ```
   DAX Studio → Run Query → View Server Timings
   ```

2. **Check Storage Engine vs Formula Engine**
   - Storage Engine (SE): Fast (compressed data)
   - Formula Engine (FE): Slow (row-by-row iteration)
   - Optimize to use SE as much as possible

3. **Common Slow Patterns:**
   ```dax
   // Slow: Nested iterators
   Slow = 
   SUMX(
       Products,
       SUMX(
           FILTER(Sales, Sales[ProductID] = Products[ProductID]),
           Sales[Amount]
       )
   )
   
   // Fast: Use relationships
   Fast = 
   SUMX(
       Products,
       CALCULATE(SUM(Sales[Amount]))
   )
   ```

### Time Intelligence Issues

#### Issue: Time intelligence functions return blank

**Common Causes:**

1. **Missing Calendar Table**
   ```dax
   // Create Calendar table
   Calendar = 
   CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31))
   
   // Mark as date table
   // Right-click → "Mark as Date Table"
   ```

2. **Calendar Table Not Marked as Date Table**
   - Right-click Calendar table
   - Select "Mark as Date Table"
   - Choose the Date column

3. **Relationship Not Configured**
   - Ensure Calendar[Date] relates to Fact table date columns
   - Check relationship is active

4. **Non-Continuous Date Range**
   ```dax
   // Problem: Dates have gaps
   // Solution: Use CALENDAR or CALENDARAUTO for continuous dates
   Calendar = CALENDARAUTO()
   ```

#### Issue: YTD showing incorrect values

**Check:**
1. Fiscal vs Calendar year alignment
2. Filter context being applied

**Solution:**
```dax
// For Fiscal Year starting July 1st
Sales FYTD = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESYTD('Calendar'[Date], "06-30")  // Fiscal year ends June 30
)
```

### Validation Tool Issues

#### Issue: Validator script won't run

**Error:** `Permission denied`

**Solution:**
```bash
# Make script executable
chmod +x tests/validate_dax.py

# Or run with python explicitly
python3 tests/validate_dax.py dax_patterns/
```

**Error:** `python3: command not found`

**Solution:**
```bash
# Install Python 3
# Ubuntu/Debian
sudo apt-get install python3

# macOS
brew install python3

# Windows: Download from python.org
```

#### Issue: False positive validation warnings

**Scenario:** Validator reports warning but DAX is correct

**Solution:**
- Check if it's a warning (not error) - warnings can be ignored
- Review the warning context
- If incorrect, report issue on GitHub with DAX example

### Power BI Desktop Issues

#### Issue: Can't paste DAX from repository

**Solution:**
1. Copy entire measure including name and `=` sign
2. In Power BI: Modeling → New Measure
3. Delete default name and paste copied measure
4. Adapt table/column names to your model

#### Issue: Table/column names don't match

**Solution:**
```dax
// Replace table/column references
// Original
SUM('Sales'[Sales Amount])

// Your model
SUM('YourSalesTable'[YourAmountColumn])

// Use Find & Replace (Ctrl+H) to update all instances
```

#### Issue: Measure shows error after pasting

**Common Causes:**
1. Missing tables or columns in your model
2. Different data types
3. Missing relationships

**Solution:**
1. Read error message carefully
2. Check if referenced tables/columns exist
3. Adapt measure to your model structure

### Data Model Issues

#### Issue: Relationships not working

**Symptoms:**
- Measures return wrong values
- Filters not propagating

**Solutions:**

1. **Check Relationship Direction**
   - One-to-many: Dimension (1) → Fact (many)
   - Direction: Single (dimension to fact)

2. **Check Data Types Match**
   ```
   Products[ProductID] (Integer) → Sales[ProductID] (Integer) ✓
   Products[ProductID] (Text) → Sales[ProductID] (Integer) ✗
   ```

3. **Check for Duplicates in "One" Side**
   - The "one" side must have unique values
   - Remove duplicates or use proper key column

4. **Multiple Relationships to Same Table**
   ```dax
   // Use USERELATIONSHIP for inactive relationships
   Sales by Ship Date = 
   CALCULATE(
       SUM(Sales[Amount]),
       USERELATIONSHIP(Sales[ShipDate], Calendar[Date])
   )
   ```

## Getting Help

### Before Asking for Help

1. ✅ Check this troubleshooting guide
2. ✅ Test measure in simple scenario
3. ✅ Run DAX validator: `python3 tests/validate_dax.py your_file.dax -v`
4. ✅ Check DAX formula syntax at [dax.guide](https://dax.guide)
5. ✅ Search existing GitHub issues

### How to Report an Issue

When reporting an issue, include:

1. **Description:** Clear description of the problem
2. **DAX Code:** The measure causing issues (formatted as code block)
3. **Expected Result:** What you expected to happen
4. **Actual Result:** What actually happened
5. **Error Message:** Full error message if any
6. **Context:** 
   - Power BI Desktop version
   - Data model structure (table names, relationships)
   - Sample data (if possible)

**Example Issue Report:**
```
Title: YTD Sales measure returns blank

Description:
I'm trying to use the YTD Sales measure from time_intelligence.dax 
but it returns blank in my report.

DAX Code:
```dax
Sales YTD = 
TOTALYTD(
    SUM('Sales'[Sales Amount]),
    'Calendar'[Date]
)
```

Expected: Should show year-to-date sales values
Actual: Shows (Blank) for all rows

Context:
- Power BI Desktop version: August 2024
- I have a Calendar table with Date column
- Calendar[Date] is related to Sales[OrderDate]
- Calendar table is marked as Date Table

Error Message: None, just shows blank
```

### Resources

- 📚 [DAX Guide](https://dax.guide/) - Complete DAX function reference
- 🎓 [SQLBI](https://www.sqlbi.com/) - Advanced DAX patterns and training
- 🛠️ [DAX Studio](https://daxstudio.org/) - Free DAX development tool
- 💬 [Power BI Community](https://community.powerbi.com/) - Official forum
- 📖 [Microsoft Docs](https://docs.microsoft.com/power-bi/) - Official documentation

### Community Support

- 🐛 [GitHub Issues](https://github.com/galafis/powerbi-dax-advanced-analytics-patterns/issues) - Bug reports and feature requests
- 💡 [GitHub Discussions](https://github.com/galafis/powerbi-dax-advanced-analytics-patterns/discussions) - Questions and discussions

