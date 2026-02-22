import json

aws_data = """
{
    "organization": "CloudTech Inc",
    "regions": {
        "us-east-1": {
            "instances": [
                {
                    "id": "i-0123456789abcdef0",
                    "type": "t2.micro",
                    "state": "running",
                    "tags": {
                        "Name": "web-server-1",
                        "Environment": "production"
                    },
                    "security_groups": [
                        {"id": "sg-12345678", "name": "default"},
                        {"id": "sg-87654321", "name": "web-access"}
                    ]
                }
            ],
            "databases": {
                "rds": {
                    "primary": {
                        "engine": "mysql",
                        "version": "8.0",
                        "replicas": [
                            {"id": "db-replica-1", "region": "us-west-2"},
                            {"id": "db-replica-2", "region": "eu-west-1"},
                            {"id": "db-replica-3", "region": "eu-west-1"},
                            {"id": "db-replica-4", "region": "eu-west-2"}
                        ]
                    }
                }
            }
        },
        "eu-west-1": {
            "instances": [],
            "s3_buckets": [
                {
                    "name": "my-data-bucket",
                    "versioning": true,
                    "lifecycle_rules": [{"days": 90, "action": "delete"}]
                }
            ]
        }
    },
    "iam": {
        "users": [
            {"username": "alice", "mfa_enabled": true, "policies": ["AdminAccess"]},
            {"username": "bob", "mfa_enabled": false, "policies": ["ReadOnlyAccess"]}
        ]
    }
}
"""

# aws_data = json.loads(aws_data)
# print(aws_data)


# # print(aws_data.keys()) # dict_keys(['organization', 'regions', 'iam'])
# rds_replicas = aws_data["regions"]["us-east-1"]["databases"]["rds"]["primary"]["replicas"] # dict_keys(['us-east-1', 'eu-west-1'])

# # print all rds databases in the region eu-west-1
# # print(type(rds_replicas))

# rds_data_i_want = []
# # i will use .append() or .extend()
# region_i_want = "eu-west-1"
# for item in rds_replicas:
#     if item["region"] == region_i_want:
#         # print(item["id"], item["region"])
#         # print(item["id"])
#         rds_data_i_want.append(item["id"])

# print(rds_data_i_want)

# take string (json string) and get me the rds instances in a certain region


def get_rds_instances_in_region(data_string, region):
    data = json.loads(data_string)

    rds_replicas = data["regions"]["us-east-1"]["databases"]["rds"]["primary"][
        "replicas"
    ]
    rds_data_i_want = []
    for item in rds_replicas:
        if item["region"] == region:
            rds_data_i_want.append(item["id"])
    return rds_data_i_want


# print(get_rds_instances_in_region(aws_data, "eu-west-2"))


# create a functio to stop rds at a certain region, and stop them
def stop_rds_instaces(rds_instances):
    for instance in rds_instances:
        # logic to stop rds instance
        print(f"Stopping RDS instance: {instance}")

    return True


stop_rds_instaces(get_rds_instances_in_region(aws_data, "eu-west-1"))
