from tkinter import *

root = Tk()
root.title('Humidity Checker')
root.geometry('700x900')

test_var = 30

class humidity_checker_gui:
    
    def __init__(self, main): #main==root
        frame = Frame(main)
        frame.grid()
        
        # GUI code starts
      
        # pie chart and percentages
        self.soil_humidity = Label(main, text='Soil Humidity', bg='green')
        self.soil_humidity.grid(row=1, columnspan=2)
        
        self.pie_chart = Label(main, text='test pie', bg='green')
        self.pie_chart.grid(row=2, rowspan=2)
        
        self.soil_percentage_dry = Label(main, text='Dry', bg='green')
        self.soil_percentage_dry.grid(row=2, column=1)
        
        self.soil_percentage_humid = Label(main, text='Humid', bg='green')
        self.soil_percentage_humid.grid(row=3, column=1)
        
        # status, user take action
        self.status = Label(main, text='Humidity Status', bg='green')
        self.status.grid(row=4, column=0, columnspan=2)

        self.add_water = Label(main, text='ADD WATER', bg='green')
        self.add_water.grid(row=5 ,column=0)

        self.less_water = Label(main, text='LESS WATER', bg='green')
        self.less_water.grid(row=5, column=1)

        self.desired_conditions = Label(main, text='Desired Conditions', bg='green')
        self.desired_conditions.grid(row=5, column=2)
        
        # drop_down down boxes 
        self.limits = Label(main, text='Set Limits', bg='green')
        self.limits.grid(row=6, column=0, columnspan=3)

        self.clicked = StringVar()
        self.clicked.set('Choose Percentage')
        self.percentages = [ 
                        '0%', 
                        '10%', 
                        '20%', 
                        '30%', 
                        '40%', 
                        '50%', 
                        '60%', 
                        '70%', 
                        '80%', 
                        '90%', 
                        '100%'
        ]

        self.dry_drop_down = OptionMenu(main, self.clicked, *self.percentages)
        self.dry_drop_down.grid(row=7, column=0)

        self.divider = Label(main, text='-', bg='orange')
        self.divider.grid(row=7, column=1)

        self.humid_drop_down= OptionMenu(main, self.clicked, *self.percentages) #change automatically according to dry percentage
        self.humid_drop_down.grid(row=7, column=3)
        # GUI code ends
        
        # functional code begins
        
        
        # functional code ends

gui_class = humidity_checker_gui(root)
root.mainloop()