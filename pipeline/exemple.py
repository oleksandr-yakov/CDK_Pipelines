from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk.aws_certificatemanager import Certificate
from constructs import Construct

# Функция для получения окружения (замените на свою логику)
def get_env():
    return "dev"

# Функция для получения тегов (замените на свою логику)
def get_tags(stack_id):
    return {}

class UiStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        bucket_name = f"{props['name']}-{get_env()}"

        # create bucket for hosting ui
        bucket = s3.Bucket(self, bucket_name,
                           bucket_name=bucket_name,
                           public_read_access=True,
                           access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL)

        # Create the CloudFront distribution
        certificate = Certificate.from_certificate_arn(self, 'certificate',
                                                       'arn:aws:acm:us-east-1:281158534830:certificate/4f2c5b22-ccbb-4205-a881-1f5043fb35eb')

        distribution = cloudfront.CloudFrontWebDistribution(self, f"{bucket_name}-distribution",
                                                            comment=f"{bucket_name} distribution",
                                                            origin_configs=[
                                                                cloudfront.SourceConfiguration(
                                                                    s3_origin_source=cloudfront.S3OriginConfig(
                                                                        s3_bucket_source=bucket),
                                                                    behaviors=[
                                                                        cloudfront.Behavior(
                                                                            is_default_behavior=True,
                                                                            compress=True,
                                                                            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                                            allowed_methods=cloudfront.CloudFrontAllowedMethods.GET_HEAD
                                                                        )
                                                                    ]
                                                                )
                                                            ],
                                                            default_root_object='index.html',
                                                            error_configurations=[
                                                                # this cloudfront will be blocked by firewall, and we can't use custom error page for 403
                                                                cloudfront.CfnDistribution.CustomErrorResponseProperty(
                                                                    error_code=404,
                                                                    response_code=200,
                                                                    response_page_path='/index.html',
                                                                    error_caching_min_ttl=300
                                                                )
                                                            ],
                                                            viewer_certificate=cloudfront.ViewerCertificateProps(
                                                                aliases=['dev-new.oversecured.com'],
                                                                acm_certificate_arn=certificate.certificate_arn,
                                                                ssl_support_method=cloudfront.SSLMethod.SNI
                                                            ),
                                                            geo_restriction=cloudfront.GeoRestriction(
                                                                restriction_type='blacklist',
                                                                locations=['RU', 'BY']
                                                            ))

        # create route53 record for bucket
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(self, f"{bucket_name}-hosted-zone",
                                                                     hosted_zone_id="ZX85OZZYVSX45",
                                                                     zone_name="oversecured.com")

        cloudfront_target = route53_targets.CloudFrontTarget(distribution)
        record_target = route53_targets.RecordTarget.from_alias(cloudfront_target)

        route53.ARecord(self, f"{bucket_name}-record",
                        record_name='dev-new',
                        zone=hosted_zone,
                        target=record_target)


