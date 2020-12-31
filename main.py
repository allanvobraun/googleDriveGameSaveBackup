from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from glob import glob
import os
import ntpath
import warnings
warnings.filterwarnings("error")

DRIVE_FOLDER_ID = '1vyXexEHdgwLLgeSwLdbD8jOea5B4wzdi'
SAVES_FOLDER = 'C:/Users/allan/Documents/My Games/Fallout4/Saves/' + '*.fos'

gauth = GoogleAuth()

try:
    gauth.LoadCredentialsFile("credentials.txt")
except UserWarning:
    warnings.filterwarnings("ignore")
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile("credentials.txt")

warnings.filterwarnings("ignore")

drive = GoogleDrive(gauth)


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
    print("Novos arquivos salvos no google drive")


def clean_folder():
    file_list = drive.ListFile({'q': f"'{DRIVE_FOLDER_ID}' in parents and trashed=false"}).GetList()
    for file in file_list:
        file.Delete()
    print("Arquivos deletados do google drive")


if __name__ == '__main__':
    clean_folder()
    upload_files()
