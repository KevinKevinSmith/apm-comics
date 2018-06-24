# importData.py
# APM Comics Demo
# Austin Krauza- June 2018
# Lambda function to read a CSV file from S3 and insert it into the DynamoDB Table

import urllib.parse
import boto3
import csv

# Definitions for DynamoDB Table
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    """
    Function handler. The "main" or "driver" of the Lambda Method.
    Recieves an event from S3, reads the CSV file, parses, and inserts into DynamoDB a table
    :param event:
    :param context:
    :return:
    """
    global s3
    global dynamodb
    # Get the object from the event and show its content type
    bucket = "YOUR_BUCKET_HERE"
    key = "data/books.csv"
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode('utf-8').splitlines(True)
        reader = csv.DictReader(body, delimiter=',')
        for record in reader:
            # Removes any keys from the dictionary for which there are no value (i.e. empty columns for a row)
            r = {k: v for k, v in record.items() if v != ''}
            # If the row contains an ISBN number
            if 'isbn' in r:
                r['itemtype'] = "book"
                r['itemid'] = r['isbn']
                # Convert the dictionary to an item readable by DynamoDB
                itm = dict_to_item(r)
                dynamodb.put_item(TableName='apm-comics-prod', Item=itm)
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e

    key = "data/customers.csv"
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode('utf-8').splitlines(True)
        reader = csv.DictReader(body, delimiter=',')
        for record in reader:
            # Removes any keys from the dictionary for which there are no value (i.e. empty columns for a row)
            r = {k: v for k, v in record.items() if v != ''}
            # If the row contains an email
            if 'email' in r:
                r['itemtype'] = "customer"
                r['itemid']= r['email']
                itm = dict_to_item(r)
                dynamodb.put_item(TableName='apm-comics-prod', Item=itm)
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e


def dict_to_item(raw):
    if type(raw) is dict:
        resp = {}
        for k, v in raw.items():
            if type(v) is str:
                resp[k] = {
                    'S': v
                }
            elif type(v) is int:
                resp[k] = {
                    'I': str(v)
                }
            elif type(v) is dict:
                resp[k] = {
                    'M': dict_to_item(v)
                }
            elif type(v) is list:
                resp[k] = []
                for i in v:
                    resp[k].append(dict_to_item(i))

        return resp
    elif type(raw) is str:
        return {
            'S': raw
        }
    elif type(raw) is int:
        return {
            'I': str(raw)
        }
