import pytest
from aws_cdk import App
from pipeline.python_docker_stack import PipelineStackDocker
from config import account_id, region


@pytest.fixture
def app():
    yield App()


@pytest.fixture
def stack(app):
    yield PipelineStackDocker(app, "TestPipelineStackDocker", env={'account': f'{account_id}', 'region': f'{region}'})


def test_stack_creation(stack):
    assert stack is not None
    assert stack.ecr_stack_instance is not None
    assert stack.source_bucket is not None
    assert stack.ecs_cluster is not None
    assert stack.task_role is not None


if __name__ == '__main__':
    pytest.main()
