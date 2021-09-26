import sys
import json
import boto3
from botocore.exceptions import ClientError
from . import config


def status_instance(instance_id, dry_run=False):
    ec2 = boto3.client('ec2',
                       region_name='ap-northeast-1',
                       aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=config.AWS_SECRET_KEY)
    if (dry_run):
        try:
            ec2.describe_instance_status(
                Instance_Ids=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
            else:
                print(e)
    try:
        response = ec2.describe_instance_status(
            InstanceIds=[instance_id], DryRun=False)
        print(response)
        return response
    except ClientError as e:
        print(e)
        return ''


def start_instance(instance_id, dry_run=False):
    ec2 = boto3.client('ec2',
                       region_name='ap-northeast-1',
                       aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=config.AWS_SECRET_KEY)
    if (dry_run):
        # DryRunで確認
        try:
            ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
            else:
                print(e)

    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        return response
    except ClientError as e:
        print(e)
        return ''


def stop_instance(instance_id, dry_run=False):
    ec2 = boto3.client('ec2',
                       region_name='ap-northeast-1',
                       aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=config.AWS_SECRET_KEY)
    if (dry_run):
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
            else:
                print(e)

    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        return response
    except ClientError as e:
        print(e)
        return ''


def test():
    instance_id = 'i-xxxxxxxxxxxxxxxxx'
    ec2 = boto3.client('ec2',
                       region_name='ap-northeast-1',
                       aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=config.AWS_SECRET_KEY)
    try:
        response = ec2.describe_instance_status(
            InstanceIds=[instance_id], DryRun=False)
        print(response)

    except ClientError as e:
        print(e)


if __name__ == '__main__':
    test()
