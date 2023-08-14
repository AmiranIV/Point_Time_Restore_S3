import sys
import boto3
from datetime import datetime, timezone


def check_versioning(bucket_name):
    s3 = boto3.client('s3')
    response = s3.get_bucket_versioning(Bucket=bucket_name)
    if 'Status' in response and response['Status'] == 'Enabled':
        return True
    else:
        return False


def find_previous_version(s3, bucket_name, object_key, timestamp):
    versions = s3.list_object_versions(Bucket=bucket_name, Prefix=object_key)['Versions']
    closest_version = None
    target_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

    for version in versions:
        if version['LastModified'] <= target_time:
            if closest_version is None or version['LastModified'] > closest_version['LastModified']:
                closest_version = version
    return closest_version


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python point_in_time_restore.py <bucket_name> <object_key> <timestamp>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    object_key = sys.argv[2]
    timestamp = sys.argv[3]

    s3 = boto3.client('s3')  

    if not check_versioning(bucket_name):
        print("Versioning is not enabled on the bucket.")
        sys.exit(1)

    previous_version = find_previous_version(s3, bucket_name, object_key, timestamp)

    if previous_version is None:
        print("No previous version found.")
        sys.exit(1)

    response = s3.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': object_key, 'VersionId': previous_version['VersionId']},
        Key=object_key
    )

    print("Object restored to previous version:", previous_version['VersionId'])
