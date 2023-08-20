from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_s3 as s3,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from constructs import Construct
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
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

        ecr_policy = iam.PolicyStatement(
            actions=["ecr:GetAuthorizationToken"],
            resources=["*"]
        )

        codebuild_role = iam.Role(self, f"CodeBuildRole-Front-{branch}",
                                  assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
                                  managed_policies=[
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser"),
                                  ])

        codebuild_role.attach_inline_policy(
            iam.Policy(self, "ECRAuthorizationPolicy", statements=[ecr_policy])
        )

        source_bucket = s3.Bucket(self, "SourceBucketDocker",
                                  removal_policy=cdk.RemovalPolicy.DESTROY,  # delte s3 if stack had been deleted
                                  bucket_name=f"yakov-s3-docker-{branch}-qefh312u",
                                  )

        ecr_repo = ecr.Repository(self, "MyECRRepository",
                                  repository_name=f"yakov-docker-repo-{branch}")

        ecs_cluster = ecs.Cluster(self, "MyECSCluster",
                                  cluster_name=f"yakov-docker-cluster-{branch}")

        ecs_cluster.add_capacity("DefaultAutoScalingGroupCapacity",
                                 instance_type=ec2.InstanceType("t2.micro"),
                                 desired_capacity=1,
                                 )

        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")

        container = task_definition.add_container("DefaultContainer",
                                                  image=ecs.ContainerImage.from_ecr_repository(ecr_repo, "testv1"),
                                                  memory_limit_mib=200,
                                                  )
        container.add_port_mappings(ecs.PortMapping(container_port=3003, host_port=85))

        ecs_service = ecs.Ec2Service(self, "Service",
                                     service_name=f"yakov-docker-service-{branch}",
                                     cluster=ecs_cluster,
                                     task_definition=task_definition
                                     )

        build_project = codebuild.PipelineProject(
            self,
            f"BuildProjectDocker-{branch}",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment={
                "privileged": True
            },
            role=codebuild_role,
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name=f'CodeBuildDocker-{branch}',
            project=build_project,
            input=git_source_output,
            outputs=[codepipeline.Artifact(artifact_name='output')],
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
