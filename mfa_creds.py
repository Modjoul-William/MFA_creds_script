import boto3
import os
from dotenv import load_dotenv

class MFACreds:

    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(current_dir, 'temp.env')
        self.access_key = None
        self.secret_access_key = None
        self.session_token = None

    def obtain_MFA_credentials(self):
        """
        Takes MFA code and obtains temporary credentials required to use boto3
        """

        TokenCode = input('What is your MFA code for getintoawsmodjoul?')

        sts_client = boto3.client('sts')
        res = sts_client.get_session_token(SerialNumber = os.getenv['IDENTIFIER'],
                                           TokenCode = TokenCode)
        
        access_key = res['Credentials']['AccessKeyId']
        secret_access_key = res['Credentials']['SecretAccessKey']
        session_token = res['Credentials']['SessionToken']

        print(f"\nAccess Key: {access_key}\n")
        print(f"secret_access_key: {secret_access_key}\n")
        print(f"session_token: {session_token}\n")

        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.access_key = session_token

    def write_creds_to_file(self):
        """
        Writes temporary credentials obtained in obtain_MFA_credentials to current file path
        """
        lines = [
            f"""AWS_ACCESS_KEY = '{self.access_key}'""",
            f"""AWS_SECRET_ACCESS_CODE = '{self.secret_access_key}'""",
            f"""AWS_SESSION_TOKEN = '{self.session_token}'""",
            """AWS_REGION = 'us-east-1'"""
            ]
        with open(self.file_path, 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

def main():
    load_dotenv()

    credentials = MFACreds()
    credentials.obtain_MFA_credentials()
    credentials.write_creds_to_file()

if __name__ == '__main__':
    main()