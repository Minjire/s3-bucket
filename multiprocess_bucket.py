import boto3
from boto3 import session
from botocore.client import Config
import multiprocessing
import logging
from pathlib import Path

# ACCESS_ID = 'IGPKYQNRTQJ3JPRMCRRP'
# ACCESS_KEY = 'I9WaEh/s5CtQEQr4CCZZUZ4X0TJe1hKwTSWt4X68dVI'
# REGION = 'ams3'
# URL = 'https://ams3.digitaloceanspaces.com'
# PATH = 'ai-images-bucket/'

ACCESS_ID = 'PEDMJAWDGWVCCNUVCXZK'
ACCESS_KEY = '+cbk3hB5CEGnGzWeDtJtu9B7KW7pvlcMf/eAIp9SkhI'
REGION = 'sfo2'
URL = 'https://sfo2.digitaloceanspaces.com'
PATH = 'capital_ai-images-bucket/'

PATHS = []

s3 = boto3.resource('s3', region_name=REGION, endpoint_url=URL, aws_access_key_id=ACCESS_ID,
                    aws_secret_access_key=ACCESS_KEY)

my_bucket = s3.Bucket('capital')


# my_bucket = s3.Bucket('ai-images')


def get_paths():
    for s3_object in my_bucket.objects.all():
        filename = s3_object.key
        if 'var/www/capitalalliance/public/files/vehicles/vehicle_pics' in filename:
            # append to array
            PATHS.append(filename)
        else:
            pass


def download_all_files(path):
    print(path)
    dir = path.rsplit('/', 3)[-3]
    dir += '/'
    temp = path.rsplit('/', 1)[-1]

    try:
        print(f"\ndownloading...{path}\n")
        Path(PATH + dir).mkdir(parents=True, exist_ok=True)
        my_bucket.download_file(path, PATH + dir + temp)
        print("Success\n")
    except Exception as e:
        logging.error(f'FilePath: {path}', exc_info=True)
        print("Error encountered: %s" % e)


if __name__ == '__main__':
    get_paths()
    print(PATHS)
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    result = p.map(download_all_files, PATHS)
    print(result)
    p.close()
    p.join()
