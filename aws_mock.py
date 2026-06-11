import boto3
from moto import mock_aws
# from mymodule import MyModel


@mock_aws
def test_my_model_save():
    conn = boto3.resource("s3", region_name="us-east-1")
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket="mybucket")
    # model_instance = MyModel("steve", "is awesome")
    # model_instance.save()
    # body = conn.Object("mybucket", "steve").get()["Body"].read().decode("utf-8")
    # assert body == "is awesome"

def get_mock_s3_client():
    # This method assumes that the moto mock is running at 5000
    # This can be done with `moto_server -p 5000` in the terminal
    s3_client = boto3.client( "s3", endpoint_url="http://localhost:5000", aws_access_key_id="mock", aws_secret_access_key="mock" )
    return s3_client

from unittest.mock import Mock, patch

@patch("your_module.boto3.client")
def test_get_mock_s3_client(mock_boto3_client):
    mock_client = Mock()
    mock_boto3_client.return_value = mock_client

    result = get_mock_s3_client()

    mock_boto3_client.assert_called_once_with(
        "s3",
        endpoint_url="http://localhost:5000",
        aws_access_key_id="mock",
        aws_secret_access_key="mock",
    )
    assert result is mock_client

def test_get_mock_s3_client_connects_to_moto():
    # This test assumes that the moto mock is running at 5000
    client = get_mock_s3_client()

    response = client.list_buckets()

    assert "Buckets" in response

# test_get_mock_s3_client_connects_to_moto()