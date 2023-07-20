# Download

Check the Releases page.

This script relies on MTP-mount to work. As that program hasnt been updated to work with dokan 2.0++ you need an older version. The Setup file should install dokan by iteself.
Link to the latest supported release: https://github.com/dokan-dev/dokany/releases/tag/v1.5.1.1000

# Todo list: 

## First Priority
- Add Force Update to EXE.
## Second Priority

-  Reset settings
-  "About" section that contains version information for the program.
- Make the program prettier
- Error handling inside the program
- Give items background colors. # item.setBackground("black")
- Make it possible to translate the program to english and other languages.

## Third Priority

- Make sure Tab Order is correct in QtDesigner. As in the order of items to cycle thrugh when pressing TAB


# Building information:
(This is mostly for me)

How to create EXE and installer: 

python3 ./Installer/create_new_release.py

How to build EXE, Installer AND puiblish a new version: 
python3 ./Installer/create_new_release.py -exe -installer -publish

Also check the launch.json in the .vscode folder.

for build information check create_new_release.py in Installer folder.
