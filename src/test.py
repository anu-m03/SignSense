import winreg
import os
import glob 

# reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")

# downloads_path = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]

# winreg.CloseKey(reg_key)

# print(downloads_path)


downloadsFolder = '../../Downloads/' + "*.xlsx"
list_of_files = glob.glob(downloadsFolder)
latest_file = max(list_of_files, key=os.path.getctime)
#do something;
# file_content = pandas.read_excel(latest_file)