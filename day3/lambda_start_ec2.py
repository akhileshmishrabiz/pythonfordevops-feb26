import boto3
from botocore.config import Config

ec2_config = Config(
    region_name = 'ap-south-1',
)

ec2= boto3.client('ec2', config=ec2_config)
ec2= boto3.client('ec2')

def get_instances():
    return [
        (
            item.get("Instances")[0]["InstanceId"],
            item.get("Instances")[0]["State"]["Name"],
        )
        for item in ec2.describe_instances().get("Reservations")
    ]

def start_instances(instance_ids):
    ec2.start_instances(
    InstanceIds=instance_ids

)
    
def lambda_handler(event, context):
    instances = [ instance for instance,_ in get_instances()]
    print(f" Starting the instances {instances}")
    start_instances(instances)


if __name__ == "__main__":
    lambda_handler("", "")