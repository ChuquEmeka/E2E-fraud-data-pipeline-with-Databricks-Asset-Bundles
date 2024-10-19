# Fraud Detection Pipeline with Delta Live Tables (DLT)

try:
    import dlt
except ImportError:
    class dlt:
        def table(comment, **options):
            def _(f):
                pass
            return _

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, TimestampType, IntegerType, DoubleType, StringType, BooleanType
from pyspark.sql.functions import first
from pyspark.sql import functions as F
# Initialize SparkSession
spark = SparkSession.builder.appName("FraudDetectionDLT").getOrCreate()
# Define schema for the incoming JSON data
base_schema = StructType([
    StructField("TransactionID", StringType(), True),
    StructField("UserID", StringType(), True),
    StructField("TransactionDate", TimestampType(), True),
    StructField("TransactionAmount", DoubleType(), True),
    StructField("TransactionType", StringType(), True),
    StructField("MerchantID", StringType(), True),
    StructField("Currency", StringType(), True),
    StructField("TransactionStatus", StringType(), True),
    StructField("DeviceType", StringType(), True),
    StructField("IP_Address", StringType(), True),
    StructField("PaymentMethod", StringType(), True),
    StructField("SuspiciousFlag", BooleanType(), True),
    StructField("IsFraud", BooleanType(), True),
    StructField("AnomalyScore", DoubleType(), True),
    StructField("Age", IntegerType(), True),
    StructField("Gender", StringType(), True),
    StructField("AccountCreationDate", TimestampType(), True),
    StructField("Location", StringType(), True),
    StructField("LocationCoordinates", StringType(), True),
    StructField("AccountStatus", StringType(), True),
    StructField("DeviceID", StringType(), True),
    StructField("UserProfileCompleteness", DoubleType(), True),
    StructField("PreviousFraudAttempts", IntegerType(), True)
])

# Bronze Table for Raw Fraud Detection Data
@dlt.table(
    comment="Bronze table for raw fraud detection data",
    table_properties={"quality": "bronze"}
)
def br_fraud_detection_raw_data_historical():
    raw_data = spark.readStream \
        .format("cloudFiles") \
        .option("cloudFiles.format", "json") \
        .option("cloudFiles.inferColumnTypes", "true") \
        .option("cloudFiles.rescuedDataColumn", "rescue_col") \
        .load("s3://fraud-detection-raw-data1/year=*/transactions_*.json")
    
    return raw_data

# Silver Table for Transactions Fact
@dlt.table(
    comment="Silver table for fraud detection transactions",
    table_properties={"quality": "silver"}
)
def si_transactions_fact():
    raw_data = dlt.read_stream("br_fraud_detection_raw_data_historical")
    return raw_data.select(
        "TransactionID",
        "UserID",
        "TransactionDate",
        "TransactionAmount",
        "TransactionType",
        "MerchantID",
        "Currency",
        "TransactionStatus",
        "DeviceType",
        "IP_Address",
        "PaymentMethod",
        "SuspiciousFlag",
        "IsFraud",
        "AnomalyScore",
        "Age",
        "Gender",
        "AccountCreationDate",
        "Location",
        "LocationCoordinates",
        "AccountStatus",
        "DeviceID",
        "UserProfileCompleteness",
        "PreviousFraudAttempts"
    ).distinct()

# Silver Table for Users Dimension
@dlt.table(
    name="si_users_dimension",
    comment="Silver quality Users Dimension table",
    table_properties={"quality": "silver"}
)
def si_users_dimension():
    raw_data = dlt.read("br_fraud_detection_raw_data_historical")
    return raw_data.groupBy("UserID").agg(
        first("Age").alias("Age"),
        first("Gender").alias("Gender"),
        first("AccountCreationDate").alias("AccountCreationDate"),
        first("AccountStatus").alias("AccountStatus"),
        first("UserProfileCompleteness").alias("UserProfileCompleteness"),
        first("PreviousFraudAttempts").alias("PreviousFraudAttempts"),
        first("Location").alias("UserLocation")
    )

# Silver Table for Devices Dimension
@dlt.table(
    name="si_devices_dimension",
    comment="Silver quality Devices Dimension table",
    table_properties={"quality": "silver"}
)
def si_devices_dimension():
    raw_data = dlt.read("br_fraud_detection_raw_data_historical")
    return raw_data.groupBy("DeviceID").agg(
        first("DeviceType").alias("DeviceType"),
        first("IP_Address").alias("IP_Address")
    )

# Gold Table for User Behavior Metrics
@dlt.table(
    name="go_user_behavior_metrics",
    comment="Gold quality table for user behavior metrics",
    table_properties={"quality": "gold"}
)
def go_user_behavior_metrics():
    return dlt.read("si_transactions_fact").groupBy("UserID").agg(
        F.count("TransactionID").alias("total_transactions"),
        F.avg("TransactionAmount").alias("avg_transaction_amount"),
        F.count(F.when(F.col("IsFraud") == 1, "TransactionID")).alias("total_fraud_transactions"),
        F.countDistinct("DeviceID").alias("unique_devices"),
        F.max("TransactionDate").alias("last_transaction_date"),
        F.min("TransactionDate").alias("first_transaction_date")
    )

# Gold Table for Merchant Risk Assessment
@dlt.table(
    name="go_merchant_risk_assessment",
    comment="Gold quality table for merchant risk assessment",
    table_properties={"quality": "gold"}
)
def go_merchant_risk_assessment():
    return dlt.read("si_transactions_fact").groupBy("MerchantID").agg(
        F.count("TransactionID").alias("total_transactions"),
        F.count(F.when(F.col("IsFraud") == 1, "TransactionID")).alias("total_fraud_transactions"),
        F.sum(F.when(F.col("IsFraud") == 1, F.col("TransactionAmount")).otherwise(0)).alias("total_fraudulent_amount"),
        F.avg("AnomalyScore").alias("avg_anomaly_score"),
        F.countDistinct("UserID").alias("unique_users")
    )

# Gold Table for Real-time Fraud Detection
@dlt.table(
    name="go_real_time_fraud_detection",
    comment="Gold quality table for real-time fraud detection",
    table_properties={"quality": "gold"}
)
def go_real_time_fraud_detection():
    return dlt.read("si_transactions_fact").filter(
        (F.col("AnomalyScore") > 0.5) | (F.col("IsFraud") == 1)
    ).select(
        "TransactionID",
        "TransactionDate",
        "TransactionAmount",
        "TransactionType",
        "UserID",
        "MerchantID",
        "DeviceID",
        "IP_Address",
        "AnomalyScore",
        "IsFraud",
        F.when(F.col("AnomalyScore") > 0.8, "High Risk")
         .when(F.col("AnomalyScore") > 0.5, "Moderate Risk")
         .otherwise("Low Risk").alias("fraud_risk_level")
    )

# Gold Table for Predictive Model Features
@dlt.table(
    name="go_predictive_model_features",
    comment="Gold quality table for predictive model features",
    table_properties={"quality": "gold"}
)
def go_predictive_model_features():
    transactions_fact = dlt.read("si_transactions_fact")
    user_behavior_metrics = dlt.read("go_user_behavior_metrics")
    merchant_risk_assessment = dlt.read("go_merchant_risk_assessment")
    
    return transactions_fact.join(user_behavior_metrics, transactions_fact.UserID == user_behavior_metrics.UserID, "inner")\
        .join(merchant_risk_assessment, transactions_fact.MerchantID == merchant_risk_assessment.MerchantID, "inner")\
        .select(
            transactions_fact.TransactionID,
            transactions_fact.TransactionAmount,
            transactions_fact.TransactionType,
            transactions_fact.AnomalyScore,
            user_behavior_metrics.total_transactions.alias("user_total_transactions"),
            user_behavior_metrics.avg_transaction_amount.alias("user_avg_transaction_amount"),
            user_behavior_metrics.total_fraud_transactions.alias("user_fraud_transactions"),
            merchant_risk_assessment.total_fraud_transactions.alias("merchant_fraud_transactions"),
            merchant_risk_assessment.avg_anomaly_score.alias("merchant_avg_anomaly_score"),
            transactions_fact.IsFraud
        )

# Gold Table for Fraud Detection Dashboard Metrics
@dlt.table(
    name="go_fraud_detection_dashboard_metrics",
    comment="Gold quality table for reporting and dashboarding metrics",
    table_properties={"quality": "gold"}
)
def go_fraud_detection_dashboard_metrics():
    transactions_fact = dlt.read("si_transactions_fact")
    return transactions_fact.agg(
        F.count("TransactionID").alias("total_transactions"),
        F.sum(F.when(transactions_fact.IsFraud == 1, 1).otherwise(0)).alias("total_fraud_transactions"),
        F.sum(F.when(transactions_fact.IsFraud == 1, transactions_fact.TransactionAmount).otherwise(0)).alias("total_fraudulent_amount"),
        F.countDistinct("UserID").alias("unique_users"),
        F.countDistinct("MerchantID").alias("unique_merchants"),
        F.avg("AnomalyScore").alias("avg_anomaly_score"),
        F.max("TransactionDate").alias("last_transaction_date")
    )
