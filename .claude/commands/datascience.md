---
argument-hint: [analyze|visualize|model|dashboard|report] [dataset|target]
description: Comprehensive data science workflows including analysis, visualization, ML modeling, and reporting
allowed-tools: mcp__ide__executeCode, Read, Write, Edit, Bash, TodoWrite, Grep, Glob
---

# 📊 Data Science Workbench

**Operation**: $ARGUMENTS

Comprehensive data science workflows using the data-scientist agent for analysis, visualization, machine learning, and reporting.

## Available Data Science Operations:

### Data Analysis
- `/datascience analyze sales.csv` - Complete exploratory data analysis
- `/datascience analyze user_behavior` - Behavioral data analysis
- `/datascience analyze timeseries` - Time series analysis and forecasting
- `/datascience analyze correlations` - Correlation and relationship analysis
- Automated EDA with statistical summaries, missing value analysis, and data quality assessment

### Data Visualization
- `/datascience visualize distributions` - Distribution plots and histograms
- `/datascience visualize correlations` - Correlation heatmaps and pair plots
- `/datascience visualize timeseries` - Time series plots with trends and seasonality
- `/datascience visualize comparisons` - Box plots, violin plots, comparison charts
- Interactive visualizations using Plotly, Seaborn, and Matplotlib

### Machine Learning Modeling
- `/datascience model classification` - Classification model development
- `/datascience model regression` - Regression analysis and prediction
- `/datascience model clustering` - Unsupervised clustering analysis
- `/datascience model forecasting` - Time series forecasting models
- Full ML pipeline: preprocessing, feature engineering, model selection, validation

### Interactive Dashboards
- `/datascience dashboard sales` - Sales analytics dashboard
- `/datascience dashboard user_metrics` - User behavior dashboard
- `/datascience dashboard financial` - Financial KPI dashboard
- `/datascience dashboard custom` - Custom interactive dashboard
- Built with Dash, Streamlit, or Jupyter widgets for real-time exploration

### Reporting & Documentation
- `/datascience report analysis` - Comprehensive analysis report
- `/datascience report model` - Model performance and evaluation report
- `/datascience report executive` - Executive summary with key insights
- `/datascience report technical` - Technical methodology documentation
- Publication-ready reports with visualizations and statistical findings

## Data Science Workflow:

### 1. Data Discovery & Assessment
- **Data Profiling**: Shape, types, missing values, basic statistics
- **Quality Evaluation**: Completeness, accuracy, consistency checks
- **Business Context**: Understanding the analytical objectives
- **Success Metrics**: Defining measurable outcomes

### 2. Exploratory Data Analysis (EDA)
- **Univariate Analysis**: Distribution of individual variables
- **Bivariate Analysis**: Relationships between variable pairs
- **Multivariate Analysis**: Complex interactions and patterns
- **Anomaly Detection**: Outliers and unusual data points

### 3. Feature Engineering & Preprocessing
- **Data Cleaning**: Handle missing values, outliers, duplicates
- **Feature Creation**: Derived variables, transformations, binning
- **Encoding**: Categorical variables, scaling numerical features
- **Feature Selection**: Identify most relevant predictors

### 4. Statistical Analysis & Modeling
- **Descriptive Statistics**: Central tendency, dispersion, shape
- **Inferential Statistics**: Hypothesis testing, confidence intervals
- **Predictive Modeling**: Classification, regression, clustering
- **Model Validation**: Cross-validation, performance metrics

### 5. Visualization & Communication
- **Exploratory Plots**: Quick insights and pattern discovery
- **Presentation Graphics**: Publication-ready visualizations
- **Interactive Dashboards**: Dynamic exploration tools
- **Statistical Reports**: Methodology and findings documentation

## Technical Capabilities:

### Core Libraries Utilized:
```python
# Data Manipulation
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Statistical Analysis
import scipy.stats as stats
import statsmodels.api as sm

# Dashboard Development
import dash
from dash import dcc, html
import streamlit as st
```

### Analysis Patterns:
- **Automated EDA**: Comprehensive data profiling with pandas-profiling
- **Statistical Testing**: Hypothesis tests, ANOVA, chi-square tests
- **Time Series**: Trend analysis, seasonality decomposition, forecasting
- **Machine Learning**: Classification, regression, clustering, dimensionality reduction

### Visualization Gallery:
- **Distribution Plots**: Histograms, box plots, violin plots, density plots
- **Relationship Plots**: Scatter plots, correlation heatmaps, pair plots
- **Time Series Plots**: Line charts, seasonality plots, trend analysis
- **Categorical Analysis**: Bar charts, pie charts, stacked plots
- **Statistical Plots**: Q-Q plots, residual plots, ROC curves

## Integration Features:

### TodoWrite Integration:
- **Analysis Tasks**: Break down complex analysis into manageable steps
- **Progress Tracking**: Monitor data pipeline and modeling progress
- **Quality Checkpoints**: Validation steps and review milestones
- **Deliverable Tracking**: Reports, models, and dashboard completion

### Project Management:
- **Reproducible Workflows**: Version-controlled analysis pipelines
- **Environment Management**: Conda/pip requirements for consistency
- **Documentation Standards**: Well-commented notebooks and reports
- **Code Review**: Statistical methodology and implementation review

### Output Formats:
- **Jupyter Notebooks**: Interactive analysis with markdown documentation
- **HTML Reports**: Static reports with embedded visualizations
- **PDF Reports**: Publication-ready documents with findings
- **Interactive Apps**: Deployable dashboards for stakeholder access

## Quality Assurance:
- ✅ **Statistical Rigor**: Proper methodology and validation techniques
- ✅ **Code Quality**: Clean, documented, reproducible code
- ✅ **Data Validation**: Quality checks and consistency verification
- ✅ **Performance Metrics**: Appropriate evaluation for each model type
- ✅ **Communication**: Clear insights and actionable recommendations

The data science workbench creates comprehensive TodoWrite task lists for systematic analysis, modeling, and reporting workflows while maintaining scientific rigor and reproducibility.