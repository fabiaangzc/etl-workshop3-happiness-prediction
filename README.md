# 🌍 ETL Workshop 3 - Happiness Prediction System with Kafka# 🌍 ETL Workshop 3 - Happiness Prediction System with Kafka Streaming



[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

[![Kafka](https://img.shields.io/badge/Kafka-7.5.0-black.svg)](https://kafka.apache.org/)[![Kafka](https://img.shields.io/badge/Kafka-7.5.0-black.svg)](https://kafka.apache.org/)

[![Docker](https://img.shields.io/badge/Docker-Required-2496ED.svg)](https://www.docker.com/)[![Docker](https://img.shields.io/badge/Docker-Required-2496ED.svg)](https://www.docker.com/)

[![Dash](https://img.shields.io/badge/Dash-2.14.2-00D4FF.svg)](https://dash.plotly.com/)[![Dash](https://img.shields.io/badge/Dash-2.14.2-00D4FF.svg)](https://dash.plotly.com/)

[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)](https://www.mysql.com/)[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)](https://www.mysql.com/)



## 📖 Overview## 📖 Table of Contents



A complete **end-to-end Machine Learning pipeline** for predicting happiness scores using the World Happiness Report (2015-2019). This system integrates:- [Overview](#-overview)

- [Project Architecture](#-project-architecture)

- **ETL Pipeline** with Apache Kafka for real-time data streaming- [Project Structure](#-project-structure)

- **Machine Learning** model (Linear Regression) for happiness prediction- [Prerequisites](#-prerequisites)

- **Data Persistence** in MySQL database- [Installation & Setup](#-installation--setup)

- **Interactive Dashboard** built with Dash & Plotly- [Complete Workflow](#-complete-workflow)

- **Comprehensive EDA** in Jupyter notebooks- [Dashboard](#-interactive-dashboard)

- [Database Schema](#-database-schema)

### Key Features- [Model Performance](#-model-performance)

- [Troubleshooting](#-troubleshooting)

✅ Real-time streaming with Apache Kafka  - [Additional Resources](#-additional-resources)

✅ Automated ETL process with data transformation  

✅ Train/Test split tracking (70-30)  ---

✅ MySQL database for prediction storage  

✅ Interactive web dashboard with 10 visualizations  ## 🎯 Overview

✅ Geographic analysis with world map  

✅ Temporal analysis (2015-2019)  This project implements a **complete end-to-end Machine Learning pipeline** for predicting happiness scores based on the World Happiness Report (2015-2019). The system integrates:

✅ Regional performance metrics  

- **ETL Pipeline**: Apache Kafka streaming for real-time data processing

---- **Machine Learning**: Linear Regression model for happiness prediction

- **Data Persistence**: MySQL database for storing predictions

## 🏗️ Architecture- **Interactive Dashboard**: Web-based visualization dashboard with Dash & Plotly

- **Analytics**: Comprehensive exploratory data analysis (EDA) notebooks

```

CSV Files (2015-2019)### Key Features

        ↓

    Producer.py (ETL)✅ **Real-time streaming** with Apache Kafka  

        ↓✅ **Automated ETL** process with data transformation  

    Kafka Topic✅ **Train/Test split tracking** for model validation  

        ↓✅ **Prediction storage** in MySQL database  

   Consumer.py (ML)✅ **Professional dashboard** with 8+ interactive visualizations  

        ↓✅ **Geographic analysis** with choropleth maps  

    MySQL Database✅ **Temporal analysis** across 5 years (2015-2019)  

        ↓✅ **Regional performance** metrics and insights  

    Dashboard (Dash)

```---



---## �️ Project Architecture



## 📂 Project Structure```

┌─────────────────┐

```│   CSV Files     │ (World Happiness 2015-2019)

etl-workshop3/│  (782 records)  │

├── 📊 data/                          # World Happiness datasets└────────┬────────┘

│   ├── 2015.csv         │

│   ├── 2016.csv         ▼

│   ├── 2017.csv┌─────────────────┐

│   ├── 2018.csv│ Kafka Producer  │ ◄─── ETL: Extract, Transform, Load

│   ├── 2019.csv│  (producer.py)  │      • Column standardization

│   ├── happiness_all.csv             # Unified dataset└────────┬────────┘      • Missing value imputation

│   └── clean/                        # Cleaned datasets         │               • Region mapping

│         │               • Train/test split (70-30)

├── 🎛️ dashboard/         ▼

│   └── happiness_dashboard.py        # Interactive dashboard┌─────────────────┐

││  Kafka Topic    │

├── 📮 kafka/│ happiness-data  │

│   ├── producer.py                   # ETL Pipeline└────────┬────────┘

│   └── consumer.py                   # ML Predictions + MySQL         │

│         ▼

├── 🤖 model/┌─────────────────┐

│   └── happiness_regression.pkl      # Trained model│ Kafka Consumer  │ ◄─── ML Prediction + Storage

││  (consumer.py)  │      • Load trained model

├── 📓 notebooks/└────────┬────────┘      • Predict happiness score

│   ├── 1_pre_EDA.ipynb              # Pre-processing analysis         │               • Calculate errors

│   ├── 2_transformation.ipynb        # Data transformation         │               • Store in MySQL

│   ├── 3_post_EDA.ipynb             # Post-transformation analysis         ▼

│   ├── 4_regression_models.ipynb     # Model comparison┌─────────────────┐      ┌──────────────────┐

│   └── 5_train_model.ipynb          # Final model training│  MySQL Database │◄────►│     Dashboard    │

││  predictions    │      │ happiness_dash   │

├── 🐳 docker-compose.yml             # Kafka + Zookeeper│   (782 rows)    │      │  (Port 8050)     │

├── 📋 requirements.txt└─────────────────┘      └──────────────────┘

└── 📖 README.md```

```

---

---

## 📂 Project Structure

## 📋 Prerequisites

```

- **Python 3.8+**etl-workshop3/

- **Docker & Docker Compose**├── 📊 data/                       # Original and processed datasets

- **MySQL 8.0** (local installation)│   ├── 2015.csv                   # World Happiness Report 2015

- **8GB RAM minimum**│   ├── 2016.csv                   # World Happiness Report 2016

│   ├── 2017.csv                   # World Happiness Report 2017

---│   ├── 2018.csv                   # World Happiness Report 2018

│   ├── 2019.csv                   # World Happiness Report 2019

## 🚀 Quick Start│   ├── happiness_all.csv          # Unified dataset (reference)

│   └── clean/                     # Cleaned datasets (reference)

### 1. Clone & Setup Environment│

├── 🎛️ dashboard/                  # Interactive web dashboard

```bash│   ├── happiness_dashboard.py     # Main dashboard application

# Clone repository│   └── README_DASHBOARD.md        # Dashboard documentation

git clone <your-repo-url>│

cd etl-workshop3├── 📮 kafka/                      # Kafka streaming components

│   ├── producer.py                # Producer: ETL pipeline

# Create virtual environment│   └── consumer.py                # Consumer: ML prediction + MySQL

python -m venv .venv│

├── 🤖 model/                      # Trained ML models

# Activate (Windows PowerShell)│   └── happiness_regression.pkl   # Linear Regression model

.venv\Scripts\Activate.ps1│

├── 📓 notebooks/                  # Jupyter notebooks for analysis

# Install dependencies│   ├── 1_pre_EDA.ipynb           # Pre-processing exploratory analysis

pip install -r requirements.txt│   ├── 2_transformation.ipynb     # Data transformation (reference)

```│   ├── 3_post_EDA.ipynb          # Post-transformation analysis

│   ├── 4_regression_models.ipynb  # Model exploration & comparison

### 2. Start Docker Services│   └── 5_train_model.ipynb       # Final model training

│

```bash├── 🐳 docker-compose.yml          # Docker services configuration

docker-compose up -d├── 📋 requirements.txt            # Python dependencies

```└── 📖 README.md                   # This file

```

Starts: **Zookeeper** (2181) & **Kafka** (9092)

---

### 3. Setup MySQL Database

## 📋 Prerequisites

The consumer creates the database automatically. Ensure MySQL is running:

Before starting, ensure you have:

```bash

# Windows- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)

net start MySQL80- **Docker & Docker Compose** - [Install Docker](https://docs.docker.com/get-docker/)

- **Git** (optional) - [Install Git](https://git-scm.com/downloads/)

# Verify connection- **8GB RAM minimum** (for Docker containers)

mysql -u root -p- **2GB free disk space**

```



**Default credentials** (edit in `kafka/consumer.py` if different):---

- Host: `localhost`

- Port: `3306`## 🚀 Installation & Setup

- User: `root`

- Password: `root`### Step 1: Clone the Repository

- Database: `happiness_db` (auto-created)

```bash

### 4. Train Model (First Time Only)git clone <your-repository-url>

cd etl-workshop3

```bash```

jupyter notebook notebooks/5_train_model.ipynb

# Run all cells to generate model/happiness_regression.pkl### Step 2: Create Virtual Environment & Install Dependencies

```

#### Windows (PowerShell)

### 5. Run Kafka Producer (ETL)```powershell

# Create virtual environment

```bashpython -m venv .venv

cd kafka

python producer.py# Activate virtual environment

```.venv\Scripts\Activate.ps1



**Output:**# Install dependencies

```pip install -r requirements.txt

[1/3] EXTRACTION - Loading CSV files...```

  ✓ 2015: 158 records

  ✓ 2016: 157 records#### Windows (CMD)

  ...```cmd

  # Create virtual environment

[2/3] TRANSFORMATION - Cleaning data...python -m venv .venv

  ✓ Unified dataset: 782 records

  ✓ Train: 547 (70%) | Test: 235 (30%)# Activate virtual environment

  .venv\Scripts\activate.bat

[3/3] LOADING - Sending to Kafka...

  ✓ 782 records sent successfully# Install dependencies

```pip install -r requirements.txt

```

### 6. Run Kafka Consumer (Predictions)

#### Linux/macOS

```bash```bash

# New terminal# Create virtual environment

cd kafkapython3 -m venv .venv

python consumer.py

```# Activate virtual environment

source .venv/bin/activate

**Output:**

```# Install dependencies

✓ Model loaded: happiness_regression.pklpip install -r requirements.txt

✓ Database connected: happiness_db```

✓ Processing predictions...

  ✓ 782 records processed and stored### Step 3: Start Docker Services

```

```bash

### 7. Launch Dashboard# Start Kafka and Zookeeper

docker-compose up -d

```bash```

cd dashboard

python happiness_dashboard.pyThis will start:

```- **Zookeeper** on port `2181`

- **Kafka Broker** on port `9092`

Open: **http://127.0.0.1:8050**

Verify services are running:

---```bash

docker-compose ps

## 📊 Dashboard Features```



The interactive dashboard includes:Expected output:

```

1. **🔍 Filters** - Dataset (All/Train/Test), Region, YearNAME                IMAGE                              STATUS

2. **📊 KPI Cards** - Total Records, MAE, RMSE, R²kafka               confluentinc/cp-kafka:7.5.0       Up

3. **📈 Scatter Plot** - Predicted vs Actual valueszookeeper           confluentinc/cp-zookeeper:latest  Up

4. **📉 Error Distribution** - Histogram with MAE reference```

5. **⚖️ Train vs Test** - Performance comparison

6. **🔝 Top 10 Errors** - Largest prediction errors### Step 4: Setup Local MySQL Database

7. **🌎 Regional Performance** - MAE and R² by region

8. **🗺️ World Map** - Geographic error distributionThis project uses a **local MySQL instance** (not Docker) for better performance and persistence.

9. **📅 Temporal Evolution** - Trends from 2015-2019

10. **🧠 Auto Insights** - Dynamic analysis and recommendations#### Install MySQL 8.0



---- **Windows**: [Download MySQL Installer](https://dev.mysql.com/downloads/installer/)

- **macOS**: `brew install mysql`

## 🗄️ Database Schema- **Linux**: `sudo apt-get install mysql-server`



### Table: `predictions`#### Configure MySQL Connection



| Column | Type | Description |The consumer expects:

|--------|------|-------------|- **Host**: `localhost`

| `id` | INT | Primary key |- **Port**: `3306`

| `country` | VARCHAR(100) | Country name |- **User**: `root`

| `region` | VARCHAR(100) | Geographic region |- **Password**: `root`

| `year` | INT | Year (2015-2019) |- **Database**: `happiness_db` (created automatically)

| `GDP_per_Capita` | FLOAT | GDP feature |

| `Social_Support` | FLOAT | Social support |To change these settings, edit `kafka/consumer.py`:

| `Healthy_Life_Expectancy` | FLOAT | Life expectancy |

| `Freedom` | FLOAT | Freedom score |```python

| `Generosity` | FLOAT | Generosity score |DB_CONFIG = {

| `Perceptions_of_Corruption` | FLOAT | Corruption perception |    'host': 'localhost',

| `actual_happiness_score` | FLOAT | Real value |    'port': 3306,

| `predicted_happiness_score` | FLOAT | Model prediction |    'user': 'root',

| `prediction_error` | FLOAT | Absolute error |    'password': 'your_password',  # Change this

| `data_split` | VARCHAR(10) | 'train' or 'test' |    'database': 'happiness_db'

| `created_at` | TIMESTAMP | Insert timestamp |}

```

### Query Examples

---

```sql

-- View predictions## 🔄 Complete Workflow

SELECT country, year, actual_happiness_score, 

       predicted_happiness_score, prediction_error### Overview

FROM predictions LIMIT 10;

The complete workflow consists of 5 stages:

-- Performance by split

SELECT data_split, COUNT(*) as count, 1. **Data Exploration** (Notebooks 1, 3, 4)

       AVG(prediction_error) as avg_error2. **Model Training** (Notebook 5)

FROM predictions GROUP BY data_split;3. **ETL Pipeline** (Kafka Producer)

4. **Prediction & Storage** (Kafka Consumer)

-- Top errors5. **Visualization** (Dashboard)

SELECT country, year, prediction_error

FROM predictions ---

ORDER BY prediction_error DESC LIMIT 10;

```### Stage 1: Exploratory Data Analysis (EDA)



---The `notebooks/` directory contains comprehensive analysis:



## 📈 Model Performance#### **1_pre_EDA.ipynb** - Pre-processing Analysis

- Load raw datasets (2015-2019)

- **Algorithm**: Linear Regression- Analyze data structure and quality

- **Training**: 547 records (70%)- Identify missing values and outliers

- **Testing**: 235 records (30%)- Visualize distributions by year

- **Features**: 6 numeric predictors- Correlation analysis per dataset

- **Target**: Happiness Score (0-10)

#### **2_transformation.ipynb** - Data Transformation (Reference Only)

**Expected Metrics:**- Column standardization

- MAE: ~0.40-0.50- Missing value imputation

- RMSE: ~0.50-0.60- Region mapping

- R²: ~0.70-0.80- Data type conversions

- **Note**: This is for reference only. In production, all transformations are automated in `producer.py`

---

#### **3_post_EDA.ipynb** - Post-transformation Analysis

## 🛠️ Troubleshooting- Verify transformation quality

- Analyze cleaned unified dataset

### Kafka Not Available- Feature engineering validation

```bash

docker-compose ps#### **4_regression_models.ipynb** - Model Exploration

docker-compose logs kafka- Compare multiple regression algorithms

docker-compose restart- Hyperparameter tuning

```- Feature importance analysis

- Cross-validation results

### MySQL Connection Failed

```bash---

# Check MySQL is running

net start MySQL80### Stage 2: Train the Machine Learning Model



# Test connection#### **5_train_model.ipynb** - Final Model Training

mysql -u root -p

This notebook trains the production model:

# Update credentials in consumer.py if needed

``````bash

# Open Jupyter

### Model Not Foundjupyter notebook notebooks/5_train_model.ipynb

```bash```

# Train the model first

jupyter notebook notebooks/5_train_model.ipynbThe notebook performs:

```- ✅ Load cleaned dataset (`happiness_all.csv`)

- ✅ Feature selection (6 features)

### Port 8050 In Use- ✅ Train/test split (70%-30%, `random_state=42`)

```bash- ✅ Train Linear Regression model

# Change port in happiness_dashboard.py:- ✅ Evaluate metrics (MAE, RMSE, R²)

app.run_server(debug=True, port=8051)- ✅ Save model to `model/happiness_regression.pkl`

```

**Features used:**

---1. GDP per Capita

2. Social Support

## 🧹 Cleanup3. Healthy Life Expectancy

4. Freedom to Make Life Choices

```bash5. Generosity

# Stop Docker6. Perceptions of Corruption

docker-compose down

**Target variable:** Happiness Score

# Remove volumes

docker-compose down -v---



# Drop MySQL database### Stage 3: Run Kafka Producer (ETL Pipeline)

mysql -u root -p

DROP DATABASE happiness_db;The producer performs the **complete ETL process**:

```

**Extract** → Load 5 CSV files (2015-2019)  

---**Transform** → Apply all cleaning and standardization  

**Load** → Stream records to Kafka topic

## 📚 Technologies

```bash

| Technology | Version | Purpose |cd kafka

|------------|---------|---------|python producer.py

| Python | 3.8+ | Core language |```

| Kafka | 7.5.0 | Stream processing |

| MySQL | 8.0 | Database |#### Expected Output:

| Scikit-learn | 1.3.2 | Machine learning |

| Dash | 2.14.2 | Web dashboard |```

| Plotly | 5.18.0 | Visualizations |==============================================

| Pandas | 2.1.4 | Data manipulation |    KAFKA PRODUCER - HAPPINESS ETL

| Docker | Latest | Containerization |==============================================



---[1/3] EXTRACTION - Loading CSV files...

  ✓ 2015: 158 records loaded

## 📄 License  ✓ 2016: 157 records loaded

  ✓ 2017: 155 records loaded

Academic project for ETL Workshop 3 - 5th Semester  ✓ 2018: 156 records loaded

  ✓ 2019: 156 records loaded

---  

[2/3] TRANSFORMATION - Cleaning and standardizing...

## 🔗 Resources  ✓ Region dictionary created: 158 countries

  ✓ Dataset 2015 processed: 158 records

- [Apache Kafka Docs](https://kafka.apache.org/documentation/)  ✓ Dataset 2016 processed: 157 records

- [Dash Documentation](https://dash.plotly.com/)  ✓ Dataset 2017 processed: 155 records

- [Scikit-learn Guide](https://scikit-learn.org/stable/)  ✓ Dataset 2018 processed: 156 records

- [World Happiness Report](https://worldhappiness.report/)  ✓ Dataset 2019 processed: 156 records

  ✓ Unified dataset created: 782 records

---  

  Train/Test Split:

**⭐ Star this project if you find it helpful!**  ✓ Training set: 547 records (70.0%)

  ✓ Test set: 235 records (30.0%)

*Last updated: November 2025*  

[3/3] LOADING - Sending data to Kafka...
  ✓ Producer connected to Kafka
  ✓ Topic: happiness-data
  Progress: 50/782 records sent
  Progress: 100/782 records sent
  Progress: 150/782 records sent
  ...
  Progress: 750/782 records sent
  ✓ All records sent successfully: 782

==============================================
✓ ETL PROCESS COMPLETED SUCCESSFULLY
==============================================
```

#### What the Producer Does:

1. **Reads** all 5 CSV files
2. **Creates** region mapping dictionary
3. **Standardizes** column names across years
4. **Imputes** missing values (median strategy)
5. **Splits** data into train/test (70-30)
6. **Serializes** records to JSON
7. **Streams** to Kafka topic `happiness-data`

---

### Stage 4: Run Kafka Consumer (ML Prediction)

The consumer receives messages, predicts happiness scores, and stores results in MySQL:

```bash
# Open a new terminal (keep producer running or after it finishes)
cd kafka
python consumer.py
```

#### Expected Output:

```
==============================================
   KAFKA CONSUMER - HAPPINESS PREDICTIONS
==============================================

✓ Model loaded: ../model/happiness_regression.pkl
  Model type: LinearRegression
  Features: 6 (GDP, Social Support, Life Expectancy, etc.)

✓ Database connection established
  Host: localhost:3306
  Database: happiness_db
  
✓ Table 'predictions' ready
  Columns: 16 (id, country, region, year, features, scores, etc.)

✓ Consumer connected to Kafka
  Topic: happiness-data
  Group: happiness-consumer-group-v2
  
Processing predictions...
  ✓ 50 records processed
  ✓ 100 records processed
  ✓ 150 records processed
  ...
  ✓ 782 records processed

==============================================
✓ ALL PREDICTIONS STORED IN MYSQL
==============================================
```

#### What the Consumer Does:

1. **Loads** trained ML model (`.pkl`)
2. **Creates** MySQL database automatically
3. **Consumes** messages from Kafka
4. **Extracts** features for prediction
5. **Predicts** happiness score
6. **Calculates** prediction error
7. **Inserts** results into MySQL with train/test label

---

### Stage 5: Launch Interactive Dashboard

The dashboard provides comprehensive visualization of predictions:

```bash
cd dashboard
python happiness_dashboard.py
```

#### Expected Output:

```
======================================================================
🌍 HAPPINESS PREDICTION ANALYSIS DASHBOARD
======================================================================
📊 Total records loaded: 782
📅 Available years: [2015, 2016, 2017, 2018, 2019]
🌎 Available regions: 10
🏳️ Unique countries: 158
======================================================================
🚀 Starting dashboard server...
🌐 Access the dashboard at: http://127.0.0.1:8050
======================================================================
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'happiness_dashboard'
 * Debug mode: on
```

Open your browser and navigate to: **http://127.0.0.1:8050**

---

## 📊 Interactive Dashboard

### Dashboard Features

The dashboard includes **8 comprehensive sections**:

#### 1. 🔍 **Filters Panel**
- **Dataset**: All / Training / Test
- **Region**: All regions or specific region
- **Year**: All years or specific year (2015-2019)

#### 2. 📊 **Performance Metrics (KPIs)**
Four key performance indicators:
- **Total Records**: Count of predictions (split by train/test)
- **MAE** (Mean Absolute Error): Average prediction error
- **RMSE** (Root Mean Squared Error): Penalizes large errors
- **R²** (Coefficient of Determination): Model fit quality (0-1)

#### 3. 📈 **Predicted vs Actual Values**
- Scatter plot comparing predictions to actual values
- Perfect prediction line (red dashed)
- Color-coded by train/test split
- Interactive hover with country details

#### 4. 📉 **Prediction Error Distribution**
- Histogram of absolute prediction errors
- Overlaid train/test distributions
- Vertical line showing global MAE
- Identifies error patterns and outliers

#### 5. ⚖️ **Train vs Test Comparison**
- Side-by-side bar chart
- Compare MAE and RMSE between sets
- Detect overfitting/underfitting

#### 6. 🔝 **Top 10 Largest Errors**
- Horizontal bar chart
- Countries with highest prediction errors
- Color-coded by train/test split
- Useful for identifying model weaknesses

#### 7. 🌎 **Performance by Region**
- Dual bar charts (MAE and R² by region)
- Identify geographic patterns
- Compare regional model performance

#### 8. 🗺️ **Geographic Performance Map**
- Choropleth world map
- Color intensity = prediction error
- Interactive hover with country statistics
- Visualize global model performance

#### 9. 📅 **Temporal Evolution (2015-2019)**
- Dual line charts:
  - MAE evolution over time
  - Average happiness trends (actual vs predicted)
- Analyze temporal patterns
- Track model consistency across years

#### 10. 🧠 **Automatic Insights**
- Dynamic text analysis
- Global metrics summary
- Best/worst performing regions
- Model bias detection (over/under prediction)

---

## 🗄️ Database Schema

### Table: `predictions`

The MySQL table stores all predictions with the following schema:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INT | Primary key (auto-increment) |
| `country` | VARCHAR(100) | Country name |
| `region` | VARCHAR(100) | Geographic region |
| `year` | INT | Year (2015-2019) |
| `GDP_per_Capita` | FLOAT | GDP per capita (normalized) |
| `Social_Support` | FLOAT | Social support score |
| `Healthy_Life_Expectancy` | FLOAT | Life expectancy score |
| `Freedom` | FLOAT | Freedom to make choices |
| `Generosity` | FLOAT | Generosity score |
| `Perceptions_of_Corruption` | FLOAT | Corruption perception |
| `actual_happiness_score` | FLOAT | Real happiness score |
| `predicted_happiness_score` | FLOAT | Model prediction |
| `prediction_error` | FLOAT | Absolute error |
| `data_split` | VARCHAR(10) | 'train' or 'test' |
| `created_at` | TIMESTAMP | Record insertion time |

### Query Examples

```sql
-- Connect to MySQL
mysql -u root -p

-- Use the database
USE happiness_db;

-- View first 10 predictions
SELECT 
    country, 
    year, 
    actual_happiness_score, 
    predicted_happiness_score,
    prediction_error,
    data_split
FROM predictions
LIMIT 10;

-- Calculate global statistics
SELECT 
    COUNT(*) as total_predictions,
    AVG(prediction_error) as avg_error,
    MIN(prediction_error) as min_error,
    MAX(prediction_error) as max_error,
    STDDEV(prediction_error) as std_error
FROM predictions;

-- Statistics by train/test split
SELECT 
    data_split,
    COUNT(*) as count,
    AVG(prediction_error) as avg_error,
    MIN(prediction_error) as min_error,
    MAX(prediction_error) as max_error
FROM predictions
GROUP BY data_split;

-- Predictions by year
SELECT 
    year,
    COUNT(*) as count,
    AVG(actual_happiness_score) as avg_actual,
    AVG(predicted_happiness_score) as avg_predicted,
    AVG(prediction_error) as avg_error
FROM predictions
GROUP BY year
ORDER BY year;

-- Top 10 countries by prediction error
SELECT 
    country,
    year,
    region,
    actual_happiness_score,
    predicted_happiness_score,
    prediction_error,
    data_split
FROM predictions
ORDER BY prediction_error DESC
LIMIT 10;

-- Performance by region
SELECT 
    region,
    COUNT(*) as countries,
    AVG(prediction_error) as avg_error,
    MIN(prediction_error) as min_error,
    MAX(prediction_error) as max_error
FROM predictions
GROUP BY region
ORDER BY avg_error ASC;
```

---

## 📈 Model Performance

### Model Specifications

- **Algorithm**: Linear Regression (Scikit-learn)
- **Training Data**: 547 records (70%)
- **Test Data**: 235 records (30%)
- **Random State**: 42 (reproducible splits)
- **Features**: 6 numeric predictors
- **Target**: Happiness Score (0-10 scale)

### Expected Performance Metrics

Based on the World Happiness Report dataset:

| Metric | Training Set | Test Set | Description |
|--------|--------------|----------|-------------|
| **MAE** | ~0.35-0.45 | ~0.40-0.50 | Average absolute error |
| **RMSE** | ~0.45-0.55 | ~0.50-0.60 | Root mean squared error |
| **R²** | ~0.75-0.80 | ~0.70-0.75 | Variance explained |

### Feature Importance

The model relies on these features (typical order of importance):

1. **GDP per Capita** (highest correlation)
2. **Healthy Life Expectancy**
3. **Social Support**
4. **Freedom to Make Life Choices**
5. **Perceptions of Corruption**
6. **Generosity** (lowest correlation)

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 🔴 Error: "Kafka broker not available"

```bash
# Check if Kafka is running
docker-compose ps

# View Kafka logs
docker-compose logs kafka

# Restart services
docker-compose restart

# If persistent, remove and recreate
docker-compose down
docker-compose up -d
```

#### 🔴 Error: "Can't connect to MySQL server"

```bash
# Check MySQL service status
# Windows
net start MySQL80

# Linux/macOS
sudo systemctl status mysql

# Test connection
mysql -u root -p -h localhost

# Verify credentials in consumer.py match your MySQL setup
```

#### 🔴 Error: "Model file not found"

```bash
# Verify model exists
ls model/happiness_regression.pkl

# If missing, train the model
jupyter notebook notebooks/5_train_model.ipynb
# Run all cells to generate the .pkl file
```

#### 🔴 Error: "Topic 'happiness-data' does not exist"

The topic is created automatically by the producer. Ensure:
- Kafka is running (`docker-compose ps`)
- Producer completed successfully
- Wait 10-15 seconds for topic creation

```bash
# Manually create topic (if needed)
docker exec -it kafka kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic happiness-data \
  --partitions 1 \
  --replication-factor 1
```

#### 🔴 Error: "Port 8050 already in use"

```bash
# Find process using port 8050
# Windows
netstat -ano | findstr :8050

# Linux/macOS
lsof -i :8050

# Kill the process or change dashboard port in happiness_dashboard.py:
app.run_server(debug=True, port=8051)  # Use different port
```

#### 🔴 Error: "Access denied for user 'root'@'localhost'"

Update MySQL password in `consumer.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'YOUR_ACTUAL_PASSWORD',  # Change this
    'database': 'happiness_db'
}
```

---

## 🧹 Cleanup & Reset

### Stop Services

```bash
# Stop Docker containers
docker-compose down
```

### Remove All Data

```bash
# Stop and remove volumes (deletes Kafka data)
docker-compose down -v

# Remove Docker images
docker-compose down --rmi all

# Drop MySQL database
mysql -u root -p
DROP DATABASE IF EXISTS happiness_db;
EXIT;
```

### Reset Virtual Environment

```bash
# Deactivate environment
deactivate

# Remove environment folder
# Windows
rmdir /s .venv

# Linux/macOS
rm -rf .venv

# Recreate fresh environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

---

## 📚 Additional Resources

### Documentation

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Python](https://plotly.com/python/)
- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [World Happiness Report](https://worldhappiness.report/)

### Dataset Information

- **Source**: World Happiness Report (2015-2019)
- **Records**: 782 country-year observations
- **Countries**: 158 unique countries
- **Regions**: 10 geographic regions
- **Features**: 6 happiness predictors + 1 target variable

### Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Programming language |
| Apache Kafka | 7.5.0 | Stream processing |
| Zookeeper | Latest | Kafka coordination |
| MySQL | 8.0 | Database storage |
| Scikit-learn | 1.3.2 | Machine learning |
| Dash | 2.14.2 | Web dashboard |
| Plotly | 5.18.0 | Data visualization |
| Pandas | 2.1.4 | Data manipulation |
| Docker | Latest | Containerization |

---

## 👥 Contributors

Developed as part of **ETL Workshop 3** - 5th Semester

### Project Team
- Data Engineering & ETL Pipeline
- Machine Learning Model Development
- Dashboard Design & Implementation
- Documentation & Testing

---

## 📄 License

This project is developed for **academic purposes** as part of the ETL course curriculum.

### Usage

- ✅ Educational use
- ✅ Learning and experimentation
- ✅ Portfolio demonstration
- ❌ Commercial use
- ❌ Redistribution without attribution

---

## 🙏 Acknowledgments

- **World Happiness Report** for providing the dataset
- **Apache Kafka** for the streaming platform
- **Plotly/Dash** for the visualization framework
- Course instructors and teaching assistants

---

## 📞 Support

For questions or issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review Docker logs: `docker-compose logs`
3. Verify MySQL connection and credentials
4. Ensure all dependencies are installed
5. Check that ports are not in use (8050, 9092, 2181, 3306)

---

**⭐ If you found this project helpful, please consider giving it a star!**

---

*Last updated: November 2025*
