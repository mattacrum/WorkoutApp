from tkinter import *
from tkinter.ttk import *
from pathlib import Path

# Path configurations
window_image = Path("Images/windowImage.png")

# Window property where everything is going to be inside of
window = Tk()

######### Window Configurations #########
# Set window size
window.geometry("500x500")
# Set window color
window.configure(bg='slateblue1')
# Set the window title
window.title("Punching Count App")
# Create image for title label
windowImage = PhotoImage(file = window_image)
# Setting icon of master window
window.iconphoto(False, windowImage)

mainloop()