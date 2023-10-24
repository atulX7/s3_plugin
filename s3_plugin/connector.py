import boto3

class S3Connector:
    def __init__(self, aws_access_key, aws_secret_key):
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    def connect(self):
        # You can implement a test connection or connection initialization here.
        pass

    def fetch_data(self, bucket_name, key):
        return self.client.get_object(Bucket=bucket_name, Key=key)['Body'].read()
