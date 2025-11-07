# Happiness Prediction with Kafka Streaming, Linear Regression & Dash

Predicting World Happiness scores from 2015–2019 with a **Multiple Linear Regression** model, streamed through **Apache Kafka** into **MySQL**, and visualized in an interactive **Dash (Plotly)** dashboard.

> **Tech stack:** Python, scikit-learn, Kafka (producer/consumer), MySQL, SQLAlchemy, Plotly/Dash, Pandas, NumPy.

---

## 1) Project Overview

This repository implements an end-to-end mini data platform:

1. **ETL & Streaming**
   The **producer** loads the raw CSVs (2015–2019), cleans and standardizes fields, assigns regions, and **streams each record to Kafka** (`happiness-data`).
   The **consumer** reads those messages, **loads the trained regression model**, makes a prediction per record, and **stores results in MySQL** (table `predictions`).

2. **Model**
   A Multiple Linear Regression trained on six explanatory variables:
   `GDP_per_Capita`, `Social_Support`, `Healthy_Life_Expectancy`, `Freedom`, `Generosity`, `Perceptions_of_Corruption`.

3. **Dashboard**
   A Dash app reads the `predictions` table and provides KPIs (R², MAE, RMSE), train/test comparisons, error distributions, top-errors, regional performance, a country choropleth (MAE), and temporal evolution charts.

---

## 2) Repository Structure

```
.
├─ data/
│  ├─ clean/
│  │  ├─ 2015.csv … 2019.csv
│  │  └─ happiness_all.csv              # (optional, if you export it)
├─ kafka/
│  ├─ producer.py                        # ETL + stream to Kafka
│  └─ consumer.py                        # Predict + load to MySQL
├─ model/
│  └─ happiness_regression.pkl           # Trained sklearn model
├─ notebooks/
│  ├─ 1_pre_EDA.ipynb
│  ├─ 2_transformation.ipynb
│  ├─ 3_post_EDA.ipynb
│  ├─ 4_regression_models.ipynb
│  └─ 5_train_model.ipynb               # Final training + export .pkl
├─ dashboard/
│  └─ happiness_dashboard.py             # Dash app (Plotly)
├─ docker-compose.yml                    # (optional) if you containerize
├─ requirements.txt
└─ README.md
```

---

## 3) Data

**Source:** World Happiness Report (2015–2019).
Files are normalized so that column names align across years (e.g., *Economy (GDP per Capita)* → `GDP_per_Capita`; *Health (Life Expectancy)* → `Healthy_Life_Expectancy`; etc.). Country aliases are reconciled (e.g., *Hong Kong S.A.R.* → *Hong Kong*).

---

## 4) End-to-End Architecture

```
CSV (2015–2019)
      │
      ▼
[ producer.py ]  — cleanse, standardize, fix regions, add train/test flags
      │
      ├── Kafka topic: happiness-data
      ▼
[ consumer.py ] — load regression model (.pkl) → predict → write to MySQL
      │
      ▼
           MySQL (database: happiness_db)
           └─ predictions (actual, predicted, error, split, region, etc.)
                                   │
                                   ▼
                       [ Dash app ] happiness_dashboard.py
```

**Kafka Topic:** `happiness-data`
**DB:** `happiness_db` (MySQL) with table `predictions`.
**Model path:** `model/happiness_regression.pkl`.

---

## 5) Features & Model

**Target:** `Happiness_Score`
**Features:**

* `GDP_per_Capita`
* `Social_Support`
* `Healthy_Life_Expectancy`
* `Freedom`
* `Generosity`
* `Perceptions_of_Corruption`

**Split:** 70% train / 30% test (seed = 42), aligned between the notebook and the streaming pipeline.

**Metrics reported in the dashboard:**

* **R²** (Coefficient of Determination)
* **MAE** (Mean Absolute Error)
* **RMSE** (Root Mean Squared Error)

---

## 6) Database Schema (Predictions)

Table: `predictions` (MySQL)

| Column                      | Type          | Notes                     |
| --------------------------- | ------------- | ------------------------- |
| id                          | INT (PK, AI)  |                           |
| country, region             | VARCHAR       | From the streaming record |
| year                        | INT           | 2015–2019                 |
| gdp_per_capita … corruption | DECIMAL(10,3) | Input features            |
| actual_happiness_score      | DECIMAL(10,3) | Ground truth (if present) |
| predicted_happiness_score   | DECIMAL(10,3) | Model output              |
| prediction_error            | DECIMAL(10,3) | `abs(actual - predicted)` |
| data_split                  | VARCHAR(10)   | `train` or `test`         |
| created_at                  | TIMESTAMP     | Insertion timestamp       |

---

## 7) Dashboard Overview (Dash/Plotly)

**Filters:** dataset (All/Train/Test), region, year.
**KPIs:** Overall R², MAE, RMSE + train/test breakdown.
**Charts:**

* *Predicted vs Actual* (with y=x reference line)
* *Prediction Error Distribution* (histogram; MAE reference line)
* *Train vs Test Comparison* (bar chart: MAE/RMSE)
* *Top-10 Largest Errors* (horizontal bar)
* *Performance by Region* (dual bars: MAE and R²)
* *Performance Map by Country* (choropleth by MAE)
* *Temporal Evolution* (MAE by year; actual vs predicted averages)

> The app reads directly from the `predictions` table and updates visuals according to filters.

---

## 8) Setup & Execution

### 8.1 Prerequisites

* Python 3.10+
* MySQL 8+ (running locally)
* Kafka 3.x (local broker)
* (Optional) Node/WSL/Docker depending on your environment

### 8.2 Installation

```bash
python -m venv .venv
source .venv/bin/activate        # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 8.3 MySQL

Create a local user or reuse the defaults. The project expects:

```
host=localhost, port=3306, user=root, password=root, database=happiness_db
```

> You can override these via environment variables for the **dashboard**:

```
DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
```

### 8.4 Start Kafka

* Start your local Kafka broker (ensure it listens on `localhost:9092`).
* Create the topic `happiness-data` if your setup doesn’t auto-create topics.

### 8.5 Run the pipeline

**1) Train (optional if `.pkl` exists):**
Use `notebooks/5_train_model.ipynb` to train and export `model/happiness_regression.pkl`.

**2) Producer (ETL → Kafka):**

```bash
python kafka/producer.py
```

**3) Consumer (Kafka → Predict → MySQL):**

```bash
python kafka/consumer.py
```

**4) Dashboard:**

```bash
python dashboard/happiness_dashboard.py
# open http://127.0.0.1:8050
```

---

## 9) Results & Screenshots

> Add your screenshots to a `docs/` folder and reference them here.

**KPIs:**
![KPIs](docs/kpis.png)

**Predicted vs Actual:**
![Scatter](docs/scatter.png)

**Error Distribution:**
![Histogram](docs/histogram.png)

**Train vs Test & Top-10 Errors:**
![Compare+Top](docs/compare_top.png)

**Performance by Region:**
![Region](docs/region.png)

**Performance Map (MAE by Country):**
![Map](docs/map.png)

**Temporal Evolution:**
![Temporal](docs/temporal.png)

---

## 10) Interpreting the Model

* **Global fit:** R² shows how much of the real variability is reproduced by the model (closer to 1 is better).
* **Error magnitude:** MAE is your average absolute error (in the 0–10 happiness scale); RMSE penalizes larger errors more strongly.
* **Generalization:** Train vs Test bars should be of similar magnitude; large gaps may indicate overfitting.
* **Regional heterogeneity:** Regions with higher MAE (and low R²) suggest non-linear patterns or missing drivers not captured by a linear model.
* **Country map:** Quickly highlights where predictions are consistently harder.

---

## 11) Configuration

Environment variables for the dashboard (fallbacks shown):

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=root
export DB_NAME=happiness_db
```

If you change Kafka or DB credentials, update them in the corresponding scripts.

---

## 12) Troubleshooting

* **Kafka connection refused:** Check broker is up and reachable at `localhost:9092`.
* **Topic not found:** Create `happiness-data` or enable auto-creation.
* **MySQL auth errors:** Verify user/password/host and that the server is running.
* **No data in dashboard:** Ensure `consumer.py` has inserted rows into `predictions` and the DB params in the dashboard match your local setup.
* **Unicode/country names on map:** The choropleth uses `locationmode="country names"`. Country aliases were reconciled; add an alias if a country doesn’t color properly.

---

## 13) Reproducibility Notes

* Train/test split uses a fixed random seed so the split is consistent across notebook and streaming pipeline.
* Numerical fields are rounded to three decimals during cleaning to harmonize across years.
* Missing values for `Perceptions_of_Corruption` are imputed by *(region, year)* mean when possible.

---

## 14) Acknowledgments

* World Happiness Report (2015–2019).
* Plotly/Dash for interactive visualization.
* Apache Kafka & MySQL for the streaming and storage layers.

---

### License

This repository is for academic purposes (course ETL Workshop). If you plan to use parts of it elsewhere, adapt credentials and data licenses accordingly.

