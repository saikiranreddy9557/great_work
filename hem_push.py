import subprocess
from subprocess import TimeoutExpired

region = "ap-south-1"

uri = "472222546423.dkr.ecr.ap-south-1.amazonaws.com/sample-demo"
ecr_url = "https://472222546423.dkr.ecr.ap-south-1.amazonaws.com"
ecr_uri = ecr_url.replace("https://","")

print(ecr_uri)

acces_key ="AKIAW34VIHH3TRJ5IHSD"
secret_key = "wRzvCqa8nIcUydaQQ2FL9EpFGWuzNrpAx6lNti91"

set_access_key_cmd = "aws configure set aws_access_key_id {}".format(acces_key)
set_secret_key_cmd = "aws configure set aws_secret_access_key {}".format(secret_key)

login_cmd = "aws ecr get-login-password \
     --region {region} | helm registry login \
     --username AWS \
     --password-stdin {ecr_uri}".format(region=region,ecr_uri=ecr_uri)

push_cmd ="helm push helm-test-chart-0.1.0.tgz oci://{ecr_uri}/".format(ecr_uri=uri)

# helm push helm-test-chart-0.1.0.tgz oci://aws_account_id.dkr.ecr.region.amazonaws.com/
print(push_cmd)


commands = [set_access_key_cmd,set_secret_key_cmd,login_cmd,push_cmd]

def helm_push(commands):
    try:
        for cmd in commands:
            # r =subprocess.run(cmd,stdout=subprocess.PIPE,shell=True,universal_newlines=True)
            # stdout=subprocess.PIPE
            # r =subprocess.run(cmd,stdout=subprocess.PIPE)
            # r = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
            # print(r.stdout)
            # print("raaaaaaaaaaaa,",r.stdout)
            # text = r.communicate()[0].decode('utf-8')
            # for i in text.splitlines():
            #     print(i)
            # capture_output=True, text=True
            r =subprocess.run(cmd,shell = True,capture_output=True, text=True)
            print("eeeee",r.stderr)
            if "Error" in r.stderr:
                print("aa")
                raise Exception
                
     
    except Exception as e  :
        print("error occured while helm push")
        print(e)
        
        
        return False
    

    print("helm upload completd")
    return True
        

print(helm_push(commands))
