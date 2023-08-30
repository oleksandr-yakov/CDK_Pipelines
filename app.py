#!/usr/bin/env python3
import aws_cdk as cdk
from pipeline.python_front_stack import PipelineStackFront
from pipeline.python_docker_stack import PipelineStackDocker
from pipeline.python_serverless_stack import PipelineStackServerless
from pipeline.python_docker_ecr import PipelineStackDockerECR
from config import account_id, region, branch


app = cdk.App()

front_stack = PipelineStackFront(app, "PipelineStackFront",
                                 env=cdk.Environment(account=account_id, region=region),
                                 stack_name=f'front-stack-{branch}')

serverless_stack = PipelineStackServerless(app, "PipelineStackServerless",
                        env=cdk.Environment(account=account_id, region=region),
                        stack_name=f'serverless-stack-{branch}')

docker_stack = PipelineStackDocker(app, "PipelineStackDocker",
                    env=cdk.Environment(account=account_id, region=region),
                    stack_name=f'docker-stack-{branch}')

docker_ecr_stack = PipelineStackDockerECR(app, "PipelineStackDockerECR",
                       env=cdk.Environment(account=account_id, region=region),
                       stack_name=f'docker-ERC-stack-{branch}')

serverless_stack.add_dependency(front_stack)
docker_ecr_stack.add_dependency(serverless_stack)
docker_stack.add_dependency(docker_ecr_stack)

app.synth()


