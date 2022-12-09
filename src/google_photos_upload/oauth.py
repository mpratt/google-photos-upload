import os
import json
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from requests_oauthlib import OAuth2Session

class OAuth:
    def __init__(self, credentials) -> None:
        self.session = None
        file = open(credentials, 'r')
        self.credentials_file = credentials
        self.credentials_data = json.load(file)
        self.token_file = "{}/{}.token".format(os.path.dirname(self.credentials_file), self.credentials_data['installed']['client_id'])

    def load_token(self):
        try:
            file = open(self.token_file, 'r')
            return json.load(file)
        except (json.JSONDecodeError, IOError):
            return None

    def save_token(self, token):
        file = open(self.token_file, 'w')
        file.write(json.dumps(token))
        file.close()

    def authorize(self):
        token = self.load_token()
        if token:
            now = datetime.now()
            expiration = token['expires_at']
            if datetime.timestamp(now) <= expiration:
                self.session = OAuth2Session(
                    self.credentials_data['installed']['client_id'],
                    token=token,
                    auto_refresh_url=self.credentials_data['installed']['token_uri'],
                    auto_refresh_kwargs= {
                        'client_id': self.credentials_data['installed']['client_id'],
                        'client_secret': self.credentials_data['installed']['client_secret']
                    },
                    token_updater=self.save_token,
                )

                return None

        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_file, scopes=[
                'https://www.googleapis.com/auth/photoslibrary'
            ]
        )

        flow.run_local_server(
            open_browser=False, bind_addr="0.0.0.0", port=8089
        )

        self.session = flow.authorized_session()
        oauth2_token = {
            "access_token": flow.credentials.token,
            "refresh_token": flow.credentials.refresh_token,
            "token_type": "Bearer",
            "scope": flow.credentials.scopes,
            "expires_at": flow.credentials.expiry.timestamp(),
        }

        self.save_token(oauth2_token)
        return None

    def make_request(self, method, path, data):
        return self.session.request(method, path, data = json.dumps(data))

    def make_upload(self, method, path, data):
        headers = {
            'Content-type': 'application/octet-stream',
            'X-Goog-Upload-Protocol': 'raw',
            'X-Goog-File-Name': os.path.basename(data)
        }

        file = open(data, 'rb')
        return self.session.request(method, path, data=file.read(), headers=headers)
