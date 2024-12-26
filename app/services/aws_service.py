import boto3
from botocore.exceptions import ClientError
from ..config import settings
from ..models import EC2Instance, InstanceState

class AWSService:
    def __init__(self):
        self.ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )

    def create_instance(self, instance_type: str, region: str) -> EC2Instance:
        try:
            response = self.ec2_client.run_instances(
                ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2 AMI ID
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1
            )
            
            instance = response['Instances'][0]
            return EC2Instance(
                instance_id=instance['InstanceId'],
                instance_type=instance['InstanceType'],
                state=InstanceState(instance['State']['Name']),
                region=region,
                public_ip=instance.get('PublicIpAddress'),
                private_ip=instance.get('PrivateIpAddress')
            )
        except ClientError as e:
            raise Exception(f"Failed to create EC2 instance: {str(e)}")

    def get_instance(self, instance_id: str) -> EC2Instance:
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            return EC2Instance(
                instance_id=instance['InstanceId'],
                instance_type=instance['InstanceType'],
                state=InstanceState(instance['State']['Name']),
                region=settings.aws_region,
                public_ip=instance.get('PublicIpAddress'),
                private_ip=instance.get('PrivateIpAddress')
            )
        except ClientError as e:
            raise Exception(f"Failed to get EC2 instance: {str(e)}")

    def update_instance(self, instance_id: str, instance_type: str = None, state: InstanceState = None) -> EC2Instance:
        try:
            if state:
                if state == InstanceState.STOPPED:
                    self.ec2_client.stop_instances(InstanceIds=[instance_id])
                elif state == InstanceState.RUNNING:
                    self.ec2_client.start_instances(InstanceIds=[instance_id])
                elif state == InstanceState.TERMINATED:
                    self.ec2_client.terminate_instances(InstanceIds=[instance_id])

            if instance_type:
                self.ec2_client.modify_instance_attribute(
                    InstanceId=instance_id,
                    InstanceType={'Value': instance_type}
                )

            return self.get_instance(instance_id)
        except ClientError as e:
            raise Exception(f"Failed to update EC2 instance: {str(e)}")

    def delete_instance(self, instance_id: str):
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
        except ClientError as e:
            raise Exception(f"Failed to delete EC2 instance: {str(e)}")
