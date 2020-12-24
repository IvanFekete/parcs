from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

pp = pprint.PrettyPrinter(indent=4)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/Users/ifekete/quiet-stacker-299415-af70e25e0801.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

results = service.files().list(pageSize=10,
                               fields="nextPageToken, files(id, name, mimeType)").execute()
nextPageToken = results.get('nextPageToken')
while nextPageToken:
        nextPage = service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, mimeType, parents)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
print(len(results.get('files')))
pp.pprint(results)


file_id = '1dBfng4rgzcKUewn1WsmylitzgG9bXB0p'
request = service.files().get_media(fileId=file_id)
filename = 'File.pdf'
fh = io.FileIO(filename, 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print ("Download %d%%." % int(status.progress() * 100))


folder_id = '1dvBsNXzAjKwjNvkfmff5ZJ8Jmuipzvxq'
name = 'Downloaded metodychka.pdf'
file_path = 'File.pdf'
file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
media = MediaFileUpload(file_path, resumable=True)
r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
pp.pprint(r)



# service.files().delete(fileId='18Wwvuye8dOjCZfJzGf45yQvB87Lazbzu').execute()
