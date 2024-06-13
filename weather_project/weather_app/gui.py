import tkinter as tk
#start a new window for my weather app
window = tk.Tk()
window.title("Weather App")
window.geometry("600x500")
window.configure(bg="gray")
#add a label to the window
label = tk.Label(window, text="Enter your city and state:", font=("Arial", 20), bg="gray")
label.pack()
#add an entry widget to the window
entry = tk.Entry(window, font=("Arial", 20))
entry.pack()
#add a button widget to the window
button = tk.Button(window, text="Get Weather", font=("Arial", 20), bg="green")
button.pack()
#add a label to the window
label = tk.Label(window, text="", font=("Arial", 20), bg="gray")
label.pack()
#start the event loop
# remove the border from the window
window.overrideredirect(True)
# make the window always on top
window.wm_attributes("-topmost", True)
# make the window transparent
window.wm_attributes("-alpha", 0.5)
#add a close wintdow button
close_button = tk.Button(window, text="Close", font=("Arial", 20), bg="red")  
close_button.pack()
#I need the close window button to close the window
def close_window():
    window.destroy()
close_button.config(command=close_window)

#add a label to the window
label = tk.Label(window, text="Weather Data", font=("Arial", 20), bg="gray")
label.pack()
#add a label to the window
label = tk.Label(window, text="City:", font=("Arial", 20), bg="gray")
label.pack()
#remove unnecessary code
window.mainloop()
