"""The file for downloading and uploading data file between S3 and local"""
import argparse
import logging.config

from src.s3 import upload_file_to_s3, download_file_from_s3

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('s3-pipeline')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', default=False, action='store_true',
                        help="Download the data from S3. If False, will upload data to S3")
    parser.add_argument('--s3_path', default='s3://2022-msia423-zhou-yihan/raw/bmw.csv',
                        help="s3 data path to download or upload data")
    parser.add_argument('--local_path', default='./data/raw/bmw.csv',
                        help="local data path to store or upload data")
    args: object = parser.parse_args()

    if args.download:
        download_file_from_s3(args.local_path, args.s3_path)
    else:
        upload_file_to_s3(args.local_path, args.s3_path)
