from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from glob import glob
import os
import ntpath


def filter_most_recent_files(files: list, n: int):
    sorted_file_time_list = sorted(files, key=os.path.getmtime)
    return sorted_file_time_list[-n:]


def upload_files():
    file_list = glob(SAVES_FOLDER)
    recent_file_list = filter_most_recent_files(file_list, 5)
    for file_path in recent_file_list:
        file = drive.CreateFile({'parents': [{'id': DRIVE_FOLDER_ID}], 'title': ntpath.basename(file_path)})
        file.SetContentFile(file_path)
        file.Upload()
        print(f"Arquivo {ntpath.basename(file_path)} salvo no drive")
    print("Todos os arquivos foram salvos no google drive")


def clean_folder():
    file_list = drive.ListFile({'q': f"'{DRIVE_FOLDER_ID}' in parents and trashed=false"}).GetList()
    for file in file_list:
        file.Delete()
    print("Arquivos deletados do google drive")


if __name__ == '__main__':

    DRIVE_FOLDER_ID = '1vyXexEHdgwLLgeSwLdbD8jOea5B4wzdi'
    SAVES_FOLDER = 'C:/Users/allan/Documents/My Games/Fallout4/Saves/' + '*.fos'

    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("credentials.txt")
    if gauth.credentials is None:
        print("Ainda não autenticado")

        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})

        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        print("O token expirou")
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.txt")
    drive = GoogleDrive(gauth)

    clean_folder()
    upload_files()
    print("Fim do programa")
    exit(0)
