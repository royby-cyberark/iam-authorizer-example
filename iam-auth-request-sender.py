# uses AWSRequestsAuth

import json
import boto3
from aws_auth import AWSRequestsAuth
import requests


def lambda_handler(event, context):

    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::<account_id<:role/<role_name>",
        RoleSessionName="cross_acct_lambda",
        ExternalId="some_ex_id_if_needed",
    )

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    print(f'AssumedRoleUser={acct_b["AssumedRoleUser"]}')

    # call api with v4 things

    base_url = 'https://<api-id>.execute-api.us-east-1.amazonaws.com/<stage>/'
    url = base_url + 'someapi' # could be something like api/dogs or dogs or whatever
    session = boto3.Session()
    # credentials = session.get_credentials()
    auth = AWSRequestsAuth(aws_access_key=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_token=SESSION_TOKEN, aws_host=base_url,
                           aws_region=session.region_name, aws_service='execute-api')


    headers = {"Content-Type": "application/json"}
    res = requests.post(url=url, data=request_input, headers=headers, auth=auth)
    print(f'Status code: {res.status_code}')
    print(f'Reason: {res.reason}')


    return {'statusCode': 200, 'body': json.dumps('OK')}
