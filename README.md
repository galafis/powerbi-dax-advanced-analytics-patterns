# Power BI Advanced Analytics with DAX

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black) ![DAX](https://img.shields.io/badge/DAX-2E8B57?style=for-the-badge) ![M Language](https://img.shields.io/badge/M_Language-0078D4?style=for-the-badge)

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

Este repositório contém **9 categorias** de padrões DAX:

1. **Time Intelligence** (15 medidas)
2. **Comparações Período-a-Período** (8 medidas)
3. **Moving Averages & Running Totals** (6 medidas)
4. **Ranking & Top N** (5 medidas)
5. **Análise de Cohort** (4 medidas)
6. **Cálculos Estatísticos** (7 medidas)
7. **What-If Analysis** (3 medidas)
8. **Análise de Pareto** (3 medidas)
9. **KPIs Dinâmicos** (5 medidas)

**Total: 56 medidas DAX prontas para uso!**

### 📂 Estrutura do Repositório

```
powerbi-dax-advanced-analytics-patterns/
├── dax_patterns/
│   ├── time_intelligence.dax          # 15 medidas de time intelligence
│   ├── period_comparisons.dax         # Comparações YoY, MoM, etc.
│   ├── moving_averages.dax            # Médias móveis e running totals
│   ├── ranking.dax                    # Top N, ranking dinâmico
│   ├── cohort_analysis.dax            # Análise de retenção
│   ├── statistical.dax                # Medidas estatísticas
│   ├── what_if.dax                    # Análise de cenários
│   ├── pareto.dax                     # Análise 80/20
│   └── dynamic_kpis.dax               # KPIs com targets dinâmicos
├── pbix_files/
│   └── dax_patterns_demo.pbix         # Dashboard com todos os exemplos
├── data_model/
│   ├── star_schema_diagram.png        # Diagrama do modelo dimensional
│   └── best_practices.md              # Melhores práticas de modelagem
├── examples/
│   ├── sales_analysis.md              # Exemplo: Análise de vendas
│   ├── customer_retention.md          # Exemplo: Retenção de clientes
│   └── inventory_optimization.md      # Exemplo: Otimização de estoque
└── README.md
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

### 🎯 Próximos Passos

- [ ] Adicionar exemplos de Power Query M
- [ ] Criar templates de dashboards
- [ ] Adicionar padrões de modelagem dimensional
- [ ] Implementar testes automatizados de DAX
- [ ] Criar vídeos tutoriais

### 🔗 Recursos Adicionais

- [DAX Guide](https://dax.guide/)
- [SQLBI - DAX Patterns](https://www.daxpatterns.com/)
- [DAX Studio](https://daxstudio.org/)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)

---

## 🇬🇧 Power BI Advanced Analytics with DAX

This repository is a **complete and professional collection** of advanced patterns and techniques for performing complex analysis in Power BI using **DAX (Data Analysis Expressions)**. Contains over **50 ready-to-use DAX measures** covering from time intelligence to advanced statistical calculations.

### 🚀 Quick Start

1. Open Power BI Desktop
2. Copy DAX measures from `dax_patterns/` folder
3. Paste into your model
4. Adapt table/column names
5. Test and validate

### 🎓 Key Learnings

- ✅ Master time intelligence functions
- ✅ Implement complex business logic
- ✅ Optimize DAX for performance
- ✅ Build enterprise-grade dashboards
- ✅ Apply statistical analysis
- ✅ Create dynamic KPIs

---

**Author:** Gabriel Demetrios Lafis  
**License:** MIT  
**Last Updated:** October 2025
