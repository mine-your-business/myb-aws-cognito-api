import json
from pathlib import Path

import pytest
from botocore.stub import Stubber

from aws_cognito import AwsCognitoApi

FIXTURES = Path(__file__).parent / 'fixtures'


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


@pytest.fixture(autouse=True)
def offline_aws_env(monkeypatch):
    # Keep boto3 from picking up a developer's real profile or credentials.
    for var in ('AWS_PROFILE', 'AWS_DEFAULT_PROFILE', 'AWS_SESSION_TOKEN', 'AWS_SECURITY_TOKEN'):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv('AWS_CONFIG_FILE', '/dev/null')
    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE', '/dev/null')
    monkeypatch.setenv('AWS_EC2_METADATA_DISABLED', 'true')


@pytest.fixture
def api():
    return AwsCognitoApi(access_key='testing', secret_key='testing', region_name='us-east-1')


@pytest.fixture
def stubber(api):
    with Stubber(api._client) as stub:
        yield stub
        stub.assert_no_pending_responses()
