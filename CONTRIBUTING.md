# Contributing to Power BI DAX Advanced Analytics Patterns

First off, thank you for considering contributing to this repository! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, include:
- A clear and descriptive title
- Detailed steps to reproduce the issue
- Expected vs actual behavior
- DAX code snippet that demonstrates the issue
- Power BI Desktop version you're using

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:
- A clear and descriptive title
- Detailed description of the proposed functionality
- Examples of how the enhancement would be used
- Why this enhancement would be useful

### 📝 Contributing DAX Patterns

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/new-dax-pattern`)
3. **Add your DAX pattern** following the existing structure:
   ```dax
   // ================================================
   // [PATTERN CATEGORY NAME]
   // Author: Your Name
   // Description: Brief description
   // ================================================
   
   // ------------------------------------------------
   // 1. [SUBCATEGORY NAME]
   // ------------------------------------------------
   
   // Pattern Name
   Pattern Measure = 
   VAR Variable1 = CALCULATE(...)
   RETURN
       Variable1
   ```
4. **Test your DAX formulas** in Power BI Desktop
5. **Document your patterns** with clear comments
6. **Commit your changes** with descriptive commit messages
7. **Push to your fork**
8. **Open a Pull Request**

### ✅ DAX Code Quality Guidelines

1. **Use Variables**: Always use VAR for complex calculations
2. **Comment Your Code**: Add clear comments explaining logic
3. **Name Conventions**: Use descriptive names (e.g., `Sales YTD` not `Measure1`)
4. **Performance**: Consider query performance and optimization
5. **Error Handling**: Use DIVIDE() instead of division operator
6. **Formatting**: Follow consistent indentation and spacing
7. **Context Awareness**: Be explicit about filter context

### 📋 Pull Request Process

1. Update the README.md if you're adding new patterns or categories
2. Ensure your DAX code follows the style guidelines
3. Add examples and use cases for your patterns
4. The PR will be merged once it receives approval from maintainers

### 🎯 Good First Issues

Look for issues tagged with `good first issue` or `help wanted` if you're new to the project.

### 💬 Questions?

Feel free to open an issue with the `question` label if you have any questions about contributing.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and considerate in all interactions.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Recognition

Contributors will be recognized in the repository's README and release notes.

Thank you for your contributions! 🚀
