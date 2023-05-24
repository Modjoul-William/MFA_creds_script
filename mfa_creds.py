import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class MFACreds:

    """
    Class to handle AWS authentication and generate temporary credentials from MFA
    """

    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(current_dir, 'temp.env')
        self.access_key = None
        self.secret_access_key = None
        self.session_token = None

    def obtain_temp_MFA_credentials(self):
        """
        Takes MFA code and obtains temporary credentials required to use boto3
        """

        mfa_code = input('What is your MFA code for getintoawsmodjoul?')

        try:
            sts_client = boto3.client('sts')
            # Identifier can be found in your security credentials in AWS account
            res = sts_client.get_session_token(SerialNumber = os.environ['IDENTIFIER'],
                                            TokenCode = mfa_code)
        except Exception as e:
            print("\nThere was an error obtaining credentials.\n")
            print(e)
            return None
        
        self.access_key = res['Credentials']['AccessKeyId']
        self.secret_access_key = res['Credentials']['SecretAccessKey']
        self.session_token = res['Credentials']['SessionToken']

        return True

    def create_AWS_connection(self, service, connection_type):
        """
        Create AWS client or resource using temp credentials

        Parameters:
        service (str): The name of the AWS service to connect. This should be 
                    a string like 's3', 'ec2', etc.
        connection_type (str): The type of connection. This should be either 'client' or 'resource'.
        """

        if connection_type == 'client':
            connection = boto3.client(
                service,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
                aws_session_token=self.session_token,
                region_name=os.getenv('AWS_DEFAULT_REGION')
            )
        elif connection_type == 'resource':
            connection = boto3.resource(
                service,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
                aws_session_token=self.session_token,
                region_name=os.getenv('AWS_DEFAULT_REGION')
            )
        else:
            raise ValueError(f"Invalid connection_type {connection_type}. Expected 'client' or 'resource'.")

        return connection

    def write_creds_to_file(self):
        """
        Writes temporary credentials obtained in obtain_temp_MFA_credentials to current file path
        """
        if self.access_key is not None:
            lines = [
                f"""AWS_ACCESS_KEY = '{self.access_key}'""",
                f"""AWS_SECRET_ACCESS_CODE = '{self.secret_access_key}'""",
                f"""AWS_SESSION_TOKEN = '{self.session_token}'""",
                """AWS_REGION = 'us-east-1'"""
                ]
            try:
                with open(self.file_path, 'w') as f:
                    for line in lines:
                            f.write(line)
                            f.write('\n')
            except Exception as e:
                print(f'There was an issue {e}')
            finally:
                f.close()
        else:
            return None
        
    def hello_world_test(self, client):
        """
        Method to verify that connection to aws services is working properly
        """
        for resp in client.list_objects(Bucket=os.getenv('AWS_BUCKET_NAME'), Prefix="2023/05")["Contents"]:
            file_name = client.get_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=resp['Key'])
            print(file_name)
            break # this will exit the loop after one iteration


def main():

    credentials = MFACreds()
    credentials.obtain_temp_MFA_credentials()
    client = credentials.create_AWS_connection('s3', 'client')

    credentials.hello_world_test(client)
    
if __name__ == '__main__':
    main()
