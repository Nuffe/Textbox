import os
if "WAYLAND_DISPLAY" in os.environ:
        del os.environ["WAYLAND_DISPLAY"]
        os.environ["DISPLAY"] = ":0"
        
from base import *       

def main():
    editor = TextEditor()
    editor.main()

if __name__ == "__main__":
    main()