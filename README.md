# myb-aws-cognito-api

A small Python client for the AWS Cognito Identity Provider API, built on `boto3`.

Requires Python 3.11 or newer.

## Installation

The package is available on PyPI:

```
pip install myb-aws-cognito-api
```

To install from source:

```
git clone https://github.com/mine-your-business/myb-aws-cognito-api.git
cd myb-aws-cognito-api
pip install .
```

## Usage

```python
from aws_cognito import AwsCognitoApi

api = AwsCognitoApi(
    access_key='AKIA...',
    secret_key='...',
    region_name='us-east-1',
)

token = api.get_user_access_token(
    client_id='your-app-client-id',
    user='user@example.com',
    password='...',
)
```

`get_user_access_token` runs the `USER_PASSWORD_AUTH` flow, so the app client must have
`ALLOW_USER_PASSWORD_AUTH` enabled. It returns the access token on success and an empty
string when Cognito responds with a challenge (for example `NEW_PASSWORD_REQUIRED`)
instead of tokens. Cognito errors such as `NotAuthorizedException` are raised as
`botocore.exceptions.ClientError`.

If `access_key`, `secret_key` or `region_name` are omitted, `boto3` falls back to its
standard credential and region resolution (environment variables, shared config, instance
roles).

## Development

```
pip install -r requirements-dev.txt
pip install -e .
flake8 .
pytest --verbose
```

The tests are offline. They use `botocore.stub.Stubber` to intercept Cognito calls, and
the request and response payloads they assert against live in
[`tests/fixtures/`](tests/fixtures). No AWS credentials are needed.

CI runs lint, tests and a package build on Python 3.11 through 3.14 for every pull
request and push to `main`. Dependabot opens weekly update PRs for pip dependencies and
GitHub Actions.

## Releases

Releases follow [Semantic Versioning](https://semver.org/).

1. Bump `__version__` in [`setup.py`](setup.py) and merge the change to `main`.
2. Go to [releases](https://github.com/mine-your-business/myb-aws-cognito-api/releases),
   draft a new release with a tag like `v1.1.0` targeting `main`, and publish it. The
   release title omits the `v` and describes the changes.
3. Publishing the release triggers
   [`.github/workflows/python-publish.yml`](.github/workflows/python-publish.yml), which
   builds the sdist and wheel and uploads them to
   [PyPI](https://pypi.org/project/myb-aws-cognito-api/) using
   [trusted publishing](https://docs.pypi.org/trusted-publishers/). No PyPI token is
   stored in GitHub; the PyPI project must list this repository, the
   `python-publish.yml` workflow and the `pypi` environment as a trusted publisher.
