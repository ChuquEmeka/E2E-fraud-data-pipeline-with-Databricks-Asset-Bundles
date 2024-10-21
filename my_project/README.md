# **Databricks Fraud Detection Pipeline with Asset Bundles**

## **Table of Contents**
- [Project Overview](#project-overview)
- [Free Trial Setup](#free-trial-setup)
- [S3 Access Configuration with Instance Profile](#s3-access-configuration-with-instance-profile)
- [Databricks Asset Bundles for Fraud Detection Pipeline](#databricks-asset-bundles-for-fraud-detection-pipeline)
- [Prerequisites for Activating Databricks Asset Bundles](#prerequisites-for-activating-databricks-asset-bundles)
- [Project Structure](#project-structure)
- [Delta Live Tables (DLT) Lineage Graph for Fraud Detection Pipeline](#delta-live-tables-dlt-lineage-graph-for-fraud-detection-pipeline)
- [Project Cost Breakdown](#project-cost-breakdown-coming-soon)
- [Conclusion](#conclusion-coming-soon)

---

## **1. Project Overview**

This project focuses on developing a robust fraud detection pipeline using **Databricks' Delta Live Tables (DLT)** alongside **Databricks Asset Bundles** for efficient development, packaging, and deployment. The pipeline was built and deployed within the Databricks platform on AWS infrastructure, integrating **Amazon S3** for scalable data storage.

### **Key Highlights:**
- **Technology Stack:** Databricks, Delta Live Tables (DLT), AWS (EC2, S3)
- **Core Functionality:** Fraud detection using a DLT pipeline with automated data lineage tracking and monitoring.
- **Infrastructure:** AWS cloud services for storage and compute, integrating with Databricks for seamless development and deployment.

This documentation outlines the setup process, access configuration, and deployment strategy using Databricks Asset Bundles, along with a cost breakdown of the resources used.

---

## **2. Free Trial Setup**

To begin the project, I took advantage of the **Databricks free trial** through the AWS Marketplace. This trial granted access to Databricks' features for 14 days, allowing me to build, test, and deploy the pipeline within this window.

While the trial covered Databricks usage, AWS charges for the **EC2 instances** used to run Databricks clusters were incurred. These costs, along with other resource usage, will be detailed in the Project Cost Breakdown section.

### **Steps Taken:**
1. Signed up for Databricks via AWS Marketplace.
2. Set up my Databricks workspace linked to my AWS account.
3. Managed compute and storage through the AWS Management Console.
4. Built the fraud detection pipeline within the free trial period, ensuring efficient resource use.
5. Monitored AWS EC2 instance costs closely, with a detailed breakdown to follow in the cost section.

---

## **3. S3 Access Configuration with Instance Profile**

To enable secure access between the Databricks clusters and **Amazon S3**, I followed a comprehensive guide to configure **S3 Access** using an **EC2 Instance Profile**. This setup ensured seamless data reading and writing from S3, while maintaining strict access controls.

### **Key Steps:**
1. **Create an IAM Role:** Configured a role with the necessary S3 permissions (read, write, delete).
2. **Set up an Instance Profile:** Attached the IAM role to an EC2 Instance Profile.
3. **Configure Databricks Cluster:** Linked the Instance Profile to the Databricks cluster, granting access to S3.
4. **Add Instance Profile to Databricks:** Included the instance profile ARN in Databricks settings for full S3 access.

For more information, refer to the official [Databricks documentation on S3 Access with Instance Profiles](https://docs.databricks.com/administration-guide/cloud-configurations/aws/instance-profiles.html).

---

## **4. Databricks Asset Bundles for Fraud Detection Pipeline**

This section outlines how **Databricks Asset Bundles** were utilized for packaging and deploying the fraud detection pipeline. The use of **Delta Live Tables (DLT)** enabled efficient, scalable, and fault-tolerant data processing while ensuring clear data lineage.

### **Key Highlights:**
- **Easy Packaging:** Databricks Asset Bundles packaged the entire fraud detection pipeline, including notebooks, Python scripts, and configuration files, making deployment seamless.
- **Automated Deployment:** The pipeline was deployed in both development and production environments using CI/CD processes (via GitHub workflows).
- **Data Processing with DLT:** Databricks' Delta Live Tables were used to create a multi-tiered data pipeline based on the **Medallion Architecture**:
  - **Bronze Layer:** Ingested raw transaction data into Databricks from Amazon S3.
  - **Silver Layer:** Cleaned and structured the data into fact and dimension tables.
  - **Gold Layer:** Aggregated and transformed the data into business-level insights, such as user behavior metrics, merchant risk assessments, and real-time fraud detection.

---

## **5. Prerequisites for Activating Databricks Asset Bundles**

Before working with **Databricks Asset Bundles**, several key steps and installations are required:

### **Key Steps:**

1. **Install Databricks CLI**: Install the Databricks CLI using WinGet on Windows to manage Databricks bundles:
    ```bash
    winget search databricks
    winget install Databricks.DatabricksCLI
    ```
    After installation, restart the Command Prompt and verify the installation using:
    ```bash
    databricks -v
    ```

2. **Initialize the Databricks Bundle**: Navigate to the project directory and initialize the bundle:
    ```bash
    databricks bundle init
    ```

3. **Retrieve and Export Bundle Schema**: Retrieve the schema of the Databricks bundle and save it to a configuration file:
    ```bash
    databricks bundle schema --profile databricks
    databricks bundle schema > bundle_config_schema.json
    ```

4. **Validate and Deploy the Bundle**: Validate and deploy the Databricks bundle:
    ```bash
    databricks bundle validate --profile databricks
    databricks bundle deploy --profile databricks
    ```

5. **Run the Job**: Execute the fraud detection pipeline by running the Databricks job:
    ```bash
    databricks bundle run my_project_job --profile databricks
    ```

This process ensures a smooth and automated deployment of the entire fraud detection pipeline across environments.

---

## **6. Project Structure**

The project structure was designed to keep everything organized for easy development, testing, and deployment using **Databricks Asset Bundles**. Below is the structure of the project:

```bash
DAB/
│
├── .github/
│   └── workflows/
│       ├── prod_deployment.yml    # Deployment to production
│       └── qa_deployment.yml      # Deployment to QA environment
│
├── databricks-env/                 # Environment-specific configurations for Databricks
│
├── my_project/
│   ├── .databricks/               # Databricks-specific settings
│   ├── .pytest_cache/             # Cached pytest results
│   ├── .vscode/                   # Visual Studio Code configurations
│   ├── build/                     # Build artifacts
│   ├── dist/                      # Distribution files for the project
│   ├── fixtures/                  # Test fixtures for unit testing
│   ├── resources/
│   │   ├── my_project.job.yml      # Job definition for Databricks
│   │   └── my_project.pipeline.yml # Pipeline definition for DLT
│   └── scratch/                   # Temporary or intermediate work
│
├── src/
│   ├── my_project/                # Core project source code
│   │   ├── __init__.py            # Project initialization file
│   │   ├── fraud_detection_data_python.py # Python script for data transformation
│   │   └── main.py                # Main script for running the project
│   ├── dashboard_metrics.ipynb    # Jupyter notebook for metrics generation
│   └── fraud-detection-data-python.ipynb # Notebook defining the DLT pipeline
│
├── tests/
│   └── (Unit tests for validating the project components)
│
├── .gitignore                     # Specifies files to be ignored by version control
├── databricks.yml                 # Core configuration for Databricks bundle
├── pytest.ini                     # Pytest configurations for running unit tests
├── README.md                      # Project documentation and instructions
├── requirements-dev.txt           # Development dependencies (e.g., testing libraries)
└── setup.py                       # Script for building and packaging the project

## **7. Delta Live Tables (DLT) Lineage Graph for Fraud Detection Pipeline**

The attached graph shows the **lineage** of the Delta Live Tables (DLT) pipeline, outlining the flow of data between tables and views in the fraud detection pipeline. This graph visually represents how data is processed and transformed as it moves from upstream raw data to downstream aggregated views and metrics.

---

### **Data Flow Explanation (Upstream to Downstream)**

1. **br_fraud_detection_raw_data_historical (Streaming Table)**
   - **Upstream Data Source**: This is the first stage of the pipeline, representing the **Bronze Layer** where raw fraud detection data is ingested. It streams from external sources (such as S3) and is loaded into the pipeline as a streaming table.
   - **Purpose**: Stores raw, unprocessed transaction data, which will later be cleaned and structured in the Silver layer.

2. **si_transactions_fact (Streaming Table)**
   - **Downstream from**: `br_fraud_detection_raw_data_historical`
   - **Silver Layer**: This table is derived from the raw data and serves as a **fact table** for transactions.
   - **Purpose**: Structured transaction data, with unnecessary fields removed and transformations applied. This central fact table is used by multiple downstream views and tables.

3. **si_users_dimension, si_devices_dimension (Materialized Views)**
   - **Downstream from**: `br_fraud_detection_raw_data_historical`
   - **Silver Layer**: These dimension tables capture user and device details by grouping and aggregating relevant fields from the raw data.
   - **Purpose**:
     - **si_users_dimension**: Stores aggregated user-level information like age, gender, and account status.
     - **si_devices_dimension**: Stores device-related information such as device type and IP address.

4. **go_user_behavior_metrics, go_merchant_risk_assessment, go_real_time_fraud_detection, go_predictive_model_features, go_fraud_detection_dashboard_metrics (Materialized Views)**
   - **Downstream from**: `si_transactions_fact`, `si_users_dimension`, and `si_devices_dimension`
   - **Gold Layer**: These views produce **business-level insights** derived from fact and dimension tables.
   
   - **Purpose**:
     - **go_user_behavior_metrics**: Aggregates data from `si_transactions_fact` to calculate user behavior metrics, such as total transactions, average transaction amount, and fraud detection flags.
     - **go_merchant_risk_assessment**: Evaluates merchant risk by analyzing the number of fraudulent transactions, total fraud amount, and anomaly scores for each merchant.
     - **go_real_time_fraud_detection**: Filters real-time transactions to identify high-risk transactions based on anomaly scores and fraud flags.
     - **go_predictive_model_features**: Aggregates metrics from transaction, user, and merchant data to create features for predictive fraud models.
     - **go_fraud_detection_dashboard_metrics**: Aggregates key metrics for the fraud detection dashboard, displaying fraud statistics such as total transactions, fraud transactions, and the fraudulent amount.

---

### **Summary of Data Flow**

- **Upstream Tables (Bronze Layer)**: The pipeline begins with `br_fraud_detection_raw_data_historical`, streaming raw data into the pipeline.
- **Intermediate Tables (Silver Layer)**: Raw data is processed into structured transaction data (`si_transactions_fact`), and dimension tables (`si_users_dimension`, `si_devices_dimension`) are created.
- **Downstream Views (Gold Layer)**: Silver-layer tables generate meaningful insights like user behavior (`go_user_behavior_metrics`), merchant risk (`go_merchant_risk_assessment`), real-time fraud detection (`go_real_time_fraud_detection`), and predictive model features, culminating in **dashboard metrics** (`go_fraud_detection_dashboard_metrics`).

Each layer of the pipeline—**Bronze**, **Silver**, and **Gold**—refines and enriches the data, producing actionable insights for **real-time fraud detection**, **risk assessments**, and **dashboard reporting**.  
  
## **8. Unity Catalog Setup for Fraud Detection Pipeline**

In this project, I used **Databricks Unity Catalog** to manage the datasets created by the fraud detection pipeline. The pipeline adheres to the **Medallion Architecture** (Bronze, Silver, and Gold layers) to organize data at different stages of transformation.

While developing, I used the **same workspace** for both development and production environments as part of an experimental setup. Ideally, separate workspaces should be used for development and production to ensure better isolation and governance.

---

### **Development and Production Catalogs**

1. **Development Catalog: `my_project_dev`**
   - In the `my_project_dev` catalog, I developed and tested the tables and views that form the core of the pipeline. This catalog includes the following layers:
   
   - **Bronze Layer**:
     - **br_fraud_detection_raw_data_historical**: Stores raw, streaming fraud detection data.
   
   - **Silver Layer**:
     - **si_transactions_fact**, **si_users_dimension**, **si_devices_dimension**: Structured data on transactions, users, and devices.
   
   - **Gold Layer**:
     - **go_user_behavior_metrics**, **go_merchant_risk_assessment**, **go_real_time_fraud_detection**, **go_predictive_model_features**, **go_fraud_detection_dashboard_metrics**: Aggregated, business-ready views providing insights into user behavior, merchant risk, real-time fraud detection, and predictive modeling.
   
   This environment allowed me to iterate and validate transformations before moving to production.

2. **Production Catalog: `my_project_prod`**
   - Once the development pipeline was validated, the same pipeline was deployed to the `my_project_prod` catalog. This structure mirrors the development catalog but is intended for finalized, production-ready data.
   
   - **Production Layers**: The production catalog contains the same Bronze, Silver, and Gold layers with the same set of tables and views, ensuring consistency between development and production environments.

---

### **Conclusion**

Although I used the **same workspace** (`emeka_data_science_and_engineering_workspace`) for both development and production environments as part of an experiment, this is **not ideal**. Typically, separate workspaces should be used to ensure proper isolation. However, by using **separate catalogs** (`my_project_dev` and `my_project_prod`) within the same workspace, I was able to simulate the separation of development and production environments.

This setup allowed for effective data governance, even within the constraints of using a single workspace.

