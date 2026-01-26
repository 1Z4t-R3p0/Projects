def handler(event, context):
    print("Image processing triggered")
    return {
        'statusCode': 200,
        'body': 'Processed'
    }
