import subprocess
import boto3
import logging
import psycopg2
from psycopg2 import OperationalError
import time
import argparse
import sys
from botocore.exceptions import ClientError
import signal
from typing import Tuple, Union
from datetime import datetime, timedelta
import math
import os
import json



aws_region = os.getenv("AWS_REGION", "ap-south-1") 

rds = boto3.client('rds', region_name=aws_region)
secret_manager = boto3.client('secretsmanager', region_name=aws_region)
ec2_client = boto3.client('ec2', region_name=aws_region)

def log_setup() -> None:
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)

    dformat = "[%(filename)s:%(lineno)d] :%(levelname)8s: %(message)s"
    handler.setFormatter(logging.Formatter(dformat))
    logger.addHandler(handler)
    log_level = logging.INFO
    if os.getenv("DEBUG", False):
        log_level = logging.DEBUG
    logger.setLevel(log_level)

    # Suppress the more verbose modules
    logging.getLogger("botocore").setLevel(logging.WARN)
    logging.getLogger("boto3").setLevel(logging.WARN)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Script to configure RDS database storage size."
    )
    parser.add_argument("--rds_instance", required=True, type=str, help="Name of the RDS database")
    parser.add_argument("--new-storage", required=True, type=int, help="New storage size for the RDS database")

    # new_storage
    return parser.parse_args()


# function to get RDS instance details
def get_rds_instance_details(instance_identifier):
    try:
        response = rds.describe_db_instances(DBInstanceIdentifier=instance_identifier)
        return response['DBInstances'][0]
    except Exception as e:
        logging.error(f"Error fetching RDS instance details: {e}")
        return None
    
def get_rds_creds(instance_identifier, secret_key="db_link"):
    # secret manager id is same as RDS instance identifier in our case
    response = secret_manager.get_secret_value(
        SecretId=instance_identifier
    )
    secret = json.loads(response['SecretString']).get(secret_key)
    user = secret.split(":")[1].strip("/")
    password = secret.split("@")[1].split(":")[-1]
    host = secret.split("@")[1].split(":")[0]
    db_name = secret.split("/")[-1]
    port = 5432
    return user, password, host, db_name, port

def duplicate_rds_instance(instance_identifier, new_storage):
    user, password, _ , db_name, port = get_rds_creds(instance_identifier, secret_key="db_link")
    source_rds_data = get_rds_instance_details(instance_identifier)

    instance_params = {
        "DBName": db_name,
        "DBInstanceIdentifier": f"new_{source_rds_data['DBInstanceIdentifier']}",
        "AllocatedStorage": new_storage,
        "DBInstanceClass": source_rds_data["DBInstanceClass"],
        "Engine": source_rds_data["Engine"],
        "MasterUsername": user,
        "MasterUserPassword": password,
        "Port": int(port),
        "DBSecurityGroups": [
            items["DBSecurityGroupName"]
            for items in source_rds_data["DBSecurityGroups"]
        ],
        "VpcSecurityGroupIds": [
            items["VpcSecurityGroupId"]
            for items in source_rds_data["VpcSecurityGroups"]
        ],
        "AvailabilityZone": source_rds_data["AvailabilityZone"],
        "DBSubnetGroupName": source_rds_data["DBSubnetGroup"]["DBSubnetGroupName"],
        "PreferredMaintenanceWindow": source_rds_data["PreferredMaintenanceWindow"],
        "DBParameterGroupName": source_rds_data["DBParameterGroups"][0][
            "DBParameterGroupName"
        ],
        "BackupRetentionPeriod": source_rds_data["BackupRetentionPeriod"],
        "PreferredBackupWindow": source_rds_data["PreferredBackupWindow"],
        "MultiAZ": source_rds_data["MultiAZ"],
        "EngineVersion": source_rds_data["EngineVersion"],
        "AutoMinorVersionUpgrade": source_rds_data["AutoMinorVersionUpgrade"],
        "LicenseModel": source_rds_data["LicenseModel"],
        "OptionGroupName": source_rds_data["OptionGroupMemberships"][0][
            "OptionGroupName"
        ],
        "PubliclyAccessible": source_rds_data["PubliclyAccessible"],
        "Tags": source_rds_data["TagList"],
        "StorageType": (
            "gp3"
            if source_rds_data["StorageType"] == "gp2"
            else source_rds_data["StorageType"]
        ),
        "StorageEncrypted": source_rds_data["StorageEncrypted"],
        "KmsKeyId": source_rds_data["KmsKeyId"],
        "CopyTagsToSnapshot": source_rds_data["CopyTagsToSnapshot"],
        "EnableIAMDatabaseAuthentication": source_rds_data[
            "IAMDatabaseAuthenticationEnabled"
        ],
        "EnablePerformanceInsights": source_rds_data["PerformanceInsightsEnabled"],
        "DeletionProtection": source_rds_data["DeletionProtection"],
        "EnableCustomerOwnedIp": source_rds_data["CustomerOwnedIpEnabled"],
        "BackupTarget": source_rds_data["BackupTarget"],
        "NetworkType": source_rds_data["NetworkType"],
        "CACertificateIdentifier": source_rds_data["CACertificateIdentifier"],
    }

    try:
        if source_rds_data["MaxAllocatedStorage"]:
            instance_params["MaxAllocatedStorage"] = source_rds_data[
                "MaxAllocatedStorage"
            ]
    except KeyError:
        pass

    response = rds.create_db_instance(**instance_params)
    return response

def check_rds_availability(
    host: str, port: str, dbname: str, user: str, password: str
) -> Union[bool, None]:
    # Set a timeout for the function
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(600)  # 10 minutes in seconds

    while True:
        try:
            # Attempt to establish a connection to the RDS database
            conn = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password
            )
            conn.close()
            logging.info(f"Connection established successfully with {host}.")
            time.sleep(90)
            return True

        except OperationalError:
            # If an OperationalError occurs (e.g., connection error), print the error
            logging.error(
                f"Error connecting to the RDS database {host}: Not ready to take connection yet."
            )
            logging.info("Retrying in 90 seconds...")
            time.sleep(90)

        except TimeoutError as e:
            logging.error(e)
            return False  # Indicate failure due to timeout

        finally:
            # Reset the alarm
            signal.alarm(0)
  
def rename_rds(old: str, new: str) -> dict:
    try:
        rds.modify_db_instance(
            DBInstanceIdentifier=old, NewDBInstanceIdentifier=new, ApplyImmediately=True
        )
        logging.info(f"DB renamed - {new}")
    except Exception as e:
        logging.error(f"Issue with renaming {old} -> {new} : {e}")
        exit(1)

def timeout_handler(signum: int, frame) -> None:
    raise TimeoutError("Timed out after as RDS is not ready to take connection")


def swap_db(old: str, new: str) -> None:
    logging.info(f"Renaming db: {old} -> {old}-old ")
    rename_rds(old, f"{old}-old")
    time.sleep(300)  # Adding time delay to wait for db renaming
    logging.info(f"Renaming db: {new} - > {old}")
    rename_rds(new, old)

def stop_rds(dbinstance: str) -> None:
    try:
        logging.info(f"Stopping the RDS instance - {dbinstance}")
        rds.stop_db_instance(DBInstanceIdentifier=dbinstance)
    except Exception as e:
        logging.error(f"Issue with stopping - {dbinstance} -> {e}")
        exit(1)

def allow_sgs(from_sg: str, to_sg: str, port: int) -> None:
    try:
        ec2_client.authorize_security_group_egress(
            GroupId=from_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": to_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("Lambda outbound rule for sg '%s' done", from_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.Duplicate":
            logging.error("sg egress change failed: %s", error)
            raise error
    try:
        ec2_client.authorize_security_group_ingress(
            GroupId=to_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": from_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("inbound rule for sg '%s' done", to_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.Duplicate":
            logging.error("sg ingress change failed: %s", error)
            raise error

    logging.info("ECS inbound rule SG '%s' -> '%s' done", from_sg, to_sg)


def revoke_sgs(from_sg: str, to_sg: str, port: int) -> None:
    try:
        ec2_client.revoke_security_group_egress(
            GroupId=from_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": to_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("ECS outbound rule for sg '%s' removed", from_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.NotFound":
            logging.error("sg egress change failed: %s", error)
            raise error
    try:
        ec2_client.revoke_security_group_ingress(
            GroupId=to_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": from_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("inbound rule for sg '%s' removed", to_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.NotFound":
            logging.error("sg ingress change failed: %s", error)
            raise error

    logging.info("SG '%s' -/-> '%s' done", from_sg, to_sg)

def sync_dbs(old_db: str, new_db: str) -> bytes:
    # Create pgsync configuration with source and destination db details
    logging.info("Creating .pgsync.yml with source and destination db links")
    with open(".pgsync.yml", "w") as f:
        f.write(f"from: {old_db}\n")
        f.write(f"to: {new_db}\n")
        f.write("to_safe: true\n")
    # pgsync
    logging.info("Syncing DB's")
    try:
        process = subprocess.Popen(
            ["pgsync", "--schema-first", "--all-schemas"],
            stdout=subprocess.PIPE,
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            logging.error(f"Command failed. Return code : {process.returncode}")
        else:
            logging.info("Sync completed ")
        return output
    except Exception as e:
        logging.error(f"Issue with db sync -> {e}")
        exit(1)

def migrate_rds(instance_identifier: str, new_storage: str) -> None:
    user, password, host , db_name, port = get_rds_creds(instance_identifier, secret_key="db_link")
    source_rds_data = get_rds_instance_details(instance_identifier)

    # ecs security group to be allowed to access new RDS for db sync
    from_sg = os.getenv("SG_ID")
    to_sg = [
        items["VpcSecurityGroupId"] for items in source_rds_data["VpcSecurityGroups"]
    ][0]

    allow_sgs(from_sg, to_sg, int(port))
    logging.info(f" Creating the duplicte rds of {instance_identifier}")

    logging.info(
        f"Duplicating the RDS instance {instance_identifier} with {new_storage} GB storage. \
        Existing storage -> {source_rds_data(instance_identifier)['AllocatedStorage']}"
    )
    new_rds_DBInstanceIdentifier = duplicate_rds_instance(instance_identifier, new_storage)["DBInstance"]["DBInstanceIdentifier"]

    logging.info(f"Creating {new_rds_DBInstanceIdentifier}")
    old_db_endpoint = host
    new_db_endpoint = (
        new_rds_DBInstanceIdentifier + "." + ".".join(old_db_endpoint.split(".")[1:])
    )
    check_rds_availability(new_db_endpoint, port, db_name, user, password)

    # DB sync
    source_db_link = f"postgresql://{user}:{password}@{old_db_endpoint}:{port}/{db_name}"
    destination_db_link = (
        f"postgresql://{user}:{password}@{new_db_endpoint}:{port}/{db_name}"
    )
    sync_dbs(source_db_link, destination_db_link)

    logging.info("Swapping dbs")
    swap_db(instance_identifier, new_rds_DBInstanceIdentifier)

    logging.info(f"Stopping the {instance_identifier}-old")
    stop_rds(f"{instance_identifier}-old")

    # Revoke SG rules
    revoke_sgs(from_sg, to_sg, int(port))

def run() -> None:
    log_setup()
    args = parse_arguments()
    if not args.rds_instance:
        logging.error("RDS instance name is required as an argument.")
        sys.exit(1)
    print(f"RDS Instance: {args.rds_instance}, New Storage: {args.new_storage} GB")
    # migrate_rds(args.rds_instance, args.new_storage)


if __name__ == "__main__":
    run()
    