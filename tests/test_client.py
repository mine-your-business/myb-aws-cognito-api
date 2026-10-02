import pytest
from botocore.exceptions import ClientError

from aws_cognito import AwsCognitoApi

from .conftest import load_fixture

REQUEST = load_fixture('initiate-auth-user-password-request.json')
USER = REQUEST['AuthParameters']['USERNAME']
PASSWORD = REQUEST['AuthParameters']['PASSWORD']
CLIENT_ID = REQUEST['ClientId']


def test_client_targets_cognito_idp_in_requested_region(api):
    assert api._client.meta.service_model.service_name == 'cognito-idp'
    assert api._client.meta.region_name == 'us-east-1'


def test_returns_access_token_on_success(api, stubber):
    response = load_fixture('initiate-auth-success.json')
    stubber.add_response('initiate_auth', response, REQUEST)

    token = api.get_user_access_token(CLIENT_ID, USER, PASSWORD)

    assert token == response['AuthenticationResult']['AccessToken']


def test_returns_empty_string_when_challenge_is_issued(api, stubber):
    stubber.add_response(
        'initiate_auth',
        load_fixture('initiate-auth-new-password-required-challenge.json'),
        REQUEST,
    )

    assert api.get_user_access_token(CLIENT_ID, USER, PASSWORD) == ''


def test_propagates_cognito_errors(api, stubber):
    error = load_fixture('initiate-auth-not-authorized-error.json')
    stubber.add_client_error(
        'initiate_auth',
        service_error_code=error['Code'],
        service_message=error['Message'],
        http_status_code=error['HTTPStatusCode'],
        expected_params=REQUEST,
    )

    with pytest.raises(ClientError) as excinfo:
        api.get_user_access_token(CLIENT_ID, USER, PASSWORD)

    assert excinfo.value.response['Error']['Code'] == error['Code']


def test_credentials_are_passed_to_boto3():
    api = AwsCognitoApi(access_key='AKIDEXAMPLE', secret_key='secret-example', region_name='eu-west-1')

    credentials = api._client._request_signer._credentials
    assert credentials.access_key == 'AKIDEXAMPLE'
    assert credentials.secret_key == 'secret-example'
