#!/bin/bash

#Compile App
mkdir -p VLC-protocol-app/Contents/MacOS
OLDVER=11
CURVER=`sw_vers | grep ProductVersion | awk '{split($0, a, ":"); print a[2]}' | awk '{split($0, b, "."); print b[2]}'`
if [ $CURVER -gt $OLDVER ]
then
  gcc -framework Cocoa -o VLC-protocol-app/Contents/MacOS/vlc-protocol vlc-protocol-10.14.m
else
  gcc -framework Cocoa -o VLC-protocol-app/Contents/MacOS/vlc-protocol vlc-protocol-10.11.m
fi

#Add Icon File and Resource Directory 
mkdir VLC-protocol-App/Contents/Resources
curl -O https://mortis.moe/resources/siteicons/iconfile.icns
mv iconfile.icns VLC-protocol-App/Contents/Resources/iconfile.icns

curl -O https://raw.githubusercontent.com/mortsnake/vlc-protocol/master/mac/Info.plist
mv Info.plist VLC-protocol-App/Contents/.
