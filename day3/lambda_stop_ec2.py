import boto3
import logging
from botocore.config import Config

ec2_config = Config(
    region_name = 'ap-south-1',
)

ec2= boto3.client('ec2', config=ec2_config)

def get_instances():
    return [
        (
            item.get("Instances")[0]["InstanceId"],
            item.get("Instances")[0]["State"]["Name"],
        )
        for item in ec2.describe_instances().get("Reservations")
    ]
def stop_instances(instance_ids):
    ec2.stop_instances(
        InstanceIds=instance_ids,
        Force=True
    )


def lambda_handler(event, context):
    instances = [ instance for instance,_ in get_instances()]
    print(f" Stopping the instances {instances}")
    stop_instances(instances)
    

if __name__ == "__main__":
    lambda_handler("", "")