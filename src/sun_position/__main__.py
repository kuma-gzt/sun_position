"This is the entry point of the package"
import sys
from sun_position.gui import SunPathGUI


def main(args=None):
    """This is the entry point for the package"""
    if args is None:
        app = SunPathGUI()
        app.main_window.mainloop()


if __name__ == "__main__":
    sys.exit(main())