import boto3
from boto3 import session
from botocore.client import Config
import logging
from colors import color
from pathlib import Path

ACCESS_ID = ''
ACCESS_KEY = ''
REGION = 'ams3'
URL = 'https://ams3.digitaloceanspaces.com'
PATH = ''

s3 = boto3.resource('s3', region_name=REGION, endpoint_url=URL, aws_access_key_id=ACCESS_ID,
                    aws_secret_access_key=ACCESS_KEY)
my_bucket = s3.Bucket('ai-images')


def download_all_files():
    error_count = 0
    file_count = 0
    for s3_object in my_bucket.objects.all():
        filename = s3_object.key
        dir = ''
        if '/' in filename:
            dir = filename.rsplit('/')[0]
            dir += '/'
            filename = filename.rsplit('/', 1)[-1]
            print(dir)
        try:
            print(color("%s \ndownloading...\n" % filename, fg='blue'))
            Path(PATH + dir).mkdir(parents=True, exist_ok=True)
            my_bucket.download_file(s3_object.key, PATH + dir + filename)
            print(color("Success\n", fg="lime"))
            file_count += 1
        except Exception as e:
            logging.error(f'FilePath: {filename}', exc_info=True)
            error_count += 1
            print(color("Error encountered: %s" % e, fg="#ff1a1a"))
            continue

    print(color("Total number of files downloaded: %d.\n" % file_count, fg="lime"))


download_all_files()


# my_bucket.upload_file('image1.jpg', 'image1.jpg')
def upload_file():
    sesn = session.Session()
    client = sesn.client('s3', region_name=REGION, endpoint_url=URL, aws_access_key_id=ACCESS_ID,
                         aws_secret_access_key=ACCESS_KEY)
    client.upload_file('test2.txt', 'ai-images', 'uploaded/test2.txt')

# upload_file()
