#!/bin/sh

# Note: On some distros like Arch linux x-terminal-emulator does not exist.
# Therefor you must either replace it with your preferred terminal emulator
# or link it to /usr/bin/x-terminal-emulator:
# 
# sudo ln -s your-terminal-here /usr/bin/x-terminal-emulator
# sudo chmod +x /usr/bin/x-terminal-emulator 

x-terminal-emulator -e "python pubmusic.py"