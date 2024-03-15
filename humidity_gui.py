from tkinter import *

root = Tk()
root.title('Humidity Checker')

main_title = Label(root, text='Humidity Checker', width=50, bg='yellow')
main_title.pack()

status = Label(root, text='Humidity Status', width=25, bg='green')
status.pack()

soil_humidity = Label(root, text='Soil Humidity', width=25, bg='green')
soil_humidity.pack()

limits = Label(root, text='Set Limits', width=25, bg='green')
limits.pack()

# drop_down down boxes 
clicked = StringVar()
clicked.set('Choose Percentage')
dry_drop_down = OptionMenu(root, clicked, "0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%" )
dry_drop_down.pack()

humid_drop_down= OptionMenu(root, clicked, "0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%" )
humid_drop_down.pack()

root.mainloop()