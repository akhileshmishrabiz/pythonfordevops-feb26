import boto3
import json
import subprocess
import os

sqs = boto3.client('sqs')
s3 = boto3.client('s3')
ses = boto3.client('ses')

Queue_url = 'https://sqs.ap-south-1.amazonaws.com/879381241087/clamav-notify'

# landing_bucket = 'landing-bucket-879381241087'
clean_bucket = 'clean-bucket-879381241087'
locals_path = '/Users/akhilesh/projects/pythonfordevops-feb26/day4'

from_email = 'livingdevops@gmail.com'
to_email = ['abubaker.dev417@gmail.com', 'shivamshekhar960@gmail.com', 'aditiyamishranit@gmail.com']


def read_sqs_queue(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
    )
    message = response.get('Messages', [])[0]
    body = json.loads(message.get('Body'))
    # print(f"Received message: {body}")
    bucket = body['Records'][0]['s3']['bucket']['name']
    key = body['Records'][0]['s3']['object']['key']  

    return bucket, key, f's3://{bucket}/{key}', message.get('ReceiptHandle')

def delete_message_from_queue(queue_url, receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

def download_file_from_landing_s3(landing_bucket, object_key, download_path):
    print(f"Downloading s3://{landing_bucket}/{object_key} to {download_path}")
    s3.download_file(landing_bucket, object_key, download_path)

def upload_file_to_clean_s3(clean_bucket, object_key, file_path):
    print(f"Uploading {file_path} to s3://{clean_bucket}/{object_key}")
    s3.upload_file(file_path, clean_bucket, object_key)


def create_tags(scan_result):
    if scan_result == 'Clean':
        return [
            {'Key': 'Status', 'Value': 'Clean'},
            {'Key': 'Scaned', 'Value': 'true'}
        ]
    else:
        return [
            {'Key': 'Status', 'Value': 'Infected'},
            {'Key': 'Scaned', 'Value': 'true'}
        ]
    
def tag_file_in_s3(bucket, key, tags):
    s3.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={
            'TagSet': [
                {
                    'Key': tag['Key'],
                    'Value': tag['Value']
                } for tag in tags
            ]
        }
    )

def scan_file_with_antivirus(file_path):
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    result = subprocess.run(['clamscan', file_path], capture_output=True)

    if result.returncode == 0:
        return 'Clean'
    else:
        return 'Infected'
    
def notify_email(file_path):
    ses.send_email(
        Source=from_email,
        Destination={
            'ToAddresses': to_email,
        },
        Message={
            'Subject': {
                'Data': f'File {file_path} has been scanned',
            },
            'Body': {
                'Text': {
                    'Data': f'File {file_path} has been scanned and found virus, please check the file and upload the clean file.',
                },
                'Html': {
                    'Data': "<h1> AKhilesh Mishra </h1>",
                }
            }
        }
    )
    

def main(Queue_url):
    bucket, key, s3_path, receipt_handle = read_sqs_queue(Queue_url)

    download_file_from_landing_s3(bucket, key, f"{locals_path}{key}")

    scan_result = scan_file_with_antivirus(f"{locals_path}/{key}")
    if scan_result == 'Clean':
        tag_file_in_s3(bucket, key, create_tags(scan_result))
        upload_file_to_clean_s3(clean_bucket, key, f"{locals_path}/{key}")
    else:       
        tag_file_in_s3(bucket, key, create_tags(scan_result))
        notify_email(s3_path)

    delete_message_from_queue(Queue_url, receipt_handle)


if __name__ == "__main__":
    main(Queue_url)


    # notify_email("/Users/akhilesh/somefile.pdf")

    # bucket, key, s3_path, receipt_handle = read_sqs_queue(Queue_url)

    # download_file_from_landing_s3(landing_bucket, key, f"{locals_path}{key}")

    # scan_result = scan_file_with_antivirus(f"{locals_path}/{key}")
    # if scan_result == 'Clean':
    #     tag_file_in_s3(landing_bucket, key, create_tags(scan_result))
    #     upload_file_to_clean_s3(clean_bucket, key, f"{locals_path}/{key}")
    # else:       
    #     tag_file_in_s3(landing_bucket, key, create_tags(scan_result))

    # delete_message_from_queue(Queue_url, receipt_handle)





    # scan_result = 'Infected'  # This should be the result of your antivirus scan
    # tags = create_tags(scan_result)
    # print(f"Tags to be applied: {tags}")
    # tag_file_in_s3(landing_bucket, key, tags)

    # upload_file_to_clean_s3(clean_bucket, key, f"{locals_path}{key}")




