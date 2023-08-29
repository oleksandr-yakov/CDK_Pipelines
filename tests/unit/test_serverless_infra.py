import pytest
from aws_cdk import App
from pipeline.python_serverless_stack import PipelineStackServerless
from config import account_id, region


@pytest.fixture
def app():
    yield App()


@pytest.fixture
def stack(app):
    yield PipelineStackServerless(app, "TestPipelineStackFront", env={'account': f'{account_id}', 'region': f'{region}'})


def test_stack_creation(stack):
    assert stack is not None
    assert stack.list_table is not None
    assert stack.card_table is not None


if __name__ == '__main__':
    pytest.main()
