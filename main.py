import requests
import yaml

def get_config_values():
    yaml_content = open('config.yaml', 'r')
    config = yaml.safe_load(yaml_content)

    username = config.get('username')
    password = config.get('password')
    url = config.get('url')
    domain = config.get('domain')

    return username, password, url, domain


def authenticate(username, password, url):
    auth_url = url + "/api/v1/auth/authenticate-user"
    auth_data = {'username': username, 'password': password}
    response = requests.post(auth_url, data=auth_data)
    access_info = response.json()
    return access_info['accessToken']


def listusers(access_token, url, domain):
    list_url = url + "/api/v1/settings/sysadmin/list-users/" + domain
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(list_url, headers=headers)
    users = response.json()
    return users


def extract_user_emails(users):
    email_addresses = []
    if 'userData' in users:
        for user in users['userData']:
            email = user.get('emailAddress')
            if email:
                email_addresses.append(email)
    return email_addresses


def expire_users_passwords(access_token, url, email_addresses):
    expire_url = url + "/api/v1/settings/domain/expire-users-passwords"
    headers = {'Authorization': 'Bearer ' + access_token}
    data = {'input': email_addresses}
    response = requests.post(expire_url, headers=headers, json=data)
    print(response.json())
    return response.json()


def get_primary_domain_admin(access_token, url, domain):
    primary_domain_admin_url = url + "/api/v1/settings/sysadmin/domain-admins/" + domain
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(primary_domain_admin_url, headers=headers)
    admins = response.json()
    if 'domainAdmins' in admins and len(admins['domainAdmins']) > 0:
        return admins['domainAdmins'][0]
    return None


def impersonate_user(access_token, url, email_address):
    impersonate_url = url + "/api/v1/settings/domain/impersonate-user"
    headers = {'Authorization': 'Bearer ' + access_token}
    data = {'email': email_address}
    response = requests.post(impersonate_url, headers=headers, data=data)
    impersonation_info = response.json()
    return impersonation_info['impersonateAccessToken']


if __name__ == '__main__':
    username, password, url, domain = get_config_values()
    access_token = authenticate(username, password, url)
    users = listusers(access_token, url, domain)
    email_addresses = extract_user_emails(users)
    primary_domain_admin = get_primary_domain_admin(access_token, url, domain)
    impersonation_token = impersonate_user(access_token, url, primary_domain_admin)
    for email_address in email_addresses:
        print("Expiring password for " + email_address)
        expire_users_passwords(impersonation_token, url, [email_address])
