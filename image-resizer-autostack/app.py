import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download original
    img_obj = s3.get_object(Bucket=bucket, Key=key)
    img_data = img_obj['Body'].read()

    # Resize
    image = Image.open(io.BytesIO(img_data))
    resized_image = image.resize((300, 300))

    # Save back to buffer
    buffer = io.BytesIO()
    resized_image.save(buffer, format=image.format)
    buffer.seek(0)

    # Upload resized image
    resized_key = f"resized/{key}"
    s3.put_object(
        Bucket=bucket,
        Key=resized_key,
        Body=buffer,
        ContentType=img_obj["ContentType"]
    )

    return {"message": f"Resized image saved: {resized_key}"}

