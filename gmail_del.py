from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    total_num_unread = 0
    page_num = 1
    response = service.users().messages().list(userId='me', q='in:inbox is:unread').execute()
    to_trash_ids = []
    while 'nextPageToken' in response:
        print(f'page number: {page_num}')
        messages = response['messages']
        to_trash_ids.extend(msg['id'] for msg in messages)
        # total_num_unread += len(response['messages'])
        next_page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q='in:inbox is:unread', pageToken=next_page_token).execute()
        page_num += 1
    print(f'num ids collected: {len(to_trash_ids)}')
    for msg_id in to_trash_ids:
        service.users().messages().trash(userId='me', id=msg_id).execute()
        print(f'trashed {msg_id}')

    # print(f'num unread: {total_num_unread}')

    #for msg in response['messages']:
        #print(msg)
#    labels = results.get('labels', [])
#
#    if not labels:
#        print('No labels found.')
#    else:
#        print('Labels:')
#        for label in labels:
#            print(label['name'])

if __name__ == '__main__':
    main()