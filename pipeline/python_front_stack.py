from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam,
)
import aws_cdk as cdk
from constructs import Construct
from config import connection_arn, branch


class PipelineStackFront(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        codebuild_role = iam.Role(self, f"CodeBuildRole-Front-{branch}",
                                 assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
                                 managed_policies=[
                                     iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                                     iam.ManagedPolicy.from_aws_managed_policy_name("CloudFrontFullAccess"),
                                 ]
                                 )

        source_bucket = s3.Bucket(self, "SourceBucket",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,                       # delte s3 if stack had been deleted
                                  bucket_name=f"yakov-s3-front-{branch}-qefh312u",
                                  #public_read_access=True,
                                  #access_control=s3.BucketAccessControl.PUBLIC_READ,
                                  )



        distribution = cloudfront.CloudFrontWebDistribution(self, f"MyDistributionFront-{branch}",
                                                            origin_configs=[cloudfront.SourceConfiguration(
                                                                s3_origin_source=cloudfront.S3OriginConfig(
                                                                    s3_bucket_source=source_bucket),
                                                                behaviors=[
                                                                    cloudfront.Behavior(is_default_behavior=True,#use this configuration by deffault
                                                                                        compress=True,
                                                                                        allowed_methods=cloudfront.CloudFrontAllowedMethods.GET_HEAD,
                                                                                        )],
                                                            )],
                                                            )

        git_source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            connection_arn=connection_arn,
            owner='fiesta-taco',
            repo='ovsrd-trainee-front',
            branch=branch,   # use global env var : DEV_ENV=dev && cdk deploy <name stack> --profile oyakovenko-trainee
            action_name=f'GitHub_Source_ovsrd-trainee-front-{branch}',
            output=git_source_output,
            trigger_on_push=True,
        )


        build_action = codepipeline_actions.CodeBuildAction(
            action_name=f'CodeBuildFront-{branch}',
            project=codebuild.PipelineProject(self, f"BuildProjectFront-{branch}",
                                              build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
                                              role=codebuild_role,
                                              ),

                                                                      #codepipline роль не нужна
                                                                      #он ничего не делает
                                                                      #а запуск codebuild есть по дефолту
                                                                      #кажется раньше надо было - сейчас если роль не указать
                                                                      # то она какая то будет дефолтная
                                                                      #а вот codebuild делает работу
                                                                      #ему нужен full access к s3 и cloudfront

            input=git_source_output,
            outputs=[codepipeline.Artifact(artifact_name='output')],
        )

        pipeline = codepipeline.Pipeline(self, f"FrontPipeline-{branch}",
                                        stages=[
                                            codepipeline.StageProps(
                                                stage_name=f'SourceGit-front-{branch}',
                                                actions=[source_action]
                                            ),
                                            codepipeline.StageProps(
                                                stage_name=f'Build-front-{branch}',
                                                actions=[build_action]
                                            ),
                                        ])







