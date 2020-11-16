#!/bin/bash

#Check if VLC is installed.  Then, get the latest VLC install .dmg file if needed
echo ""
echo "Working on VLC app:"
if [ -d /Applications/VLC.app ]  
then
  echo "    VLC is already installed!  Skipping this step..."
else
  echo "    Downloading..."
  cd ~/Downloads
  if [ ! -f vlc-3.0.8.dmg ]
  then
    curl -O https://videolan.mirrors.hivelocity.net/vlc/3.0.8/macosx/vlc-3.0.8.dmg > mim_installer.log 2>&1
  fi
  #Need to mount and install the dmg file:
  hdiutil mount vlc-3.0.8.dmg >> mim_installer.log 2>&1
  echo "    Installing...  This might take a second!"
  cp -r /Volumes/VLC\ media\ player/VLC.app /Applications/VLC.app
  echo "    Cleaning up..."
  hdiutil unmount /Volumes/VLC\ media\ player
  echo "    VLC complete!"
fi

#Disable some stupid security settings
#Allow Apps from Anywhere
spctl --master-disable
#Whitelist VLC
spctl --add /Applications/VLC.app

#First get the repo, git should be installed on OSX by default
echo ""
echo "Working on VLC-Protocol association:"
if [ ! -d /tmp/vlc-protocol ]
then
  git clone https://github.com/mortsnake/vlc-protocol.git /tmp/vlc-protocol >> mim_installer.log 2>&1
fi

#CD into dir, run the build script.  This should compile successfully
cd /tmp/vlc-protocol/mac
echo "    Building..."
./build.sh 

#Copy app into Applications dir
echo "    Installing..."
cp -r /tmp/vlc-protocol/mac/VLC-protocol-app /Applications/MortIsMoe\ Streaming.app
#Whitelist app
spctl --add /Applications/MortIsMoe\ Streaming.app
echo "    VLC-Protocol Add-On Complete"

#Will remove all downloaded files and stuff to free up space
echo ""
echo "Working on cleaning up loose files..."
rm -rf /tmp/vlc-protocol
echo "    Clean-up complete!"

#Instruct user to complete some instructions
echo ""
echo ""
echo "In a second, your web browser will open up."
sleep 1
echo "  -Safari has issues and might not work correctly."
sleep 1
echo "  -I would recommend using Chrome or Firefox in general, anyways."
sleep 2
echo ""
echo "  -Just press enter if you don't want to download any new browsers," 
echo "   or if you already have another browser"
echo ""
echo "    1) Download Firefox"
echo "    2) Download Chrome"
echo "    3) Don't download anything new (default)"
echo ""

read -p "    Make Choice or Press Enter To Do Nothing: " ANSWER

case "$ANSWER" in 
  [1]|[Ff]*) 
    open https://ftp.mozilla.org/pub/firefox/releases/75.0b9/mac/en-US/Firefox%2075.0b9.dmg
    #Mount and install here
    read -p "Press enter after Firefox is done installing..." STALLING
    open -a /Applications/Firefox.app https://mortis.moe/downloadauth.php
    ;;
  [2]|[Cc]*)
    open https://www.google.com/chrome/thank-you.html?brand=CHBD&statcb=0&installdataindex=empty&defaultbrowser=0#
    read -p "Press enter after Chrome is done installing..." STALLING
    open -a /Applications/Google\ Chrome.app https://mortis.moe/downloadauth.php
    ;;
  *)
    open https://mortis.moe/downloadauth.php
    ;; 
esac
    
echo ""
echo "" 
echo "All set!  Please contact Mort if you have any questions"
