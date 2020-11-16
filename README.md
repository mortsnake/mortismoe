# **MortIsMoe Files and Scripts for Web Streaming**

## **What is this?**
Scripts and Programs that I have created to be able to stream .mkv files from the web

Uses VLC and command-line parameters to pull the stream and play it from VLC

## **How does it work?**
For each system, the basic gist is that the scripts:
    * VLC is downloaded and installed from the official source repository (https://get.videolan.org/vlc/)
    * Scripts are run that change system values for URI handling (https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)
    * Add the handler for the vlc:// URI which will then be streamed to VLC via a Batch Script (Windows), or the Streaming App (MacOS)

Currently has not been developed for Linux systems

## **It doesn't work!**
Please send me a message.  I do not own a Mac that has a version higher than 10.11 (El Capitan) so there are some settings that are probably borked on newer versions.