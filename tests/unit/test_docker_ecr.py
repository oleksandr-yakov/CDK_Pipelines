import pytest
from aws_cdk import App
from pipeline.python_docker_ecr import PipelineStackDockerECR
from config import account_id, region


@pytest.fixture
def app():
    yield App()


@pytest.fixture
def stack(app):
    yield PipelineStackDockerECR(app, "TestPipelineStackockerECR", env={'account': f'{account_id}', 'region': f'{region}'})

def test_stack_creation(stack):
    assert stack is not None
    assert stack.ecr_repo is not None


if __name__ == '__main__':
    pytest.main()
