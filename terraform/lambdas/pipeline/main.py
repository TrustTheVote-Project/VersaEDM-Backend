def lambda_handler(event, context):
    import json
    modifiedFiles = event["commits"][0]["modified"]
    folderName = None
    # full path
    for filePath in modifiedFiles:
        # Extract folder name
        folderName = (filePath[:filePath.find("/")])
        break

    # start the pipeline
    if folderName:
        # Codepipeline name is foldername-job.
        # We can read the configuration from S3 as well.
        returnCode = start_code_pipeline(folderName + '-job')

    return {
        'statusCode': 200,
        'body': json.dumps('Modified project in repo:' + folderName)
    }


def start_code_pipeline(pipelineName):
    client = codepipeline_client()
    response = client.start_pipeline_execution(name=pipelineName)
    return True


cpclient = None


def codepipeline_client():
    import boto3
    global cpclient
    if not cpclient:
        cpclient = boto3.client('codepipeline')
    return cpclient