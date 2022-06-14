import docker
import boto3
import base64
import json
import os

# acces_key ="AKIAW34VIHH3R4PND75F"
# secret_key = "UFhlUX6Lf/KYB9/yUn+ZVkBBKkqZWsQcMlnqLP3c"

uri  = "public.ecr.aws/g4a1d4c4/example-demo"
region="ap-south-1"

LOCAL_REPOSITORY = 'sample-demo'

# repo_name = "example-demo"

acces_key ="AKIAW34VIHH3TRJ5IHSD"
secret_key = "wRzvCqa8nIcUydaQQ2FL9EpFGWuzNrpAx6lNti91"


def read_aws_credentials():
    dic_map = {'access_key_id':acces_key,'secret_access_key':secret_key,'region':region}
    return dic_map


def main():
    """Build Docker image, push to AWS and update ECS service.
    
    :rtype: None
    """

    # get AWS credentials
    aws_credentials = read_aws_credentials()
    access_key_id = aws_credentials['access_key_id']
    secret_access_key = aws_credentials['secret_access_key']
    aws_region = aws_credentials['region']

    # build Docker image
    docker_client = docker.from_env()
    print(docker_client)
    image, build_log = docker_client.images.build(
        path='.', tag=LOCAL_REPOSITORY, rm=True)
    
    print("image",image)

    # get AWS ECR login token
    ecr_client = boto3.client(
        'ecr', aws_access_key_id=access_key_id, 
        aws_secret_access_key=secret_access_key, region_name=aws_region)

    print("access",access_key_id)

    print("ecr_c;inet",ecr_client)

    ecr_credentials = (
        ecr_client
        .get_authorization_token()
        ['authorizationData'][0])

    v = ecr_client.get_authorization_token()
    print("auth token",v)


    print("ecr_cred",ecr_credentials)

    ecr_username = 'AWS'

    ecr_password = (
        base64.b64decode(ecr_credentials['authorizationToken'])
        .replace(b'AWS:', b'')
        .decode('utf-8'))

    ecr_url = ecr_credentials['proxyEndpoint']
    print("ecr_url",ecr_url)

    # get Docker to login/authenticate with ECR
    docker_client.login(
        username=ecr_username, password=ecr_password, registry=ecr_url)

    # tag image for AWS ECR
    ecr_repo_name = '{}/{}'.format(
        ecr_url.replace('https://', ''), LOCAL_REPOSITORY)
    print("ecr_repo",ecr_repo_name)


    image.tag(ecr_repo_name, tag='latest')

    # push image to AWS ECR
    # ecr_repo_name = ecr_repo_name+":latest"
    print(ecr_repo_name)
    push_log = docker_client.images.push(ecr_repo_name, tag='latest')
    print("pushlog",push_log)

    return True


main()
