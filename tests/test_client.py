import pytest
# from aws_cognito import AwsCognitoApi


# TODO - This needs tests!
@pytest.fixture(scope='module')
def client():
    return None
    # return AwsCognitoApi(access_key, secret_key, region_name)


@pytest.mark.usefixtures('client')
class TestClient(object):

    def test(self, client):
        # TODO!
        assert True
