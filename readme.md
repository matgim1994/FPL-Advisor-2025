# FPL Advisor 2025
![Logo](misc/FPL_Advisor_2025.png)\
**Please be informed that this app is still in progress therefore it's usage is limited.**

**FPL Advisor** is a robust, Python-based data tool designed to build and maintain a structured PostgreSQL database using the most up-to-date data from the official Fantasy Premier League API via a simple CLI.

## 🛠 Prerequisites

* **Docker:** Used for containerizing the PostgreSQL database instance.
* **Python (3.11.2 or newer)**

## ⚙️ Installation Guide

Follow these steps to set up the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/matgim1994/FPL-Advisor-2025.git
    ```

2.  **Setup Python Environment:**
    ```bash
    # Create and activate virtual environment
    python3 -m venv env
    source env/bin/activate 
    
    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    * Create a `.env` file based on the provided `.envexample` template.
    * **Note:** You do not need to create the PostgreSQL database manually. The credentials specified in the `.env` file will be used by Docker Compose to initialize and configure the database instance automatically.

4.  **Initialize Database with Docker:**
    ```bash
    docker compose up -d
    ```
    This command starts the PostgreSQL container, making the database accessible.

5.  **Run Update:**
    ```bash
    python3 fpl.py -u
    ```
    This command performs the initial setup, including fetching the latest full data batch from the FPL API and running the initial data transformation.
    Later, when all necessary database objects are created, you can use it as main data update function.
    
## ⚡️ Application Usage and Commands

All operations are executed via the main script, `fpl.py`. Use the help command to see the full list of options.

### Key Commands

| Command | Description |
| :--- | :--- |
| `python3 fpl.py -h` | Displays **help documentation** and all available CLI arguments. |
| `python3 fpl.py -u` | **Update** Performs initial database creation, raw data ingestion, and full transformation. |
| `python3 fpl.py -ur` | **Update Raw Data.** Downloads a new, complete batch of raw data from the FPL API. The application includes the script run date in the `ingestion_time` column for tracking and auditability. |
| `python3 fpl.py -rd` | **Run Data Transformations.** Executes the dbt models, updating data across the `bronze`, `silver`, and `gold` schemas. This step also runs **data quality tests** defined within dbt against the transformed data. |

## 📊 PostgreSQL Data Architecture (Medallion Structure)

The database implements a robust data architecture, separating data into distinct schemas for quality, transformation, and reporting purposes.

| Schema | Description | Purpose & Tools |
| :--- | :--- | :--- |
| `raw` | Core data fetched directly from the FPL API. Data is **validated by Pydantic** upon ingestion to ensure structural integrity and prevent schema drift. | **Landing Zone**  |
| `bronze` | Newest data loaded from the `raw` schema. Data is validated but there are no major transormations at this stage. Data is stored as SCD2 using dbt snapshots.| **Standardized Data**|
| `silver` | Cleaned, structured, and integrated data. Raw data is organized into new objects prepared for later transformations into gold schema. | **Data Integration** |
| `gold` | Final, application-ready data. Contains aggregated tables and calculated metrics optimized for BI reporting and custom application features. | **App Ready Data** |

## 🏗️ dbt

The data transformation layer relies on **dbt**. All logic for moving data from the `bronze` layer through `silver` to the final `gold` schema is defined in dbt models.

* **Project Location:** All dbt models, tests, and configuration files are located in the `fpl_dbt` directory.
* **Testing:** Data quality is maintained by comprehensive dbt tests executed during the `-rd` command.

For complete, interactive documentation of the data flow, models, column definitions, and tests, please follow these steps:

1.  **Generate Documentation Artifacts:** Ensure you have the latest project metadata by running:
    ```bash
    dbt docs generate
    ```
2.  **Serve Documentation Site:** Start the local web server to view the interactive documentation:
    ```bash
    dbt docs serve
    ```

## 🔮 Roadmap and Future Development

As FPL Advisor is under active development, there are several key features planned to enhance its functionality:

| Feature | Description | Status |
| :--- | :--- | :--- |
| **API** | Implementing a production-ready API using FastAPI to serve data from the `gold` schema. | In Progress |
| **Gold Layer Enrichment** | Extracting further analytical insights from the `silver` layer. | In Progress |
| **Automated Scheduling** | Implementing orchestration using Airflow to automate the data flow. | Planned |
| **Web Interface** | Development of a lightweight web interface for easy data visualization and recomendations. | Planned |
| **External Data Sources** | Integrating secondary data sources (e.g., shots on target, final third touches) to enrich official FPL data. | Planned |

## 🚨 Known Issues

Before opening a new issue, please check the following list of known problems:

* **Issue:** The `silver` layer contains significantly more data/tables than the `gold` layer.
    * **Answer:** This is intentional at the current stage. The `gold` layer enrichment is an ongoing process. Please refer to the **Roadmap** section for planned updates.
* **Issue:** There is no API to query the data directly.
    * **Answer:** Implementing a REST API is the next major feature planned for development. See the **Roadmap** section for the status of the **API** integration.
* **Issue:** Application logs are stored separately from dbt logs.
    * **Answer:** I'm still looking for a best solution for logging in this app.

## 📜 License and Contact

### License

This project is licensed under the GPL v3 License.

### Contact

If you have any questions, suggestions, or need support, please reach out via github.