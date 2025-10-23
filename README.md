# Power BI Advanced Analytics with DAX

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black) ![DAX](https://img.shields.io/badge/DAX-2E8B57?style=for-the-badge) ![M Language](https://img.shields.io/badge/M_Language-0078D4?style=for-the-badge)

[![DAX Validation](https://github.com/galafis/powerbi-dax-advanced-analytics-patterns/actions/workflows/dax-validation.yml/badge.svg)](https://github.com/galafis/powerbi-dax-advanced-analytics-patterns/actions/workflows/dax-validation.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🇧🇷 Padrões Avançados de DAX para Power BI

Este repositório é uma **coleção completa e profissional** de padrões e técnicas avançadas para realizar análises complexas no Power BI utilizando **DAX (Data Analysis Expressions)**. Contém mais de **50 medidas DAX** prontas para uso, cobrindo desde time intelligence até cálculos estatísticos avançados.

### 🎯 Objetivo

Fornecer um guia prático e funcional com exemplos de código DAX para resolver problemas reais de negócio, permitindo que analistas e desenvolvedores de BI criem dashboards de nível empresarial com performance otimizada.

### 🌟 Por que DAX Avançado?

DAX é a linguagem de fórmulas do Power BI, mas dominar seus conceitos avançados separa analistas básicos de especialistas:

| Nível | Conhecimento | Impacto |
|-------|--------------|---------|
| **Básico** | SUM, AVERAGE, COUNT | Dashboards simples |
| **Intermediário** | CALCULATE, FILTER | Análises com contexto |
| **Avançado** | Time Intelligence, Variables | Análises complexas |
| **Expert** | Context Transition, Iterators | Performance otimizada |

### 📊 Padrões DAX Incluídos

Este repositório contém **9 categorias** de padrões DAX com **mais de 290 medidas prontas**:

1. **Time Intelligence** (21 medidas) - YTD, MTD, QTD, YoY, MoM, SPLY
2. **Comparações Período-a-Período** (25 medidas) - YoY, MoM, QoQ, DoD, WoW
3. **Moving Averages & Running Totals** (21 medidas) - SMA, EMA, WMA, cumulative sums
4. **Ranking & Top N** (31 medidas) - Rankings, Top N, percentages, tiers
5. **Análise de Cohort** (42 medidas) - Retention, LTV, churn, behavior metrics
6. **Cálculos Estatísticos** (41 medidas) - Mean, median, std dev, percentiles, correlation
7. **What-If Analysis** (31 medidas) - Scenarios, sensitivity, forecasts, optimization
8. **Análise de Pareto** (37 medidas) - ABC classification, 80/20, Gini coefficient
9. **KPIs Dinâmicos** (42 medidas) - Performance scores, trends, alerts, balanced scorecard

**Total: 291 medidas DAX prontas para uso!** ✅ Todas validadas automaticamente

### 📂 Estrutura do Repositório

```
powerbi-dax-advanced-analytics-patterns/
├── dax_patterns/                        # 📊 DAX Formula Library
│   ├── time_intelligence.dax            # 21 time-based measures
│   ├── period_comparisons.dax           # 25 period comparison measures
│   ├── moving_averages.dax              # 21 moving averages & running totals
│   ├── ranking.dax                      # 31 ranking & Top N measures
│   ├── cohort_analysis.dax              # 42 cohort & retention measures
│   ├── statistical.dax                  # 41 statistical measures
│   ├── what_if.dax                      # 31 scenario analysis measures
│   ├── pareto.dax                       # 37 Pareto & ABC classification measures
│   └── dynamic_kpis.dax                 # 42 KPI & performance measures
├── examples/                            # 📚 Real-World Use Cases
│   ├── sales_analysis.md                # Sales performance analysis
│   ├── customer_retention.md            # Cohort & retention analysis
│   └── inventory_optimization.md        # Inventory management
├── data_model/                          # 🗂️ Data Modeling Guide
│   └── best_practices.md                # Star schema, optimization, patterns
├── tests/                               # ✅ Validation & Testing
│   ├── validate_dax.py                  # DAX syntax validator
│   └── README.md                        # Testing documentation
├── .github/workflows/                   # 🔄 CI/CD Pipeline
│   └── dax-validation.yml               # Automated DAX validation
├── images/                              # 🖼️ Visual Assets
├── INSTALL.md                           # Installation guide
├── CONTRIBUTING.md                      # Contribution guidelines
├── LICENSE                              # MIT License
└── README.md                            # This file
```

### 🚀 Como Usar

#### 1. Copiar Medidas DAX

Todas as medidas estão em arquivos `.dax` prontos para copiar e colar no Power BI:

```dax
// Exemplo: Year-to-Date Sales
YTD Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESYTD('Calendar'[Date])
)
```

#### 2. Adaptar para Seu Modelo

Substitua os nomes de tabelas e colunas:

```dax
// Original
SUM(Sales[Amount])

// Adaptado para seu modelo
SUM(MinhaTabela[MinhaColuna])
```

#### 3. Testar Performance

Use o **DAX Studio** para analisar performance:

```bash
# Instalar DAX Studio
# Download: https://daxstudio.org/
```

### 💻 Exemplos de Código DAX

#### 1. Time Intelligence Completo

```dax
// ============================================
// TIME INTELLIGENCE MEASURES
// ============================================

// Year-to-Date (YTD)
YTD Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESYTD('Calendar'[Date])
)

// Quarter-to-Date (QTD)
QTD Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESQTD('Calendar'[Date])
)

// Month-to-Date (MTD)
MTD Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESMTD('Calendar'[Date])
)

// Previous Year (PY)
PY Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR('Calendar'[Date])
)

// Year-over-Year Growth (YoY)
YoY Growth = 
VAR CurrentYear = SUM(Sales[Amount])
VAR PreviousYear = [PY Sales]
RETURN
    DIVIDE(
        CurrentYear - PreviousYear,
        PreviousYear,
        0
    )

// Year-over-Year Growth %
YoY Growth % = 
FORMAT([YoY Growth], "0.00%")

// Month-over-Month Growth (MoM)
MoM Growth = 
VAR CurrentMonth = SUM(Sales[Amount])
VAR PreviousMonth = 
    CALCULATE(
        SUM(Sales[Amount]),
        DATEADD('Calendar'[Date], -1, MONTH)
    )
RETURN
    DIVIDE(
        CurrentMonth - PreviousMonth,
        PreviousMonth,
        0
    )

// Rolling 12 Months
Rolling 12M Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESINPERIOD(
        'Calendar'[Date],
        LASTDATE('Calendar'[Date]),
        -12,
        MONTH
    )
)

// Same Period Last Year (SPLY)
SPLY Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR('Calendar'[Date])
)

// Fiscal Year-to-Date (Fiscal year starts in July)
FYTD Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESYTD('Calendar'[Date], "06-30")
)
```

#### 2. Moving Averages & Running Totals

```dax
// ============================================
// MOVING AVERAGES & RUNNING TOTALS
// ============================================

// 3-Month Moving Average
3M Moving Avg = 
AVERAGEX(
    DATESINPERIOD(
        'Calendar'[Date],
        LASTDATE('Calendar'[Date]),
        -3,
        MONTH
    ),
    [Total Sales]
)

// 7-Day Moving Average
7D Moving Avg = 
AVERAGEX(
    DATESINPERIOD(
        'Calendar'[Date],
        LASTDATE('Calendar'[Date]),
        -7,
        DAY
    ),
    [Total Sales]
)

// Running Total (Cumulative Sum)
Running Total = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL('Calendar'[Date]),
        'Calendar'[Date] <= MAX('Calendar'[Date])
    )
)

// Running Total by Category
Running Total by Category = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALLEXCEPT('Calendar', 'Calendar'[Date]),
        'Calendar'[Date] <= MAX('Calendar'[Date])
    )
)

// Weighted Moving Average
Weighted Moving Avg = 
VAR Period1 = CALCULATE([Total Sales], DATEADD('Calendar'[Date], -1, MONTH))
VAR Period2 = CALCULATE([Total Sales], DATEADD('Calendar'[Date], -2, MONTH))
VAR Period3 = CALCULATE([Total Sales], DATEADD('Calendar'[Date], -3, MONTH))
RETURN
    (Period1 * 0.5 + Period2 * 0.3 + Period3 * 0.2)
```

#### 3. Ranking & Top N

```dax
// ============================================
// RANKING & TOP N
// ============================================

// Product Rank by Sales
Product Rank = 
RANKX(
    ALL(Products[ProductName]),
    [Total Sales],
    ,
    DESC,
    DENSE
)

// Top 10 Products Filter
Top 10 Products = 
IF(
    [Product Rank] <= 10,
    [Total Sales],
    BLANK()
)

// Dynamic Top N (with parameter)
Top N Sales = 
VAR TopNValue = SELECTEDVALUE('Top N Parameter'[Value], 10)
VAR CurrentRank = [Product Rank]
RETURN
    IF(
        CurrentRank <= TopNValue,
        [Total Sales],
        BLANK()
    )

// Percentage of Total
% of Total = 
DIVIDE(
    [Total Sales],
    CALCULATE(
        [Total Sales],
        ALL(Products)
    )
)

// Cumulative % (for Pareto)
Cumulative % = 
VAR CurrentProduct = MAX(Products[ProductName])
VAR ProductsUpToCurrent = 
    FILTER(
        ALL(Products[ProductName]),
        [Product Rank] <= 
        CALCULATE([Product Rank], Products[ProductName] = CurrentProduct)
    )
RETURN
    CALCULATE(
        [% of Total],
        ProductsUpToCurrent
    )
```

#### 4. Statistical Measures

```dax
// ============================================
// STATISTICAL MEASURES
// ============================================

// Standard Deviation
Sales Std Dev = 
STDEV.P(Sales[Amount])

// Variance
Sales Variance = 
VAR.P(Sales[Amount])

// Coefficient of Variation (CV)
Sales CV = 
DIVIDE(
    [Sales Std Dev],
    [Average Sales],
    0
)

// Z-Score
Sales Z-Score = 
VAR CurrentSales = SUM(Sales[Amount])
VAR AvgSales = [Average Sales]
VAR StdDev = [Sales Std Dev]
RETURN
    DIVIDE(
        CurrentSales - AvgSales,
        StdDev,
        0
    )

// Median
Sales Median = 
MEDIAN(Sales[Amount])

// Percentile 90
Sales P90 = 
PERCENTILEX.INC(Sales, Sales[Amount], 0.90)

// Interquartile Range (IQR)
Sales IQR = 
VAR Q1 = PERCENTILEX.INC(Sales, Sales[Amount], 0.25)
VAR Q3 = PERCENTILEX.INC(Sales, Sales[Amount], 0.75)
RETURN
    Q3 - Q1
```

### 📊 Casos de Uso Reais

#### Caso 1: Dashboard de Vendas Executivo

**Desafio**: CEO precisa ver vendas YTD, comparação com ano anterior e forecast.

**Solução DAX**:
```dax
// KPI Card: YTD Sales vs Target
YTD vs Target = 
VAR YTDActual = [YTD Sales]
VAR YTDTarget = [YTD Target]
VAR Variance = YTDActual - YTDTarget
VAR VariancePct = DIVIDE(Variance, YTDTarget, 0)
RETURN
    "YTD: " & FORMAT(YTDActual, "$#,##0") & 
    " | Target: " & FORMAT(YTDTarget, "$#,##0") & 
    " | Variance: " & FORMAT(VariancePct, "+0.0%;-0.0%")
```

#### Caso 2: Análise de Retenção de Clientes

**Desafio**: Medir retenção de clientes mês a mês.

**Solução DAX**:
```dax
// Customer Retention Rate
Retention Rate = 
VAR CustomersLastMonth = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        DATEADD('Calendar'[Date], -1, MONTH)
    )
VAR CustomersThisMonth = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        FILTER(
            ALL('Calendar'),
            'Calendar'[Date] = MAX('Calendar'[Date])
        )
    )
VAR RetainedCustomers = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        FILTER(
            Sales,
            Sales[CustomerID] IN 
                CALCULATETABLE(
                    VALUES(Sales[CustomerID]),
                    DATEADD('Calendar'[Date], -1, MONTH)
                )
        )
    )
RETURN
    DIVIDE(RetainedCustomers, CustomersLastMonth, 0)
```

### 🎓 Conceitos Avançados

#### Context Transition

```dax
// Sem context transition (ERRADO)
Sales per Customer = 
SUMX(
    Customers,
    SUM(Sales[Amount])  // Retorna total geral!
)

// Com context transition (CORRETO)
Sales per Customer = 
SUMX(
    Customers,
    CALCULATE(SUM(Sales[Amount]))  // Filtra por cada cliente
)
```

#### Variables para Performance

```dax
// Sem variáveis (calcula 3 vezes)
Bad Measure = 
IF(
    SUM(Sales[Amount]) > 1000,
    SUM(Sales[Amount]) * 0.9,
    SUM(Sales[Amount])
)

// Com variáveis (calcula 1 vez)
Good Measure = 
VAR TotalSales = SUM(Sales[Amount])
RETURN
    IF(
        TotalSales > 1000,
        TotalSales * 0.9,
        TotalSales
    )
```

### 🔧 Melhores Práticas

1. **Use variáveis** para melhorar legibilidade e performance
2. **Evite iteradores** quando possível (SUMX, FILTER)
3. **Prefira medidas** ao invés de colunas calculadas
4. **Otimize relacionamentos** (1:N, não N:N)
5. **Use tabelas de calendário** para time intelligence
6. **Documente medidas complexas** com comentários
7. **Teste performance** com DAX Studio

### 📈 Performance Tips

| Técnica | Impacto | Exemplo |
|---------|---------|---------|
| **Variables** | Alto | `VAR x = SUM(...) RETURN x * 2` |
| **CALCULATE vs FILTER** | Alto | Prefira CALCULATE quando possível |
| **Evitar N:N** | Muito Alto | Use tabela bridge |
| **Medidas vs Colunas** | Médio | Medidas são calculadas on-demand |
| **Minimizar Iteradores** | Alto | Use agregações nativas |

### 🧪 Testar com DAX Studio

```sql
-- Query para testar performance
EVALUATE
SUMMARIZECOLUMNS(
    'Calendar'[Year],
    'Calendar'[Month],
    "Total Sales", [Total Sales],
    "YoY Growth", [YoY Growth],
    "3M Moving Avg", [3M Moving Avg]
)
ORDER BY 'Calendar'[Year], 'Calendar'[Month]
```

### ✅ Validação Automatizada

Este repositório inclui **validação automatizada de DAX** para garantir qualidade:

#### Executar Validação Local
```bash
# Validar todos os arquivos DAX
python3 tests/validate_dax.py dax_patterns/

# Validar arquivo específico
python3 tests/validate_dax.py dax_patterns/time_intelligence.dax -v
```

#### O que é Validado?
- ✅ Sintaxe básica de DAX
- ✅ Parênteses, colchetes e chaves balanceados
- ✅ Estrutura de definição de medidas
- ⚠️ Uso de melhores práticas (DIVIDE, etc.)
- ❌ Funções inexistentes (SUMIF, COUNTIF)
- ❌ Erros comuns de sintaxe

#### CI/CD com GitHub Actions
Toda alteração em arquivos DAX é automaticamente validada via GitHub Actions.

Badge de Status: [![DAX Validation](https://github.com/galafis/powerbi-dax-advanced-analytics-patterns/actions/workflows/dax-validation.yml/badge.svg)](https://github.com/galafis/powerbi-dax-advanced-analytics-patterns/actions/workflows/dax-validation.yml)

### 🎯 Próximos Passos

- [x] ~~Adicionar padrões de modelagem dimensional~~
- [x] ~~Implementar testes automatizados de DAX~~
- [ ] Adicionar exemplos de Power Query M
- [ ] Criar templates de dashboards (.pbix)
- [ ] Criar vídeos tutoriais
- [ ] Adicionar diagramas visuais de arquitetura

### 🔗 Recursos Adicionais

- [DAX Guide](https://dax.guide/) - Referência completa de funções DAX
- [SQLBI - DAX Patterns](https://www.daxpatterns.com/) - Padrões avançados
- [DAX Studio](https://daxstudio.org/) - Ferramenta gratuita para desenvolvimento DAX
- [Power BI Documentation](https://docs.microsoft.com/power-bi/) - Documentação oficial Microsoft
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 🆘 Guia de Solução de Problemas

### 🤝 Como Contribuir

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre:
- Como reportar bugs
- Como sugerir melhorias
- Como adicionar novos padrões DAX
- Diretrizes de código e estilo
- Processo de Pull Request

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🇬🇧 Power BI Advanced Analytics with DAX

This repository is a **complete and professional collection** of advanced patterns and techniques for performing complex analysis in Power BI using **DAX (Data Analysis Expressions)**. Contains over **290 ready-to-use DAX measures** covering from time intelligence to advanced statistical calculations.

### 🚀 Quick Start

1. Open Power BI Desktop
2. Copy DAX measures from `dax_patterns/` folder
3. Paste into your model
4. Adapt table/column names
5. Test and validate

### 🎓 What You'll Learn

- ✅ Master time intelligence functions (YTD, YoY, MoM)
- ✅ Implement complex business logic with variables
- ✅ Optimize DAX for performance
- ✅ Build enterprise-grade dashboards
- ✅ Apply statistical analysis (correlation, regression, percentiles)
- ✅ Create dynamic KPIs with conditional formatting
- ✅ Perform cohort analysis and customer retention tracking
- ✅ Implement What-If scenarios and forecasting

### 📚 Real-World Examples

Explore complete use cases with step-by-step DAX implementation:

- **[Sales Analysis](examples/sales_analysis.md)** - Revenue performance, Pareto analysis, regional trends
- **[Customer Retention](examples/customer_retention.md)** - Cohort tracking, LTV calculation, churn prediction
- **[Inventory Optimization](examples/inventory_optimization.md)** - ABC classification, reorder points, stockout prevention

### 🎯 Repository Features

- ✅ **291 Production-Ready DAX Measures** across 9 categories
- ✅ **Automated Validation** - All formulas syntax-checked via CI/CD
- ✅ **Comprehensive Documentation** - Every pattern explained with examples
- ✅ **Real-World Use Cases** - Practical business scenarios
- ✅ **Data Modeling Best Practices** - Star schema, optimization tips
- ✅ **MIT Licensed** - Free to use in your projects

### 🔧 Quality Assurance

Every DAX formula is automatically validated for:
- Syntax correctness
- Balanced parentheses/brackets
- Best practices adherence
- Common mistake prevention

Run validation locally:
```bash
python3 tests/validate_dax.py dax_patterns/ -v
```
- ✅ Create dynamic KPIs

### 🌟 Support This Project

If you find this repository helpful, please:
- ⭐ Star this repository
- 🔀 Fork and contribute
- 🐛 Report issues
- 💡 Suggest new patterns
- 📣 Share with your network

### 👨‍💻 Author & Maintainer

**Gabriel Demetrios Lafis**

### 📬 Connect

- 💼 [GitHub Profile](https://github.com/galafis)
- 🔗 [LinkedIn](https://linkedin.com)
- 📧 Questions? Open an issue or discussion

---

**Last Updated:** October 2025  
**License:** MIT  
**Status:** ✅ Active Development
