import appdynamics
import boto3

s3_client = boto3.client("s3")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('abhiappdtest')
@appdynamics.tracer
def lambda_handler(event, context):
  bucket_name = event['Records'][0]['s3']['bucket']['name']
  s3_file_name = event['Records'][0]['s3']['object']['key']
  resp = s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
  data = resp['Body'].read().decode("utf-8")
  heroes = data.split("\n")
  for hero in heroes:
    print(hero)
    hero_data = hero.split(",")
    table.put_item(
      Item = {
            "id": hero_data[0],
            "name": hero_data[1],
            "location": hero_data[2]
        }
    )
