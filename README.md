# shopping-cart

![Version](https://img.shields.io/static/v1.svg?label=Version&message=0.1.0&color=blue&logo=github)
![Python](https://img.shields.io/static/v1.svg?label=Python&message=^3.12.2&color=blue&logo=python)
![Poetry](https://img.shields.io/static/v1.svg?label=Poetry&message=^1.8.4&color=blue&logo=poetry)
![FastAPI](https://img.shields.io/static/v1.svg?label=FastAPI&message=^0.115.4&color=blue&logo=FastAPI)
![Boto3](https://img.shields.io/static/v1.svg?label=Boto3&message=^1.35.54&color=blue&logo=amazonwebservices)
[![Tests Status](./docs/tests/badges/tests-badge.svg?dummy=8484744)](./docs/tests/coverage/html/index.html)
[![Coverage Status](./docs/tests/badges/coverage-badge.svg?dummy=8484744)](./docs/tests/coverage/html/index.html)

# Backend for a Shopping Cart Microservice

This project implements the backend for a shopping cart microservice, designed to process purchase transactions securely, resiliently, and at scale. The architecture uses AWS services to ensure reliable data storage and asynchronous processing, with monitoring and alerts in case of failures. The solution includes a layered Data Lake for data analytics, with quality and governance policies in place.

## System Architecture

![Architecture](https://github.com/willrockoliv/shopping-cart/blob/main/docs/architecture.png)

*to see the above diagram with more details, you can open it directly in [Excalidraw](https://excalidraw.com/), just import the [image](https://github.com/willrockoliv/shopping-cart/blob/main/docs/architecture.png) or the [.excalidraw](https://github.com/willrockoliv/shopping-cart/blob/main/docs/architecture.excalidraw) file*

### Operational Flow

1. **Client Request**
   - The client sends an HTTP request with purchase details (`buyer_id`, `product_id`, `number_of_installments`, `total_amount`, `purchase_date`) to the shopping cart API.

2. **Shopping Cart API**
   - The API, built with **FastAPI**, is hosted on an **AWS Lambda** function, and the code is versioned on **GitHub**, using the **GitHub Actions** as CI/CD for deployment.
   - This API processes the request and sends the purchase data to an **Amazon SNS** topic for asynchronous processing.
   - Then, the message is sent to an **Amazon SQS** queue subscribed to this SNS topic.

3. **Processing with AWS Lambda**
   - Other **AWS Lambda** function, also with the code versioned on GitHub, consumes messages from SQS, processing each transaction and storing the data in **Amazon DynamoDB** for fast and scalable storage.

4. **Data Persistence in DynamoDB**
   - **Amazon DynamoDB** stores the transaction data, ensuring scalability and low latency for read and write operations.

5. **Fallback with Dead Letter Queue (DLQ)**
   - If a message fails to be processed, the **DLQ** in SQS stores failed messages, ensuring no transaction is lost.

6. **Monitoring and Alerts**
   - **Amazon CloudWatch** monitors the Lambda, SQS, and DynamoDB operations. For critical errors, **SNS (Simple Notification Service)** sends alerts to notify stakeholders.

### Data Lake and Medallion Architecture Layers

To implement the **Medallion Architecture** (Bronze, Silver, and Gold layers) an **Airflow** is used for orchestrate the data journey through these layers, ensuring data quality and scalability for analytics.

1. **Bronze Layer:** A scheduled DAG will run periodically extracting new records in DynamoDB and stores raw data (JSON Files) in a **S3 Bucket**, partitioning by `year/month/day/hour/`, using the [`DynamoDBToS3Operator()`](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/transfer/dynamodb_to_s3.html).

2. **Silver Layer:**
    - Performs transformations (such as data cleaning and enrichment) using **Spark** and **Amazon EMR** clusters, orchestrated by a DAG using [EMR Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/emr/emr.html).
    - The datasets are written partitioned in S3 buckets in **parquet** file format.
    - A **quality gate** is applied to check data quality using libraries like [SODA](https://www.soda.io/) or [Great Expectations](https://greatexpectations.io/), before moving to the next layer.
    - The Silver layer also uses a **Glue Crawler** to catalog the metadata in the **Glue Data Catalog** (or [Amundsen](https://www.amundsen.io/)).

3. **Gold Layer:**
    - Performs aggregations also using **Spark** and **Amazon EMR** clusters, orchestrated by a DAG using [EMR Operators](https://airflow.apache).
    - The aggregated datasets are written partitioned in S3 buckets in **parquet** file format, ready for analysis.
    - An additional **quality gate** is applied after dataset generation in this layer, ensuring that only high-quality data is available for analytics.
    - And also uses the **Glue Crawler** to catalog in **Glue Data Catalog**.

4. **Data Contract:** Formalizes data quality and structure expectations across layers, ensuring consistency and governance between the Data Producers and Data Consumers in the company.
        - Reference:
            - https://www.datamesh-manager.com/
            - https://datacontract.com/ 


4. **Data Contract:** Formalizes data quality and structure expectations across layers, ensuring consistency and governance between the Data Producers and Data Consumers in the company.
    - Reference:
        - https://www.datamesh-manager.com/
        - https://datacontract.com/

## Technologies Used

- **Python** with FastAPI for implementing the shopping cart API.
- **Amazon SNS** and **SQS** for the asynchronous message queue.
- **AWS Lambda** to process messages and store data.
- **DynamoDB** for NoSQL storage of transaction data.
- **AWS CloudWatch** and **SNS** for monitoring and alerts.
- **Apache Airflow** for data pipeline orchestration
- **S3 Buckets** for storage
- **Apache Spark** for distributed data processing
- **AWS Glue** (**Crawler** and **Catalog**) for metadata management.
- **Quality Gates** libraries for data validation in the Silver and Gold pipelines.
    - [SODA](https://www.soda.io/)
    - [Great Expectations](https://greatexpectations.io/)
- **Data Contracts** for consistency and governance between the Data Producers and Data Consumers in the company.
- **Medallion architecture** (Bronze, Silver, and Gold layers).

## Configuration Requirements

- Python ^3.12.2
- Poetry ^1.8.4

## Installation

run:
```bash
poetry install
```

## Running the Project

1. Configure environment variables for authentication and access permissions to AWS.
2. Configure the `.env` file on root with:
    - `SNS_TARGET_ARN="arn:aws:sns:us-east-2:00000000000:MyTopic"`

3. run:
```bash
task run
```

## Running tests

3. run:
```bash
task test
```
