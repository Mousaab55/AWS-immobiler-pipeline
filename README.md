# AWS immobilier Pipeline

## Overview
Inspired by my internship experience working with real estate dataset that i have scraped, I built a **serverless AWS pipeline** that automatically cleans, catalogs, and analyzes property data.  

Whenever a new dataset lands in S3, the pipeline:  
- **Infers the schema** with AWS Glue crawlers  
- **Transforms and enriches** the data (e.g., calculating price per m²)  
- **Notifies users** automatically via Lambda + SNS  
- Makes data **ready for analysis** in Athena  

It’s basically a **hands-off, self-updating real estate data lake**, perfect for multi-department use and scalable analytics.

---

## Architecture
The pipeline uses the following AWS services:  

- **S3:** Storage for raw datasets
- **Glue:** Crawlers to infer schema and catalog datasets  
- **Athena:** Query datasets directly using SQL  
- **Lambda + SNS:** Event-driven notifications on new uploads  
- **IAM + CloudFormation:**  
  - IAM roles for Lambda, Glue, and users   
  - Infrastructure defined and deployed via CloudFormation templates  

---

## Dataset
The project works on real estate listings with columns like:  
`titre, prix, surface, chambres, salles_bain, source, garage, terrassse`  


---
## Main Tasks

- **Task 1 – Configure AWS Glue Crawler:**  
  Set up a crawler to scan the S3 bucket, detect schema, and register metadata in AWS Glue Data Catalog. Modified schema to include a new computed column: `prix_m2`.

- **Task 2 – Query and Validate Data with Athena:**   
  Configured an S3 bucket to store Athena query results, previewed the Glue-inferred table, and verified data integrity before analysis.

- **Task 3 – Automate Infrastructure with CloudFormation:**  
  Created reusable templates to deploy IAM roles, Glue crawlers, and Lambda functions automatically. Validated templates before stack creation.

- **Task 4 – Implement Lambda + SNS Integration:**  
  Built a Lambda that triggers on S3 upload events, runs the crawler, and sends notifications to subscribed users (e.g., Finance) through Amazon SNS.

- **Task 5 – Simulate Multi-User Access with IAM Roles:**  
  Tested different users (Finance, Admin) by exporting AWS credent

## Steps / Workflow

1. **Upload dataset to S3** → triggers Lambda  
2. **Lambda publishes a message to SNS** and starts the Glue crawler  
3. **CloudFormation templates** deploy IAM roles for secure access:  
   - Lambda execution role  
   - Glue crawler role  
   - users   
4. **Glue crawler** infers schema, updates the catalog,  
5. **Athena queries** the tables for analytics.  

---


## Tips

- **Avoid parasitic tables:** Glue crawlers may create extra “parasitic tables” if multiple files or folders exist in your S3 bucket. Consider separating raw uploads and Athena query results into different S3 prefixes or buckets.  
- **Lambda triggers:** Ensure S3 PUT event triggers are configured correctly to invoke your Lambda function on every new upload.  
- **CloudFormation for reproducibility:** Define all IAM roles, Glue crawlers, and permissions in CloudFormation templates to easily reproduce the pipeline across environments.  
- **Validate templates:** Always run `aws cloudformation validate-template` before deploying a stack.
- **Use Parquet format:** Store datasets in Parquet to optimize Athena query performance and reduce scanning costs.  
- **SNS notifications:** When using SNS for automated notifications, ensure the topic is subscribed to by the intended recipients (email or other endpoints) and confirm the subscription before relying on alerts.  
