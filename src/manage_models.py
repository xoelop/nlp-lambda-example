import argparse
import os
import tarfile
from pathlib import Path

import boto3
import requests

import settings

model = os.environ['SPACY_MODEL_MEDIUM']
model_sm = os.environ['SPACY_MODEL_SMALL']
dest = '/tmp/models'
s3_bucket = os.environ['S3_BUCKET']


def makedir_if_not_exists(dest):
    if not os.path.exists(dest):
        os.makedirs(dest)


def download_model_from_github(model: str, dest: str = '/tmp/models') -> str:
    print(f'Downloading {model} to {dest}')
    url = f'https://github.com/explosion/spacy-models/releases/download/{model}/{model}.tar.gz'

    makedir_if_not_exists(dest)
    filename = os.path.join(Path(dest), f'{model}.tar.gz')

    # download model
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    unzip_file(filename, dest)
    uncompressed_file = os.path.join(Path(dest), model)
    print(f'Downloaded to {uncompressed_file}')
    
    return uncompressed_file


def download_model_from_s3(model: str, dest: str) -> str:
    print(f'Downloading {model} from S3')
    makedir_if_not_exists(dest)
    filename = os.path.join(Path(dest), f'{model}.tar.gz')

    # download model
    object_name = f'models/{model}.tar.gz'
    s3 = boto3.client('s3')
    s3.download_file(s3_bucket, object_name, filename)

    unzip_file(filename, dest)
    uncompressed_file = os.path.join(Path(dest), model)
    print(f'Downloaded to {uncompressed_file}')

    return uncompressed_file


def unzip_file(filename: str, dest: str):
    print(f'Unzipping {filename}')
    with tarfile.open(filename) as f:
        f.extractall(path=dest)


def get_model_from_disk(model: str, dest: str = dest) -> str:
    print(f'Getting model {model} from disk')
    filename = os.path.join(Path(dest), model)
    if not os.path.exists(filename):
        print('Not in disk, downloading from S3 bucket')
        filename = download_model_from_s3(model, dest)
    dirname = model.split('-')[0]
    model_full_path = os.path.join(filename, dirname, model)
    return model_full_path


def upload_model_to_s3(model: str, location: str = dest, s3_bucket: str = s3_bucket):
    print(f'Uploading {model} from {location} to {s3_bucket} S3 bucket')
    file_full_path = os.path.join(Path(location), f'{model}.tar.gz')
    if not os.path.exists(file_full_path):
        print('File not in disk, downloading from GitHub')
        download_model_from_github(model, dest=location)
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_full_path, s3_bucket, f'models/{model}.tar.gz')
    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Spacy models to disk and upload them to S3')
    parser.add_argument('--download', '-d', action='store_true')
    parser.add_argument('--upload', '-u', action='store_true')

    args = parser.parse_args()

    if args.download:
        download_model_from_github(model=model_sm)
    if args.upload:
        upload_model_to_s3(model=model_sm)

    # download_model_from_github(model=model)
    # get_model_from_disk(model_sm, dest=f'{dest}/test_S3')
