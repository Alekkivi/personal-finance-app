from login import *
from main_menu import *


try:
    user = LoginWindow()
    username = user.username
    if not username:
        quit()
    else:
        MainMenuWindow(username)

except AttributeError:
    pass

# menu = MainMenuWindow('TOIMII')