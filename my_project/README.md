# **Databricks Fraud Detection Pipeline with Asset Bundles**

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Free Trial Setup](#free-trial-setup)
3. [S3 Access Configuration with Instance Profile](#s3-access-configuration-with-instance-profile)
4. [Databricks Asset Bundles for Fraud Detection Pipeline](#databricks-asset-bundles-for-fraud-detection-pipeline)
5. [Prerequisites for Activating Databricks Asset Bundles](#prerequisites-for-activating-databricks-asset-bundles)
6. [Project Structure](#project-structure)
7. [Delta Live Tables (DLT) Lineage Graph for Fraud Detection Pipeline](#delta-live-tables-dlt-lineage-graph-for-fraud-detection-pipeline)
8. [Unity Catalog Setup for Fraud Detection Pipeline](#unity-catalog-setup-for-fraud-detection-pipeline)
9. [CI/CD Deployment Workflows](#cicd-deployment-workflows)
10. [Project Cost Breakdown](#project-cost-breakdown-coming-soon)
11. [Conclusion](#conclusion-coming-soon)

---

## **1. Project Overview**

This project focuses on developing a robust fraud detection data pipeline using **Databricks' Delta Live Tables (DLT)** alongside **Databricks Asset Bundles** for efficient development, packaging, and deployment. The pipeline was built and deployed within the Databricks platform on AWS infrastructure, integrating **Amazon S3** for scalable data storage.

### **Key Highlights:**
- **Technology Stack:** Databricks, Delta Live Tables (DLT), AWS (EC2, S3)
- **Core Functionality:** Fraud detection using a DLT pipeline with automated data lineage tracking and monitoring.
- **Infrastructure:** AWS cloud services for storage and compute, integrating with Databricks for seamless development and deployment.

This documentation outlines the setup process, access configuration, and deployment strategy using Databricks Asset Bundles, along with a cost breakdown of the resources used.

---

## **2. Free Trial Setup**

Professionally, I have been using Databricks platform for over two years, but to begin this private project, I took advantage of the **Databricks free trial**. This trial granted access to Databricks' features for 14 days, allowing me to build, test, and deploy the pipeline within this window.

### Setting Up My Databricks Free Trial

To begin using **Databricks**, I signed up for the **free trial** by following these steps:

1. **Sign Up**:
   - I navigated to the **Try Databricks** page.
   - I entered my name, company, email, and title, then clicked **Continue**.

2. **Cloud Provider Selection**:
   - I selected **Amazon Web Services (AWS)** as my cloud provider and clicked **Get started**.

3. **Trial Information**:
   - I noted that the Databricks trial was free, but I needed an active AWS account since Databricks utilized compute and storage resources within AWS.

4. **Email Verification**:
   - I looked for the welcome email and clicked the link to verify my email address.

5. **Account Setup**:
   - After verification, I was redirected to the **Databricks account console**, where I set up my Databricks account and created a workspace.

**Note**: While the trial period was free, I had the option to upgrade at any time by providing my credit card information.


---  
## **Raw Data Generation**

This **[fraud-detection-raw-data.py](./raw_data_simulation/fraud-detection-raw-data.py)** file generates **synthetic user and transaction data** raw data for this project and uploads it to **Amazon S3**.

- **Purpose**: To create realistic **user and transaction records** for testing fraud detection algorithms.
- **Output**: **JSON files** stored in **S3**, partitioned by year.  
### **Key Features**

- **User Data**: Generates profiles for **1,000 users** with attributes like `UserID`, `Age`, `Gender`, and `Account Creation Date`.
  
- **Transaction Data**: Creates **15,000 transaction records** including `TransactionID`, `Amount`, `Type`, `Merchant`, and fraud indicators (`IsFraud`).
  
- **Data Merging**: Combines **user and transaction data** for comprehensive datasets.

- **AWS Integration**: Uses **Boto3** to upload generated data to a specified **S3 bucket**.  
![ER](output_images/S3_bucket.png)

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
    After installation, I restarted my computer and verified the installation using:
    ```bash
    databricks -v
    ```

2. **Authenticate Databricks Workspace**: Once the **Databricks CLI** is installed, authenticate your **Databricks workspace** to enable the CLI to interact with the workspace for deployments.

    ### **Steps to Authenticate**:
    1. **Generate an Access Token**:
       - In Databricks, navigate to **Settings > User Settings > Access Tokens** and generate a new access token.
    2. **Configure Workspace Profile**:
       - Use the following command to configure your workspace profile with the generated token:
         ```bash
         databricks configure --
         ```
       - When prompted, enter your **Databricks Host URL** and the **Access Token**.

    This step ensures **secure communication** between the **Databricks CLI** and your **Databricks workspace**, allowing the CLI to execute commands for deployments.

3. **Initialize the Databricks Bundle**: Navigate to the project directory and initialize the bundle:
    ```bash
    cd my_project
    databricks bundle init
    ```

4. **Retrieve and Export Bundle Schema**: Retrieve the schema of the Databricks bundle and save it to a configuration file:
    ```bash
    databricks bundle schema --profile databricks
    databricks bundle schema > bundle_config_schema.json
    ```

5. **Validate and Deploy the Bundle**: Validate and deploy the Databricks bundle:
    ```bash
    databricks bundle validate --profile databricks
    databricks bundle deploy --profile databricks
    ```

6. **Run the Job**: Execute the fraud detection pipeline by running the Databricks job:
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
 ``` 
  
## **7. Delta Live Tables (DLT) Lineage Graph for Fraud Detection Pipeline**

The attached graph shows the **lineage** of the Delta Live Tables (DLT) pipeline, outlining the flow of data between tables and views in the fraud detection pipeline. This graph visually represents how data is processed and transformed as it moves from upstream raw data to downstream aggregated views and metrics as defined in [fraud_detection_data_python.py](./src/my_project/fraud_detection_data_python.py) transformation dlt pipeline script.  
![ER](output_images/dlt_pipeline_lineage_graph.png)  
  
## **Job and Pipeline Flow**

This section details the **job configuration** and **pipeline setup** for automating the daily execution of the fraud detection pipeline and the subsequent calculation of metrics.

---

### **Job Configuration ([my_project.job.yml](./resources/my_project.job.yml))**

The `my_project.job.yml` file defines the configuration for a **Databricks job** that automates the daily execution of the fraud detection pipeline.

- **Job Name**: `fraud_detection_job`
- **Trigger**: Runs every day with a 24-hour interval between runs.
- **Email Notifications**: Sends failure notifications to `nweke.edeh@gmail.com`.
- **Tasks**:
  - **Task 1 (`refresh_pipeline`)**: Refreshes the fraud detection pipeline using the pipeline ID from `my_project.pipeline.yml`.
  - **Task 2 (`fraud_metrics`)**: Depends on the `refresh_pipeline` task and runs the `dashboard_metrics.ipynb` notebook to compute and collect fraud detection metrics after the pipeline has refreshed.  
![ER](output_images/job_lineage_graph.png) 
- **Cluster Configuration**:
  - **Autoscaling Spark Cluster**: Configured with a minimum of 1 worker and a maximum of 4 workers, running **Spark version 15.4.x with Scala 2.12**.
  - **AWS Instance Profile**: Uses an AWS instance profile for secure access to AWS services like **S3**.

---

### **Pipeline Configuration ([my_project.pipeline.yml](./resources/my_project.pipeline.yml))**

The `my_project.pipeline.yml` file defines the **Databricks Delta Live Tables (DLT) pipeline** that processes the fraud detection data.

- **Pipeline Name**: `fraud_detection_data_pipeline`
- **Unity Catalog Integration**: Targets the `emeka_data_science_and_engineering_workspace` and dynamically applies the appropriate target schema based on the environment (`my_project_${bundle.environment}`).
- **Notebook as Library**: Uses the `fraud-detection-data-python.ipynb` notebook to perform data transformation and processing, moving data through the **Bronze**, **Silver**, and **Gold layers**.
- **Pipeline Configuration**: Dynamically references project source files using `bundle.sourcePath`, ensuring that the right resources are deployed in the appropriate environment.


---

### **Data Flow Explanation (Upstream to Downstream)**  
#### Table Naming Conventions

In the **Fraud Detection Data Pipeline**, prefixes indicate the layer of the tables:  
- **`br_`** for **Bronze Layer** tables (raw data),  
- **`si_`** for **Silver Layer** tables (structured data), and  
- **`go_`** for **Gold Layer** views (business insights).  

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
![ER](output_images/unity_catalog.png) 

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

Although I used the **same workspace** (`emeka_data_science_and_engineering_workspace`) for both development and production environments as part of an experiment, this is **not ideal**. Typically, separate workspaces should be used to ensure proper isolation. However, by using **separate catalogs** (`my_project_dev` and `my_project_prod`) within the same workspace, I was able to simulate the separation of development and production environments.

This setup allowed for effective data governance, even within the constraints of using a single workspace.  
  
## **9. CI/CD Deployment Workflows**

This project utilizes **GitHub Actions** workflows for **CI/CD deployment** to both development and production environments. The workflows are configured for seamless deployment of the fraud detection pipeline using **Databricks Asset Bundles**.
![ER](output_images/job_git_action_workflow.png)   
---

### **QA Deployment Configuration ([qa_deployment.yml](./.github/workflows/qa_deployment.yml))**

This GitHub Actions workflow handles the CI/CD deployment to the **development environment (QA)**. It is triggered by a push to the `update-pipeline` branch, but the trigger can be customized for other organizational workflows, such as pull requests or other events.

#### **Workflow Steps:**

1. **Deploy Bundle to Dev (QA)**:
   - **Trigger**: Initiated by a push to the `update-pipeline` branch, but can be modified for other events.
   - **Authentication**: Creates a `~/.databrickscfg` file using secrets for Databricks authentication.
   - **Databricks CLI Setup**: Installs the Databricks CLI for deployment.
   - **Deployment**: Deploys the bundle to the development environment using the `databricks.yml` file.

2. **Run Pipeline Update for Dev (QA)**:
   - **Execution**: After deployment, the job (`my_project_job`) is run to refresh the pipeline in the QA environment.
   - **Authentication and CLI Setup**: Repeats authentication and CLI setup steps.
   - **Job Execution**: Executes the job to ensure the pipeline is updated with the latest data.

---

### **Production Deployment Workflow ([prod_deployment.yml](./.github/workflows/prod_deployment.yml))**

This GitHub Actions workflow manages the deployment to the **production environment**. It is triggered by a push to the `master` branch but can be configured for other triggers based on organizational requirements.  
![ER](output_images/prod_deplo_workflow.png)

#### **Workflow Steps:**

1. **Deploy Bundle to Prod**:
   - **Trigger**: Activated by a push to the `master` branch, with options for other event types.
   - **Authentication**: Creates the `~/.databrickscfg` file using secrets for secure access.
   - **Databricks CLI Setup**: Installs the Databricks CLI to handle deployments.
   - **Deployment**: Deploys the bundle to the production environment using the `databricks.yml` file.

2. **Run Pipeline Update for Prod**:
   - **Execution**: Following deployment, the job (`my_project_job`) is executed to refresh the production pipeline.
   - **Authentication and CLI Setup**: Similar steps for authentication and CLI installation.
   - **Job Execution**: Runs the job to update the pipeline with current data.

---

### **Key Points**

- **Adjustable Triggers**: The workflows can be tailored to trigger on various events, such as pull requests or manual deployments, according to team practices.
- **Streamlined Process**: Both workflows maintain a consistent process for authentication, deployment, and job execution, ensuring efficient CI/CD management for both development and production environments.  


  

## **10. Project Cost Breakdown**

This section details the **costs incurred** during the development and deployment of the fraud detection pipeline. Although I utilized the **Databricks free trial** for the project, I incurred the following costs from **AWS**:

- **AWS EC2 Instance Usage**: Charges incurred for running Databricks clusters configured on **EC2 instances**.
- **S3 Storage Costs**: Costs associated with storing **raw and processed data** for the pipeline in **Amazon S3**.
- **Databricks Charges**: These charges will be incurred after the **free trial ends** for any continuous job execution.

The detailed breakdown will provide insights into **managing cloud costs** effectively while **scaling the project**.  
![ER](output_images/cost.png)  
![ER](output_images/cost2.png)  

## **11. Data Governance**

To ensure **data integrity**, **security**, and **compliance** , a data governance framework is applied, covering various aspects of data lifecycle management.

---

### **Key Data Governance Measures**

1. **Access Control and Security**:
   - **Role-Based Access Control (RBAC)**: Implement **Unity Catalog** in Databricks to manage access to data at the catalog, schema, and table levels, with role-specific permissions for development and production environments.
   - **AWS IAM Policies**: Use **AWS IAM** to control access to **S3** buckets, ensuring only authorized services and users can read/write data.

2. **Data Quality and Validation**:
   - **Delta Live Tables (DLT) Expectations**: Apply **data quality rules** using DLT to validate data during ingestion (e.g., non-null checks, value range enforcement).
   - **Validation Checks**: Include data validation tests in the **QA deployment workflow** to ensure the accuracy and completeness of data before deployment.
   - Due to time constraints, data quality and validation checks, as well as **unit tests**, were not fully implemented in this project. However, I implement **data quality rules, validation checks, and unit tests**      professionally, including non-null checks, value range enforcement, and comprehensive tests to ensure accuracy and completeness.

3. **Data Lineage and Documentation**:
   - **Automated Lineage Tracking**: Use **Delta Live Tables** to automatically generate data lineage for tracking transformations from raw data (Bronze) to aggregated views (Gold).
   - **Documentation**: Maintain detailed documentation of tables, transformations, and pipeline configurations for transparency. 

---

This data governance approach ensures secure, compliant, and high-quality data handling throughout the **Fraud Detection Data Pipeline**.


## **12. Overall Project Summary: Fraud Detection Data Pipeline**

The **Fraud Detection Data Pipeline** utilizes **Databricks Delta Live Tables (DLT)** and **Databricks Asset Bundles** to create an efficient solution for detecting fraudulent transactions, structured using the **Medallion Architecture** (Bronze, Silver, and Gold layers).

---

### **Key Highlights**

- **Efficient Packaging and Deployment**: **Databricks Asset Bundles** streamlined the deployment process across both development (`my_project_dev`) and production (`my_project_prod`) environments, enabling easy version control and consistent setup.
  
- **Job Integration**: Added a **job task** to automate pipeline execution, ensuring the reliable processing of data.

- **CI/CD Workflows**: Established CI/CD workflows (`qa_deployment.yml` and `prod_deployment.yml`) to automate deployment and updates, triggered by changes to designated branches.

---






