#!/usr/bin/env python3
"""
DAX Syntax Validator
Validates DAX formula files for common syntax errors and best practices
"""

import argparse
import json
import re
import sys
from pathlib import Path


class DAXValidator:
    """Validates DAX formulas for syntax errors and best practices"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
        # DAX keywords and functions (common ones)
        self.keywords = {
            'VAR', 'RETURN', 'IF', 'SWITCH', 'TRUE', 'FALSE',
            'CALCULATE', 'CALCULATETABLE', 'FILTER', 'ALL', 'ALLEXCEPT', 'ALLSELECTED',
            'SUM', 'AVERAGE', 'COUNT', 'DISTINCTCOUNT', 'MIN', 'MAX',
            'SUMX', 'AVERAGEX', 'COUNTX', 'MAXX', 'MINX',
            'DATESYTD', 'DATESMTD', 'DATESQTD', 'TOTALYTD', 'TOTALMTD', 'TOTALQTD',
            'SAMEPERIODLASTYEAR', 'DATEADD', 'DATESINPERIOD', 'DATESBETWEEN',
            'DIVIDE', 'FORMAT', 'CONCATENATE', 'BLANK', 'ISBLANK',
            'HASONEVALUE', 'SELECTEDVALUE', 'VALUES', 'DISTINCT',
            'RANKX', 'TOPN', 'PERCENTILEX', 'MEDIAN',
            'AND', 'OR', 'NOT', 'IN',
            'EARLIER', 'EARLIEST', 'RELATED', 'RELATEDTABLE',
            'SUMMARIZE', 'SUMMARIZECOLUMNS', 'ADDCOLUMNS', 'SELECTCOLUMNS',
            'CROSSJOIN', 'UNION', 'INTERSECT', 'EXCEPT',
            'USERELATIONSHIP', 'TREATAS', 'CROSSFILTER',
        }
    
    def validate_file(self, filepath: Path) -> bool:
        """Validate a single DAX file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.errors = []
            self.warnings = []
            self.info = []
            
            # Run validation checks
            self._check_basic_syntax(content, filepath)
            self._check_balanced_parentheses(content, filepath)
            self._check_measure_definitions(content, filepath)
            self._check_best_practices(content, filepath)
            self._check_common_mistakes(content, filepath)
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.errors.append(f"Error reading file {filepath}: {str(e)}")
            return False
    
    def _check_basic_syntax(self, content: str, filepath: Path):
        """Check basic DAX syntax"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Skip comments and empty lines
            if not line_stripped or line_stripped.startswith('//'):
                continue
            
            # Check for unterminated strings
            if line_stripped.count('"') % 2 != 0 and not line_stripped.startswith('//'):
                # Could be continued on next line, so just warn
                self.warnings.append(f"{filepath}:{i} - Possible unterminated string")
    
    def _check_balanced_parentheses(self, content: str, filepath: Path):
        """Check if parentheses, brackets, and braces are balanced"""
        # Remove comments
        content_no_comments = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        # Remove strings
        content_no_strings = re.sub(r'"[^"]*"', '', content_no_comments)
        
        # Check parentheses
        paren_count = content_no_strings.count('(') - content_no_strings.count(')')
        bracket_count = content_no_strings.count('[') - content_no_strings.count(']')
        brace_count = content_no_strings.count('{') - content_no_strings.count('}')
        
        if paren_count != 0:
            self.errors.append(f"{filepath} - Unbalanced parentheses (difference: {paren_count})")
        if bracket_count != 0:
            self.errors.append(f"{filepath} - Unbalanced brackets (difference: {bracket_count})")
        if brace_count != 0:
            self.errors.append(f"{filepath} - Unbalanced braces (difference: {brace_count})")
    
    def _check_measure_definitions(self, content: str, filepath: Path):
        """Check measure definitions"""
        # Pattern for measure definition: MeasureName = ...
        # Must NOT match VAR lines (VAR Name = ...) or lines inside expressions
        measure_pattern = r'^([A-Za-z0-9_][A-Za-z0-9_ %-]*)\s*=\s*$'
        
        lines = content.split('\n')
        measure_count = 0
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Skip comments
            if line_stripped.startswith('//') or line_stripped.startswith('--'):
                continue
            
            # Skip VAR assignments (VAR Name = ...)
            if line_stripped.upper().startswith('VAR '):
                continue
            
            # Check for measure definition
            if re.match(measure_pattern, line_stripped):
                measure_count += 1
                
                # Check if next non-empty line exists (measure should have a body)
                has_body = False
                for j in range(i, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('//'):
                        has_body = True
                        break
                
                if not has_body:
                    self.warnings.append(f"{filepath}:{i} - Measure '{line_stripped.split('=')[0].strip()}' appears to have no body")
        
        self.info.append(f"{filepath} - Found {measure_count} measure definitions")
    
    def _check_best_practices(self, content: str, filepath: Path):
        """Check DAX best practices"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            line_upper = line_stripped.upper()
            
            # Skip comments
            if line_stripped.startswith('//') or line_stripped.startswith('--'):
                continue
            
            # Check for division operator (should use DIVIDE)
            if '/' in line_stripped and 'DIVIDE' not in line_upper and 'FORMAT' not in line_upper:
                # Check if it's actually division, not part of a comment or date
                if re.search(r'[\]\)0-9]\s*/\s*[A-Za-z\[\(0-9]', line_stripped):
                    self.warnings.append(f"{filepath}:{i} - Consider using DIVIDE() instead of / operator for safety")
            
            # Check for using VALUES() in CALCULATE (might want DISTINCT)
            if 'CALCULATE' in line_upper and 'VALUES(' in line_upper:
                self.info.append(f"{filepath}:{i} - Consider if DISTINCT() might be more appropriate than VALUES()")
            
            # Check for nested CALCULATE (often inefficient)
            if line_upper.count('CALCULATE') > 1:
                self.warnings.append(f"{filepath}:{i} - Multiple CALCULATE functions detected - consider refactoring")
    
    def _check_common_mistakes(self, content: str, filepath: Path):
        """Check for common DAX mistakes"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_upper = line.strip().upper()
            
            # Skip comments
            if line.strip().startswith('//') or line.strip().startswith('--'):
                continue
            
            # Check for common function name mistakes
            if 'SUMIF' in line_upper:
                self.errors.append(f"{filepath}:{i} - SUMIF doesn't exist in DAX. Use CALCULATE(SUM(...), filter) or SUMX")
            
            if 'COUNTIF' in line_upper:
                self.errors.append(f"{filepath}:{i} - COUNTIF doesn't exist in DAX. Use CALCULATE(COUNT(...), filter) or COUNTX")
            
            if 'AVERAGEIF' in line_upper:
                self.errors.append(f"{filepath}:{i} - AVERAGEIF doesn't exist in DAX. Use CALCULATE(AVERAGE(...), filter) or AVERAGEX")
            
            # Check for comparison with BLANK() - should use ISBLANK()
            if re.search(r'=\s*BLANK\(\)', line_upper) or re.search(r'<>\s*BLANK\(\)', line_upper):
                self.warnings.append(f"{filepath}:{i} - Comparing with BLANK() directly. Consider using ISBLANK()")
    
    def print_results(self, verbose: bool = False):
        """Print validation results"""
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if verbose and self.info:
            print("\nℹ️  INFO:")
            for info in self.info:
                print(f"  {info}")
        
        if not self.errors and not self.warnings:
            print("✅ All checks passed!")
    
    def get_summary(self) -> dict:
        """Get validation summary"""
        return {
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'info': len(self.info),
            'passed': len(self.errors) == 0
        }


def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description='Validate DAX formula files')
    parser.add_argument('paths', nargs='+', help='Paths to DAX files or directories')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    args = parser.parse_args()
    
    validator = DAXValidator()
    all_files = []
    
    # Collect all DAX files
    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file() and path.suffix == '.dax':
            all_files.append(path)
        elif path.is_dir():
            all_files.extend(path.rglob('*.dax'))
    
    if not all_files:
        print("No DAX files found to validate")
        return 1
    
    print(f"Validating {len(all_files)} DAX file(s)...\n")
    
    results = []
    total_errors = 0
    total_warnings = 0
    
    for dax_file in sorted(all_files):
        print(f"Checking: {dax_file}")
        is_valid = validator.validate_file(dax_file)
        
        if not args.json:
            validator.print_results(args.verbose)
            print()
        
        summary = validator.get_summary()
        results.append({
            'file': str(dax_file),
            'summary': summary,
            'errors': validator.errors.copy(),
            'warnings': validator.warnings.copy()
        })
        
        total_errors += summary['errors']
        total_warnings += summary['warnings']
    
    # Print summary
    print("=" * 60)
    print(f"VALIDATION COMPLETE")
    print(f"Files checked: {len(all_files)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    
    if args.json:
        print("\n" + json.dumps(results, indent=2))
    
    # Return exit code
    return 0 if total_errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
