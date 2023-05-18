# MFACreds

This Python class is used to handle AWS authentication and generate temporary credentials from Multi-Factor Authentication (MFA).

## Class Methods

Below are the methods included in the `MFACreds` class.

### `__init__(self)`

This method initializes the MFACreds class. It sets up the `file_path`, `access_key`, `secret_access_key`, and `session_token` attributes.

### `obtain_temp_MFA_credentials(self)`

This method prompts the user for an MFA code and uses it to obtain temporary AWS credentials.

### `create_AWS_connection(self, service, connection_type)`

This method creates either an AWS client or resource using the temporary credentials. The service parameter should be a string indicating the AWS service to connect to (e.g., 's3', 'ec2', etc.), and the connection_type should be either 'client' or 'resource'.

### `write_creds_to_file(self)`

This method writes the temporary AWS credentials to a file at the specified `file_path`.

### `hello_world_test(self)`

This method is used to verify that the connection to AWS services is working properly. It prints the first object from the specified AWS S3 bucket and prefix.

## Usage

Here's an example of how to use the MFACreds class:

```python
credentials = MFACreds()
credentials.obtain_temp_MFA_credentials()
credentials.hello_world_test()
```

This will create an instance of the MFACreds class, use it to prompt for an MFA code and obtain temporary AWS credentials, and then verify that these credentials work by printing the first object from a specified AWS S3 bucket and prefix.

Remember to set up the appropriate environment variables and/or replace the placeholders in the above script to match your actual AWS setup.

## Environment Variables

You'll need to setup the following environment variables in your `.env` file:

```
AWS_ACCESS_KEY_ID = 'Your Access Key ID Here'
AWS_SECRET_ACCESS_KEY = 'Your Secret Access Key Here'
AWS_DEFAULT_REGION = 'Your Default AWS Region Here'
AWS_BUCKET_NAME = 'Your AWS S3 Bucket Name Here'
IDENTIFIER = 'Your MFA Identifier Here'
```

Ensure that these environment variables match your actual AWS configuration.
