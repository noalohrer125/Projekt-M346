import json
import boto3
import csv

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Event-Details extrahieren
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Datei aus S3 lesen
    csv_file = s3.get_object(Bucket=bucket_name, Key=file_key)
    csv_content = csv_file['Body'].read().decode('utf-8').splitlines()
    
    # CSV zu JSON konvertieren
    reader = csv.DictReader(csv_content)
    json_data = list(reader)

    # JSON-Datei speichern
    output_bucket = 'json-output-bucket'  # Ersetzen mit deinem Output-Bucket
    output_key = file_key.replace('.csv', '.json')
    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=json.dumps(json_data),
        ContentType='application/json'
    )

    return {"statusCode": 200, "body": "File converted successfully"}
