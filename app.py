#!/usr/bin/env python3
import aws_cdk as cdk
from pipeline.python_front_stack import PipelineStackFront
from pipeline.python_docker_stack import PipelineStackDocker
from pipeline.python_serverless_stack import PipelineStackServerless
from config import account, region, branch


app = cdk.App()

PipelineStackFront(app, "PipelineStackFront",
                        env=cdk.Environment(account=account, region=region),
                        stack_name=f'front-stack-{branch}')

PipelineStackServerless(app, "PipelineStackServerless",
                        env=cdk.Environment(account=account, region=region),
                        stack_name=f'serverless-stack-{branch}')

PipelineStackDocker(app, "PipelineStackDocker",
                        env=cdk.Environment(account=account, region=region),
                        stack_name=f'docker-stack-{branch}')


app.synth()


