import pytest
from aws_cdk import App
from pipeline.python_front_stack import PipelineStackFront
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
)
from config import account_id, region

@pytest.fixture
def app():
    yield App()


@pytest.fixture
def stack(app):
    yield PipelineStackFront(app, "TestPipelineStackFront", env={'account': f'{account_id}', 'region': f'{region}'})


def test_stack_creation(stack):
    assert stack is not None


def test_s3_bucket_creation(stack):
    assert any(isinstance(res, s3.CfnBucket) for res in stack.node.find_all())


def test_cloudfront_distribution_creation(stack):
    assert any(isinstance(res, cloudfront.CfnDistribution) for res in stack.node.find_all())


if __name__ == '__main__':
    pytest.main()
