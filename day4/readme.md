Clamav scan 


Inbound/landing bucket  = landing-bucket-879381241087

Clan bucket = clean-bucket-879381241087

sqs queue (where we will notify uploads)

# Create bucket notification on sqs

```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ToSendMessage",
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "SQS:SendMessage",
      "Resource": "arn:aws:sqs:ap-south-1:879381241087:*",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "879381241087"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:::*"
        }
      }
    }
  ]
}
```