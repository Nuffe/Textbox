import os
import sys
if sys.platform.startswith("linux"):
    session_type = os.environ.get("XDG_SESSION_TYPE")
    if session_type == "wayland":
        os.environ["SDL_VIDEODRIVER"] = "wayland"
        
from base import *   
import pygame
pygame.init()

def main():
    editor = TextEditor()
    editor.main()

if __name__ == "__main__":
    main()