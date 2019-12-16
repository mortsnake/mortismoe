import os
import winreg
import time
import re
import urllib.request
import webbrowser
import hashlib
import ctypes

if not ctypes.windll.shell32.IsUserAnAdmin():
    print("This program will not work as this user.  Please re-run as Administrator!")
    time.sleep(1)
    input("\nPress Enter to exit.")
    exit()

def fileHash(filepath):
    md5_hash = hashlib.md5()
    with open(filepath,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()

userinput = input("\nDo you already have VLC installed on your computer?  (If you do, or would not like to update enter 'Y') [y/N]: ")
userinput = userinput.strip().lower()
if userinput == "yes" or userinput == "y" or userinput == "ye":
    print("Skipping VLC install, please note that if you DO NOT have this program you WILL NEED IT before running this program!\n")
else:
    # First install the latest version of VLC Player
    print("Installing VLC from source")
    url = 'https://get.videolan.org/vlc/'
    page = urllib.request.urlopen(url)
    itemsArr = []
    cwd = os.getcwd()
    filenameFormatted = ""



    i = 1
    for line in page:
        itemsArr.append(line.decode("utf-8"))

    for i in range (len(itemsArr)-1, 0, -1):
        if (re.search(r'"\d+\.\d+\.\d+', itemsArr[i])):
            vCheck = itemsArr[i].split("\"")
            baseVer = vCheck[1].split("/")[0]
            filenameFormatted = "vlc-{}-win64.exe".format(baseVer)
            urlFormatted = "{}{}win64/{}".format(url, vCheck[1], filenameFormatted)

            print("Downloading version: {}".format(filenameFormatted))
            
            urllib.request.urlretrieve(urlFormatted, cwd+'\\'+filenameFormatted)
            urllib.request.urlretrieve(urlFormatted, cwd+'\\'+filenameFormatted+".md5")
            break
            

    print("Downloaded VLC File!")
    # Calculate MD5 Hash of File just downloaded
    print("MD5 Hash Sum of VLC Install File:",fileHash(cwd+'\\'+filenameFormatted))
    print("Please check",cwd+'\\'+filenameFormatted+".md5 for the MD5 Sum provided by VideoLan")
    print("Installing VLC now, please follow the prompts in the next window!")
    while (os.system(cwd+'\\'+filenameFormatted)):
        pass
    print("VLC has been installed!")


# Next find the directory that VLC was installed to
print("Now searching for directory VLC is installed in...")
dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]
vlcpath = ""

print("Searching...")

try:
    for drive in drives:
        if vlcpath == "":
            for root, dirs, files in os.walk(drive+"\\"):
                if vlcpath == "":
                    for file in files:
                        if file == "vlc.exe":
                            vlcpath = os.path.join(root, file)
                            tArr = vlcpath.split("\\")
                            tArr.pop()
                            vlcpath = "\\".join(tArr)+"\\"
                            break
                else: 
                    break
        else: 
            break
except:
    print("There was an error with this install.  Please ensure VLC is installed, and then re-run as Administrator!")
    input("\nPress Enter to exit.")
    exit()




if (vlcpath == ""):
    print("Couldn't find VLC installed on your system!  Please ensure it is installed correctly!")
    input("\nPress Enter to exit.")
    exit()
else:
    print("Found VLC!")

with open(vlcpath+"MortIsMoe.bat", "w") as file:
    file.write("Setlocal EnableDelayedExpansion\n")
    file.write("set url=%~1\n")
    file.write("set url=!url: =%%20!\n")
    file.write(r'start "VLC" "'+vlcpath+'vlc.exe" --open "%url:~6%"\n')

print("Setting system variables...")

subkeyTOP = r'vlc'
subkeyICO = r'vlc\DefaultIcon'
subkeyCMD = r'vlc\shell\open\command'
subkeyNAME = r'SOFTWARE\Classes\Applications\MortIsMoe.bat'

try:
    hKeyTOP = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, subkeyTOP)
    hKeyICO = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, subkeyICO)
    hKeyCMD = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, subkeyCMD)
    hKeyNAME = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, subkeyNAME)

    winreg.SetValueEx(hKeyTOP, None, 0, winreg.REG_SZ, "URL:vlc Protocol")
    winreg.SetValueEx(hKeyTOP, "URL Protocol", 0, winreg.REG_SZ, "")

    winreg.SetValueEx(hKeyICO, None, 0, winreg.REG_SZ, "\""+vlcpath+"vlc.exe\",0")

    winreg.SetValueEx(hKeyCMD, None, 0, winreg.REG_SZ, "\""+vlcpath+"MortIsMoe.bat\" \"%1\"")

    winreg.SetValueEx(hKeyNAME, None, 0, winreg.REG_SZ, "")
    winreg.SetValueEx(hKeyNAME, "FriendlyAppName", 0, winreg.REG_SZ, "VLC media player")

    print("Set all keys successfully")
except WindowsError:
    print("Couldn't set standard toolbar keys.  Please Re-Run as administrator.")
    input("\nPress Enter to exit.")
    exit()

print("All set!  Enjoy the website!")

webbrowser.open_new_tab("https://www.mortis.moe/downloadauth.php")
time.sleep(4)

input("\nPress Enter to Quit")