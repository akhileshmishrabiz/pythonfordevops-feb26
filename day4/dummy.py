import boto3
import json

json_dict = """
{'MessageId': '1fcd33b6-273c-48e1-b08c-1b6ee76d1b33', 'ReceiptHandle': 'AQEBYTMkaN6vV2suIK0KSxEzvM+ayGfxrXish79bs1lv1IzNmAIBMFjESiAFQPnUa2zyBQGhxgrEJEdpOsUX8wu+z2YRZS2OyRQa5dwzJNTck7uuQ2o64z4fgg2ypaWXq252EnEJmdCgmVrbnyESY6NyoIY2tPJrGs6qJMKoT+PZngm2puI42Mw0zbCbkqgd9EWK4Wocs2kooc+XllGamUC8eCXuPzmPnxiE3ZSOiNi02Hli+spHLKtzDSZg5iPUoYbeG/XgdsUmKOBw1HICjSWngTlc57sLPFB5BsF2i/gkRSNGBg6tswNpWyJrxCcn+dTOUiCp7Yy8mw1xMciOdn3g+1HufHTj/dY0AUioYs0SoLbotVawKCmRSCVSepOaIHDESbCZjLD7IKG1T2KcvVObsA==', 'MD5OfBody': '529950eeeacea76aebfd1e1422999761', 'Body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"ap-south-1","eventTime":"2026-02-28T13:30:59.348Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"A168SSCSJWRKEO"},"requestParameters":{"sourceIPAddress":"122.161.50.181"},"responseElements":{"x-amz-request-id":"SYBR5YDYCNV1JPR2","x-amz-id-2":"1nibw70Sk0CYC52wXu/RitwbETGgPERpwkjGz9awVDKkuYVyanvcOxL651Hbv5TSSX8/ilwK3zuYJxkIsnYpOm12fJJs396Z"},"s3":{"s3SchemaVersion":"1.0","configurationId":"notoficyqueue","bucket":{"name":"landing-bucket-879381241087","ownerIdentity":{"principalId":"A168SSCSJWRKEO"},"arn":"arn:aws:s3:::landing-bucket-879381241087"},"object":{"key":"9107361_33.pdf","size":109107,"eTag":"7644897dc349b3b7a9a7238bcbaa77c8","sequencer":"0069A2EE1350971C62"}}}]}'}
"""
data = json.loads(json_dict)
bucket = data['Records'][0]['s3']['bucket']['name']
key = data['Records'][0]['s3']['object']['key']

print(f"Bucket: {bucket}")
print(f"Key: {key}")