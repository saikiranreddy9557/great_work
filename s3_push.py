# sample--bucket--doc
import boto3
from botocore.exceptions import NoCredentialsError



ACCESS_"
SECRET_KEY = ""


def upload_to_aws_helm_chart(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        v = s3.upload_file(local_file, bucket, s3_file)
        print("vv",v)
        print("Upload Successful")
        return True
    except Exception as e:
        print(e  )
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

file_path = "helm-test-chart-test-chart-0..0.tgz"
bucket_name = "sample--bucket--doc"
s3_file_name = "helm_upload"
uploaded = upload_to_aws_helm_chart(file_path, bucket_name, s3_file_name)
print("sss",uploaded)
