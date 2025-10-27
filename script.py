import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=8000)

# Save the credentials for later use
with open('token.pkl', 'wb') as token:
    pickle.dump(creds, token)

print("Token saved as token.pkl")
