import boto3

ec2 = boto3.client("ec2")

# response = ec2.describe_instances().get("Reservations")

# print(response)
# print(type(response))

# instances = [("instacneID", "state"),("instacneID", "state")]
# instances = []
# for item in response:
#     # print(item.get("Instances"))
#     # print(len(item.get("Instances")))
#     # print(item.get("Instances")[0]["InstanceId"])
#     # print("##########################")
#     # print("##########################")
#     Instance_ID = item.get("Instances")[0]["InstanceId"]
#     state = item.get("Instances")[0]["State"]["Name"]
#     instances.append((Instance_ID,state ))

#     # print(f'InstanceId -> {Instance_ID} with state {state}')
# print(instances)

# to_print=

# List comprenhsion
# l=[]
# for i in range(1,11):
#     l.append(i)
# print(l)

# l = [i for i in range(1,11)]
# print(l)


#   response = ec2.describe_instances().get("Reservations")
#     Instance_ID = item.get("Instances")[0]["InstanceId"]
#     state = item.get("Instances")[0]["State"]["Name"]
def get_instances():
    return [
        (
            item.get("Instances")[0]["InstanceId"],
            item.get("Instances")[0]["State"]["Name"],
        )
        for item in ec2.describe_instances().get("Reservations")
    ]


# instance_ids is a list
def stop_instances(instance_ids):
    ec2.stop_instances(
        InstanceIds=instance_ids,
        Force=True
    )

def start_instances(instance_ids):
    ec2.start_instances(
    InstanceIds=instance_ids

)

def main():

    # instances = [("instacneID", "state"),("instacneID", "state")]
    instance_data = get_instances()
    instances = []
    for item in instance_data:
        # print(item)
        instance, _ = item
        # instance = item(0)
        instances.append(instance)
    # print(instances)
    # stop_instances(instances)
    start_instances(instances)


main()