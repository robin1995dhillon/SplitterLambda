import os
import shutil
from urllib.parse import unquote_plus

import boto3
from spleeter.separator import Separator

s3_client = boto3.client('s3')

def split_music(src_file, des_dir):
    if __name__ == '__main__':
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(src_file, des_dir)

split_music("source/1.mp3","dest")

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        src_file = '/tmp/src/{}'.format(tmpkey)
        s3_client.download_file(bucket, key, src_file)
        des_dir = '/tmp/des/'
        split_music(src_file, des_dir)

        output_path = '/tmp/des/{}'.format(os.path.splitext(tmpkey)[0])
        upload_path = output_path+'.zip'
        shutil.make_archive(upload_path, 'zip', output_path)
        s3_client.upload_file(upload_path, '{}-processed'.format(bucket), key)