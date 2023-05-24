# Download

Check the Releases page: 


# Building information:
(This is mostly for me)

pyinstaller 
--noconfirm 
--onefile 
--console 
--icon "C:/WORKFOLDER/Super_Simple_Image_Importer/Assets/icon.ico" 
--add-data "C:/WORKFOLDER/Super_Simple_Image_Importer/Assets;app/Assets/" 
--add-data "C:/WORKFOLDER/Super_Simple_Image_Importer/importer.py;app/" 
--add-data "C:/WORKFOLDER/Super_Simple_Image_Importer/mainWindow.ui;app/"  "C:/WORKFOLDER/Super_Simple_Image_Importer/setup.py"

<!-- Build EXE: ```python setup.py build_exe```

Build MSI: ```python setup.py bdist_msi``` -->