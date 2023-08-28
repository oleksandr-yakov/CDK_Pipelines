import os

connection_arn = "arn:aws:codestar-connections:eu-central-1:666398651410:connection/46c6e5d6-ba43-49e9-bb58-cf9bd4c97755" #           arn:aws:codestar-connections:eu-central-1:666398651410:connection/c3334e5c-add7-4e56-a34e-e0baab5c5a7e
account_id = '666398651410'
region = 'eu-central-1'
branch = os.environ.get('DEV_ENV')
crt_aws_manager_arn = "arn:aws:acm:eu-central-1:666398651410:certificate/6bf3c0d6-04d2-4f7c-b47c-c097bdf6d987"
crt_aws_manager_arn_front = "arn:aws:acm:us-east-1:666398651410:certificate/3f74281b-c871-4f2d-b2b7-ea5d0f05f113"


