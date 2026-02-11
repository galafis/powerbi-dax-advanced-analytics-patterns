# Testing Guide

## Overview

This repository includes automated validation for DAX formulas to ensure quality and consistency.

## DAX Validator

The DAX validator (`tests/validate_dax.py`) checks for:

### Syntax Checks
- ✅ Balanced parentheses, brackets, and braces
- ✅ Basic syntax validation
- ✅ Measure definition structure
- ✅ Unterminated strings

### Best Practices
- ⚠️ Use of DIVIDE() instead of / operator
- ⚠️ Nested CALCULATE functions
- ⚠️ VALUES() vs DISTINCT() usage

### Common Mistakes
- ❌ Non-existent functions (SUMIF, COUNTIF, etc.)
- ❌ Direct comparison with BLANK()
- ❌ Excel functions that don't exist in DAX

## Running Locally

### Prerequisites
```bash
# Python 3.7 or higher required
python3 --version
```

### Validate All DAX Files
```bash
# From repository root
python3 tests/validate_dax.py dax_patterns/

# Verbose mode
python3 tests/validate_dax.py dax_patterns/ -v

# JSON output
python3 tests/validate_dax.py dax_patterns/ --json
```

### Validate Specific File
```bash
python3 tests/validate_dax.py dax_patterns/time_intelligence.dax -v
```

### Validate Multiple Files
```bash
python3 tests/validate_dax.py dax_patterns/time_intelligence.dax dax_patterns/ranking.dax -v
```

## CI/CD Pipeline

The repository uses GitHub Actions to automatically validate DAX files on:
- Push to main/develop branches
- Pull requests to main branch

### Workflow Status

### What Gets Validated
- All `.dax` files in `dax_patterns/` directory
- Syntax correctness
- Best practice adherence
- Common mistake detection

## Adding New DAX Patterns

When adding new DAX patterns:

1. **Create file** in `dax_patterns/` directory
2. **Follow naming convention**: `pattern_name.dax`
3. **Use consistent format**:
   ```dax
   // ================================================
   // PATTERN CATEGORY NAME
   // Author: Your Name
   // Description: Brief description
   // ================================================
   
   // ------------------------------------------------
   // 1. SUBCATEGORY NAME
   // ------------------------------------------------
   
   // Measure Name
   Measure Name = 
   VAR Variable1 = ...
   RETURN
       Variable1
   ```

4. **Run validator** before committing:
   ```bash
   python3 tests/validate_dax.py dax_patterns/your_new_file.dax -v
   ```

5. **Fix any errors or warnings** reported

6. **Commit and push** - CI will automatically validate

## Validation Rules

### Error Level (Must Fix)
- Unbalanced parentheses/brackets/braces
- Non-existent DAX functions
- Invalid syntax

### Warning Level (Should Fix)
- Use of division operator instead of DIVIDE()
- Nested CALCULATE functions
- Potential unterminated strings
- Comparison with BLANK() directly

### Info Level (Good to Know)
- Number of measures found
- Suggestion for VALUES() vs DISTINCT()

## Manual Testing

While automated validation checks syntax, you should also:

### 1. Test in Power BI Desktop
- Copy measures to a Power BI model
- Verify they return expected results
- Check performance with DAX Studio

### 2. Test with Sample Data
- Use appropriate data types
- Test edge cases (nulls, zeros, empty tables)
- Verify filter context behavior

### 3. Performance Testing
Use DAX Studio to:
- Measure query execution time
- Analyze query plan
- Check storage engine vs formula engine usage
- Optimize if needed

## Contributing Tests

To improve the validator:

1. **Add new validation rules** in `tests/validate_dax.py`:
   ```python
   def _check_new_rule(self, content: str, filepath: Path):
       """Check for new pattern"""
       # Implementation
   ```

2. **Add to validation pipeline**:
   ```python
   def validate_file(self, filepath: Path) -> bool:
       # ... existing checks ...
       self._check_new_rule(content, filepath)
   ```

3. **Test your changes**:
   ```bash
   python3 tests/validate_dax.py dax_patterns/ -v
   ```

4. **Submit pull request**

## Troubleshooting

### Validator Not Running
```bash
# Make script executable
chmod +x tests/validate_dax.py

# Or run with python explicitly
python3 tests/validate_dax.py dax_patterns/
```

### False Positives
If validator reports an error that isn't actually a problem:
- Check if it's a warning (can be ignored)
- Report issue with example DAX code
- We'll update validation rules

### Python Not Found
```bash
# Install Python 3
# Ubuntu/Debian
sudo apt-get install python3

# macOS
brew install python3

# Windows
# Download from python.org
```

## Examples

### Good Validation Result
```
✅ All checks passed!

ℹ️  INFO:
  dax_patterns/time_intelligence.dax - Found 21 measure definitions
```

### With Warnings
```
⚠️  WARNINGS:
  dax_patterns/example.dax:45 - Consider using DIVIDE() instead of / operator for safety

ℹ️  INFO:
  dax_patterns/example.dax - Found 15 measure definitions
```

### With Errors
```
❌ ERRORS:
  dax_patterns/example.dax - Unbalanced parentheses (difference: 2)
  dax_patterns/example.dax:30 - SUMIF doesn't exist in DAX

⚠️  WARNINGS:
  dax_patterns/example.dax:45 - Consider using DIVIDE() instead of / operator
```

## Resources

- [DAX Guide](https://dax.guide/) - Official DAX function reference
- [DAX Studio](https://daxstudio.org/) - Free tool for DAX development and testing
- [SQLBI](https://www.sqlbi.com/) - Advanced DAX patterns and optimization
- [Power BI Documentation](https://docs.microsoft.com/power-bi/) - Official Microsoft docs
