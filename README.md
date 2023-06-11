# User Password Expiration Script

This script allows you to expire the passwords of users in a specific domain. It retrieves the necessary configuration values from a `config.yaml` file and uses the provided credentials to authenticate and perform actions on the target system.

## Prerequisites

- Python 3.x installed
- `requests` library installed (`pip install requests`)
- Configuration file (`config.yaml`) in the same directory as the script

## Configuration

1. Open the `config.yaml` file and update the following fields:
   - `username`: Your admin username for authentication.
   - `password`: Your admin password for authentication.
   - `url`: The URL of the target SmarterMail website.
   - `domain`: The domain for which you want to expire users' passwords.

## Usage

1. Install the required `requests` library if you haven't already: `pip install requests`.

2. Place the `config.yaml` file in the same directory as the script.

3. Run the script with the following command: `python main.py`.

4. The script will authenticate using the provided credentials and then list the users in the specified domain.

5. It will extract the email addresses of the users and expire their passwords one by one using impersonation.

6. The script will display the response for each user's password expiration.


Note: Please note that the script has been tested and works with SmarterMail Build 8559. However, use this script at your own risk. It is recommended to test it in a non-production environment before using it in a production setting. The author takes no responsibility for any issues or damages caused by the usage of this script.




