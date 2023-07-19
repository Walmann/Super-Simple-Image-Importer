import argparse
import os
import re
import subprocess
import sys
import shutil
from github import Github
# import github 


def update_version_info(version_number, version_info_file):
    with open(version_info_file, "r") as f:
        content = f.read()
        content = re.sub(r'filevers=\([0-9]+, [0-9]+, [0-9]+, [0-9]+\)', f'filevers=({version_number.replace(".", ", ")})', content)
        content = re.sub(r'prodvers=\([0-9]+, [0-9]+, [0-9]+, [0-9]+\)', f'prodvers=({version_number.replace(".", ", ")})', content)
        content = re.sub(r"StringStruct\('FileVersion', '[0-9.]+.[0-9]+.[0-9]+.[0-9]+'\)", f"StringStruct('FileVersion', '{version_number}')", content)
        content = re.sub(r"StringStruct\('ProductVersion', '[0-9.]+.[0-9]+.[0-9]+.[0-9]+'\)", f"StringStruct('ProductVersion', '{version_number}')", content)


    with open(version_info_file, "w") as f:
        f.write(content)

def update_innosetup_version(version_number, innosetup_file):
    with open(innosetup_file, "r") as f:
        lines = f.readlines()

        # version_number = version_number.split(".")
        # version_number = f"{version_number[0]}.{version_number[1]}"
        for i, line in enumerate(lines):
            if line.startswith("AppVersion"):
                lines[i] = f"AppVersion={version_number}\n"
                break

    with open(innosetup_file, "w") as f:
        f.writelines(lines)

def run_pyinstaller(pyinstaller_settings_file, output_folder):
    # PyInstaller Test:
    import PyInstaller.__main__

    PyInstaller.__main__.run([
        "--noconfirm",
        "--name=SSII",
        f"--icon={current_working_dir}/src/Assets/icon.ico",
        "--console",
        "--clean",
        f"--version-file={version_info_file}",
        f"--distpath={current_working_dir}/Installer/Exe_Dest/",
        f"--add-data={current_working_dir}/src/Assets;Assets/",
        f"--add-data={current_working_dir}/src/ui;ui/",
        f"--add-data={current_working_dir}/src/bin;bin/",
        # "--add-data={current_working_dir}/.venv/Lib/site-packages;site-packages/",
        "--hidden-import=PySide6",
        f"{current_working_dir}/src/app.py"
    ])

    print()

    # # pyinstaller_command = f'pyinstaller --distpath "./Exe_Dest/" --workpath "./Exe_Build/" --noconfirm --onedir --windowed --icon f"{current_working_dir}/Assets/icon.ico" --name "SSII" --version-file "{version_info_file}" --add-data f"{current_working_dir}/Assets;Assets/" --collect-submodules "win32api" --add-data f"{current_working_dir}/ui;ui/" --add-data f"{current_working_dir}/bin;bin/"  f"{current_working_dir}/bin/importer.py"'
    # # pyinstaller_command = f'pyinstaller --distpath "./Installer/Exe_Dest/" --workpath "./Installer/Exe_Build/" --noconfirm --onedir --windowed --icon "./src/Assets/icon.ico" --name "SSII" --version-file "{version_info_file}" --add-data "./src/Assets;Assets/" --collect-submodules "win32api" --add-data "./src/ui;ui/" --add-data "./src/bin;bin/"  "./src/bin/importer.py"'
    # pyinstaller_command = f'pyinstaller --distpath "./Installer/Exe_Dest/" --workpath "./Installer/Exe_Build/" --noconfirm --onedir --windowed --icon f"{current_working_dir}/src/Assets/icon.ico" --name "SSII" --version-file f"{current_working_dir}/Installer/version_info.txt" --add-data f"{current_working_dir}/src/Assets;Assets/" --collect-submodules "win32api" --add-data f"{current_working_dir}/src/ui;ui/" --add-data f"{current_working_dir}/src/bin;bin/" --hidden-import "PySide6"  f"{current_working_dir}/src/app.py"'
    
    # subprocess.run(pyinstaller_command, shell=True)
        
    # # Delete contents of the output folder
    # if os.path.exists(output_folder):
    #     shutil.rmtree(output_folder)

    # # Move files to output folder
    # dist_folder = "./output/SSII"
    # if os.path.exists(dist_folder):
    #     shutil.move(dist_folder, output_folder)

def run_inno_setup(innosetup_file, inno_setup_exe):
    innosetup_command = f'"{inno_setup_exe}" {innosetup_file}'
    subprocess.run(innosetup_command, shell=True)

def check_inno_setup_in_path(inno_setup_exe):
    try:
        subprocess.run([inno_setup_exe, "/?"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        inno_setup_dir = r"C:\\Program Files (x86)\\Inno Setup 6"
        os.environ["PATH"] += os.pathsep + inno_setup_dir
        print("Inno Setup added to PATH. Please restart the terminal for the changes to take effect.")
        sys.exit(0)


def get_github_token(token_file):
    # Check if the token file exists
    if not os.path.exists(token_file):
        # Token file does not exist, prompt the user for the token
        github_token = input("Enter your GitHub personal access token (https://github.com/settings/tokens): ").strip()

        # Save the token to the token file
        with open(token_file, 'w+') as f:
            f.write(github_token)
    
    # Token file exists, read the token from the file
    with open(token_file, 'r') as f:
        github_token = f.read().strip()

    if len(github_token) >= 1:
        return Github(github_token)
    raise ValueError

def create_github_release(version_number, innosetup_file, github_token):

    g = github_token

    # Replace with your repository information
    repo_owner = "Walmann"
    repo_name = "SuperSimpleImageImporter"

    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # Create a new release
    release = repo.create_git_release(tag=version_number, name=version_number, message="This is an automated release.", draft=True)

    # Upload the Inno Setup file
    release.upload_asset(built_setup_file, label=f"SuperSimpleImageImporterV{version_number}.exe")

    # Publish the release
    release.update_release(draft=False, name=version_number, message="This is an automated release.")



parser = argparse.ArgumentParser(
        description="Download profiles from Instagram and Snapchat."
    )
parser.add_argument(
        "-exe", action="store_true", help="Only create the exe"
    )
parser.add_argument(
        "-installer", action="store_true", help="Only create the exe and the installer"
    )
parser.add_argument(
        "-publish", action="store_true", help="publish new version to GitHub and Users"
    )

args = parser.parse_args()
# Configuration
version_number = "0.3.1.0"
version_info_file = "./Installer/version_info.txt"
innosetup_file = "./Installer/createInstallerScript_innoSetup.iss"
pyinstaller_settings_file = "./Installer/AutoPyToExeSettings.json"
output_folder = "./Installer/Exe_Build"
inno_setup_exe = r"C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
built_setup_file = "./Installer/Setup_build/SuperSimpleImageImporterSetup.exe"
token_file = "./github_token.txt"
current_working_dir = f"{os.getcwd()}"




# Update version number in version_info.txt
update_version_info(version_number, version_info_file)

# Update version number in innosetup.iss
update_innosetup_version(version_number, innosetup_file)
if args.exe:
    # Run PyInstaller
    run_pyinstaller(pyinstaller_settings_file, output_folder)

if args.installer:
    # Run Inno Setup
    run_inno_setup(innosetup_file, inno_setup_exe)

if args.publish:
    github_token = get_github_token(token_file)
    create_github_release(version_number, innosetup_file, github_token)