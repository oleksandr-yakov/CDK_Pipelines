import os


connection_arn = "arn:aws:codestar-connections:eu-central-1:666398651410:connection/46c6e5d6-ba43-49e9-bb58-cf9bd4c97755" #           arn:aws:codestar-connections:eu-central-1:666398651410:connection/c3334e5c-add7-4e56-a34e-e0baab5c5a7e
account = '666398651410'
account_test = '423704380788'
region = 'eu-central-1'

branch = os.environ.get('DEV_ENV')
# print(branch)
#branch = "main"


# - aws s3 rm s3://$S3_BUCKET_NAME --recursive --exclude 'core/*'

# - aws s3 sync ./dist s3://$S3_BUCKET_NAME --cache-control max-age=604800 --exclude 'index.html' --exclude 'core/*'

# - AWS_MAX_ATTEMPTS=10 aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_DISTRIBUTION_ID --paths "/*"

