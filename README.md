# JobScope Analytics

### Job Data Management & Business Intelligence Dashboard

**JobScope Analytics** is a Python-based data management and analytics dashboard designed to organise job posting information, track company records, monitor expired job listings, and generate meaningful insights through interactive visualisations.

It combines **MySQL-compatible database management, Python, Streamlit, Pandas, and Plotly** to provide a centralised view of job-related data.

**Live Application:** # JobScope Analytics

### Job Data Management & Business Intelligence Dashboard

**JobScope Analytics** is a Python-based data management and analytics dashboard designed to organise job posting information, track company records, monitor expired job listings, and generate meaningful insights through interactive visualisations.

It combines **MySQL-compatible database management, Python, Streamlit, Pandas, and Plotly** to provide a centralised view of job-related data.

**Live Application:** [Add your Streamlit Cloud URL here]

**GitHub Repository:** https://github.com/Sowmya07484/jobscope-analytics

---

## Project Overview

Managing job information across multiple companies can involve duplicate records, outdated listings, and scattered datasets.

JobScope Analytics addresses these challenges through a centralised dashboard that helps organise job records, view company information, distinguish active and expired listings, and explore trends using interactive charts.

The project was developed as an independent demonstration using synthetic data.

## Key Features

- **Dataset Overview:** Displays total records, companies, active jobs, expired jobs, and archived records.
- **Company Management:** Organises company information by industry and location.
- **Job Tracking:** Stores and displays job titles, locations, posting dates, expiry dates, and listing status.
- **Expired Job Archive:** Maintains a separate collection of expired job listings.
- **Interactive Analytics:** Uses charts to explore job posting patterns and company-level information.
- **Data Filtering:** Enables users to explore records using available filters.
- **CSV Export:** Allows filtered job records to be exported for further analysis.
- **Cloud Database Integration:** Connects the dashboard to a cloud-hosted TiDB database.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Dashboard interface |
| MySQL / TiDB Cloud | Database management |
| Pandas | Data processing |
| Plotly | Interactive visualisations |
| MySQL Connector/Python | Database connectivity |
| Certifi | SSL certificate verification |

## System Architecture

1. Job and company records are stored in the relational database.
2. Python connects to the database using MySQL Connector.
3. Pandas retrieves and processes the records.
4. Streamlit presents the data through an interactive dashboard.
5. Plotly generates visual analytics.
6. Users can filter records and export data as CSV files.

## Database Design

The project uses the following database tables and view:

| Table / View | Purpose |
|---|---|
| `companies` | Stores company information |
| `jobs` | Stores job listing information |
| `expired_jobs` | Maintains expired job records |
| `imported_job_report` | Stores imported report data |
| `job_audit_log` | Stores job status-change history |
| `job_company_report` | View combining job and company information |

The database uses relational keys and indexes to support data retrieval and reporting.

## Project Structure

```text
jobscope-analytics/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── .streamlit/
    └── secrets.toml   # Local secrets; excluded from Git
```

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sowmya07484/jobscope-analytics.git
cd jobscope-analytics
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database credentials

Create a `.streamlit/secrets.toml` file and add your own TiDB Cloud connection details:

```toml
[mysql]
host = "YOUR_DATABASE_HOST"
port = 4000
user = "YOUR_DATABASE_USERNAME"
password = "YOUR_DATABASE_PASSWORD"
database = "job_data_management"
```

Never commit database credentials to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## Cloud Deployment

The dashboard is deployed using **Streamlit Community Cloud** and connects to a cloud-hosted **TiDB database**.

Deployment configuration:
- Repository: `Sowmya07484/jobscope-analytics`
- Branch: `main`
- Main file: `app.py`
- Database: TiDB Cloud
- Application hosting: Streamlit Community Cloud

Database credentials are configured through Streamlit Cloud Secrets.

## Data Disclaimer

This project uses synthetic demonstration data. The company names and job records displayed in the dashboard are used for demonstration purposes and should not be interpreted as live job listings or actual company database records.

## Future Scope

- Automated job listing updates.
- Advanced company-wise and industry-wise analytics.
- Scheduled data archival.
- Duplicate record detection.
- Additional reporting and visualisation features.
- Role-based access and user authentication.

## Author

**N. V. Sowmya**  
Computer Science and Engineering  
Stanley College of Engineering and Technology for Women

GitHub: https://github.com/Sowmya07484  
LinkedIn: https://linkedin.com/in/n-v-sowmya/

---

*JobScope Analytics — Organising job data. Discovering insights.*

**GitHub Repository:** https://github.com/Sowmya07484/jobscope-analytics

---

## Project Overview

Managing job information across multiple companies can involve duplicate records, outdated listings, and scattered datasets.

JobScope Analytics addresses these challenges through a centralised dashboard that helps organise job records, view company information, distinguish active and expired listings, and explore trends using interactive charts.

The project was developed as an independent demonstration using synthetic data.

## Key Features

- **Dataset Overview:** Displays total records, companies, active jobs, expired jobs, and archived records.
- **Company Management:** Organises company information by industry and location.
- **Job Tracking:** Stores and displays job titles, locations, posting dates, expiry dates, and listing status.
- **Expired Job Archive:** Maintains a separate collection of expired job listings.
- **Interactive Analytics:** Uses charts to explore job posting patterns and company-level information.
- **Data Filtering:** Enables users to explore records using available filters.
- **CSV Export:** Allows filtered job records to be exported for further analysis.
- **Cloud Database Integration:** Connects the dashboard to a cloud-hosted TiDB database.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Dashboard interface |
| MySQL / TiDB Cloud | Database management |
| Pandas | Data processing |
| Plotly | Interactive visualisations |
| MySQL Connector/Python | Database connectivity |
| Certifi | SSL certificate verification |

## System Architecture

1. Job and company records are stored in the relational database.
2. Python connects to the database using MySQL Connector.
3. Pandas retrieves and processes the records.
4. Streamlit presents the data through an interactive dashboard.
5. Plotly generates visual analytics.
6. Users can filter records and export data as CSV files.

## Database Design

The project uses the following database tables and view:

| Table / View | Purpose |
|---|---|
| `companies` | Stores company information |
| `jobs` | Stores job listing information |
| `expired_jobs` | Maintains expired job records |
| `imported_job_report` | Stores imported report data |
| `job_audit_log` | Stores job status-change history |
| `job_company_report` | View combining job and company information |

The database uses relational keys and indexes to support data retrieval and reporting.

## Project Structure

```text
jobscope-analytics/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── .streamlit/
    └── secrets.toml   # Local secrets; excluded from Git
```

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sowmya07484/jobscope-analytics.git
cd jobscope-analytics
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database credentials

Create a `.streamlit/secrets.toml` file and add your own TiDB Cloud connection details:

```toml
[mysql]
host = "YOUR_DATABASE_HOST"
port = 4000
user = "YOUR_DATABASE_USERNAME"
password = "YOUR_DATABASE_PASSWORD"
database = "job_data_management"
```

Never commit database credentials to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## Cloud Deployment

The dashboard is deployed using **Streamlit Community Cloud** and connects to a cloud-hosted **TiDB database**.

Deployment configuration:
- Repository: `Sowmya07484/jobscope-analytics`
- Branch: `main`
- Main file: `app.py`
- Database: TiDB Cloud
- Application hosting: Streamlit Community Cloud

Database credentials are configured through Streamlit Cloud Secrets.

## Data Disclaimer

This project uses synthetic demonstration data. The company names and job records displayed in the dashboard are used for demonstration purposes and should not be interpreted as live job listings or actual company database records.

## Future Scope

- Automated job listing updates.
- Advanced company-wise and industry-wise analytics.
- Scheduled data archival.
- Duplicate record detection.
- Additional reporting and visualisation features.
- Role-based access and user authentication.

## Author

**N. V. Sowmya**  
Computer Science and Engineering  
Stanley College of Engineering and Technology for Women

GitHub: https://github.com/Sowmya07484  
LinkedIn: https://linkedin.com/in/n-v-sowmya/

---

*JobScope Analytics — Organising job data. Discovering insights.*
