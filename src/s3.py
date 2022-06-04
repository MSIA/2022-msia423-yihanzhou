"""Upload or download data between AWS S3 and local files ."""
import logging.config
import re
import typing

import boto3
import botocore

logger = logging.getLogger(__name__)


def parse_s3(s3path: str) -> typing.Tuple[str, str]:
    """
    Parse the s3 path to get both the bucket name and the path name

    Args:
        s3path (str): input for the s3 path

    Returns:
         s3bucket (str): the s3 bucket name
         s3path (str): the s3 path
    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    match = re.match(regex, s3path)
    s3bucket = match.group(1)
    s3path = match.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path: str, s3path: str) -> None:
    """
    Upload the file from the local path to s3

    Args:
        local_path (str): the path of the local data
        s3path (str): the path to where the data will be stored in s3

    Returns: None
    """
    s3bucket, s3_just_path = parse_s3(s3path)

    s3_boto = boto3.resource("s3")
    bucket = s3_boto.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and '
                     'AWS_SECRET_ACCESS_KEY env variables.')
    except FileNotFoundError:
        logger.error('The local path does not have the dataset file')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)


def download_file_from_s3(local_path: str, s3path: str) -> None:
    """
    Download the file from s3 to local

    Args:
        local_path (str): the local path for storing the downloaded dataset from s3
        s3path (str): the s3 path that the data will be downloaded

    Returns: None
    """
    s3bucket, s3_just_path = parse_s3(s3path)

    s3_boto = boto3.resource("s3")
    bucket = s3_boto.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
        logger.info('Data begin to download')
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID '
                     'and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data downloaded from %s to %s', s3path, local_path)
