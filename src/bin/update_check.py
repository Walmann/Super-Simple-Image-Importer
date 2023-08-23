import requests
import sys
import win32api
from bin.debug_write import isDebug, writeDebug
def get_local_version_info(exe_path):
    info = win32api.GetFileVersionInfo(exe_path, '\\')
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    version = f'{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}'
    return version



def check_for_updates():
    # Check local version
    exe_path = sys.executable
    version_info_local = get_local_version_info(exe_path)
    writeDebug(f'Local Version: {version_info_local}')
    


    # Check Github Version:
    repo_url = 'https://github.com/Walmann/SuperSimpleImageImporter'
    api_url = repo_url.replace('github.com', 'api.github.com/repos') + '/releases/latest'
    response = requests.get(api_url)
    data = response.json()
    version_info_remote = data['tag_name']
    writeDebug(f'Remote Version: {version_info_remote}')
    
    # Avgjør om det skal oppdateres eller ikke.
    if version_info_remote != version_info_local:
        # print(f'En nyere versjon ({latest_version}) er tilgjengelig på GitHub.')
        return [True, version_info_local, version_info_remote]
    else:
        # print(f'Du har allerede den siste versjonen ({current_version}).')
        return [False, version_info_local, version_info_remote]
# check_for_updates()