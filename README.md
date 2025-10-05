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

- **S3:** Storage for raw datasets and Parquet outputs  
- **Glue:** Crawlers to infer schema and catalog datasets  
- **Athena:** Query datasets directly using SQL  
- **Lambda + SNS:** Event-driven notifications on new uploads  
- **IAM + CloudFormation:**  
  - IAM roles for Lambda, Glue, and users   
  - Infrastructure defined and deployed via CloudFormation templates  

---

## Dataset
The project works on real estate listings with columns like:  
`titre, prix, surface, localisation, chambres, salles_bain, source`  


---

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
- **Validate templates:** Always run `aws cloudformation validate-template` before deploying a stack to catch errors early.  
- **Data cleaning:** Use Athena or preprocessing scripts to handle inconsistent or malformed data before casting to numeric types, especially for prices or areas.  
- **Use Parquet format:** Store datasets in Parquet to optimize Athena query performance and reduce scanning costs.  

- **SNS notifications:** When using SNS for automated notifications, ensure the topic is subscribed to by the intended recipients (email or other endpoints) and confirm the subscription before relying on alerts.  
