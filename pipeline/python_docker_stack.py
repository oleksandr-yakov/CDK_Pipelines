from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_s3 as s3,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_iam as iam,
)
from constructs import Construct
from config import connection_arn, branch
import aws_cdk as cdk

class PipelineStackDocker(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            connection_arn=connection_arn,
            owner='fiesta-taco',
            repo='ovsrd-trainee-back-docker',
            branch=branch,
            action_name=f'GitHub_Source-ovsrd-trainee-back-docker-{branch}',
            output=git_source_output,
        )
        codebuild_role = iam.Role(self, f"CodeBuildRole-Front-{branch}",
                                  assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
                                  managed_policies=[
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess"),
                                  ])

        source_bucket = s3.Bucket(self, "SourceBucketDocker",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,  # delte s3 if stack had been deleted
                                  bucket_name=f"yakov-s3-docker-{branch}-qefh312u",
                                  )

        ecr_repo = ecr.Repository(self, "MyECRRepository",
                                  repository_name=f"yakov-docker-repo-{branch}")

        ecs_cluster = ecs.Cluster(self, "MyECSCluster",
                                  cluster_name=f"yakov-docker-cluster-{branch}")

        build_action = codepipeline_actions.CodeBuildAction(
            action_name=f'CodeBuildDocker-{branch}',
            project=codebuild.PipelineProject(self, f"BuildProjectDocker-{branch}",
                build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml")),
            input=git_source_output,
            outputs=[codepipeline.Artifact(artifact_name='output')]
        )

        pipeline = codepipeline.Pipeline(self, f"DockerPipeline-{branch}", stages=[
            codepipeline.StageProps(
                stage_name=f'SourceGit-docker-{branch}',
                actions=[source_action]
            ),
            codepipeline.StageProps(
                stage_name=f'Build-docker-{branch}',
                actions=[build_action]
            ),
        ])
