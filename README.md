# shopping-cart

![version](https://img.shields.io/static/v1.svg?label=version&message=0.1.0&color=blue&logo=github)

Backend for a Shopping Cart Microservice

![Architecture](https://github.com/willrockoliv/shopping-cart/blob/main/docs/architecture.png)

# Backend for a Shopping Cart Microservice

This project implements the backend for a shopping cart microservice, designed to process purchase transactions securely, resiliently, and at scale. The architecture uses AWS services to ensure reliable data storage and asynchronous processing, with monitoring and alerts in case of failures. The solution includes a layered Data Lake for data analytics, with quality and governance policies in place.

## System Architecture

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

The system uses a **Data Lake** with a Medallion architecture (Bronze, Silver, and Gold layers) to ensure data quality and prepare it for analytics.

1. **Bronze Layer**
   - Stores raw transaction data.

2. **Silver Layer**
   - Performs transformations (such as data cleaning and enrichment). After generating datasets, a **quality gate** is applied to check data quality (using libraries like [SODA](https://www.soda.io/) or [Great Expectations](https://greatexpectations.io/)) before moving to the next layer. The Silver layer also uses a **Glue Data Catalog** for metadata management (or [Amundsen](https://www.amundsen.io/)).

3. **Gold Layer**
   - Stores transformed data ready for analysis. An additional **quality gate** is applied after dataset generation in this layer, ensuring that only high-quality data is available for analytics. The **Glue Data Catalog** also manages metadata in this layer.

4. **Data Contract**
    - A **Data Contract** formalizes data quality and structure expectations across layers, ensuring consistency and governance between the Silver and Gold layers.
    - Reference:
        - https://www.datamesh-manager.com/
        - https://datacontract.com/

## Technologies Used

- **Python** with **FastAPI** for implementing the shopping cart API.
- **Amazon SNS** and **SQS** for the asynchronous message queue.
- **AWS Lambda** to process messages and store data.
- **Amazon DynamoDB** for NoSQL storage of transaction data.
- **AWS CloudWatch** and **SNS** for monitoring and alerts.
- **AWS Glue** for metadata management with the Data Catalog.
- **Quality Gates** for data validation in the Silver and Gold pipelines.
    - [SODA](https://www.soda.io/)
    - [Great Expectations](https://greatexpectations.io/)
- **Data Lake** with Medallion architecture (Bronze, Silver, and Gold layers).

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
