import json
import boto3
import urllib.parse
from datetime import datetime

sns = boto3.client('sns')
glue = boto3.client('glue')

SNS_TOPIC_ARN = "arn:aws:sns:eu-west-3:XXXXXXXXXXXX:dataset-upload-topic"
CRAWLER_NAME = "cfn-crawler-immobilier"

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        size = record['s3']['object'].get('size', 'unknown')
        upload_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Message détaillé
        message = (
            f" Nouveau dataset détecté !\n\n"
            f" Bucket : {bucket}\n"
            f" Fichier : {key}\n"
            f" Taille : {size} octets\n"
            f" Uploadé à : {upload_time}\n\n"
        )
        
        # Envoyer la notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=" Nouveau dataset uploadé"
        )
        
        #  Démarrer le crawler Glue
        glue.start_crawler(Name=CRAWLER_NAME)
        
    return {"status": "done"}
