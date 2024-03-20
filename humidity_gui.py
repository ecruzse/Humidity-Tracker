from tkinter import *
# import customtkinter

root = Tk()
root.title('Humidity Checker')
root.configure(background='#212222')
# root.geometry('700x500')

test_var = 30
LABEL_COLOR = '#9ea1a2'
BUTTON_COLOR = '#1167b1'
WARNING_LABEL = '#eed202'
WARNING_LABEL2 = '#ff9966'
BALANCED_LABEL = '#339900' #00FF00

class humidity_checker_gui:
    
    def __init__(self, main): #main==root
        frame = Frame(main)
        frame.grid()
        TEMP_DRY_VAL = '30%'
        TEMP_HUM_VAL = '70%'
        TEMP_DRY_LIMIT = ''
        TEMP_DRY_LIMIT = ''
   
        # functional code begins
        def display_required_action(desired_percentage):
            desired_float_percentage = float(desired_percentage.strip('%'))
            float_dry_value =  float(TEMP_DRY_VAL.strip('%'))

            if  float_dry_value > desired_float_percentage:
                print(f'{TEMP_DRY_VAL} {desired_percentage} success')
                self.less_water.grid(row=5, column=1)
            elif float_dry_value < desired_float_percentage:
                self.add_water.grid(row=5 ,column=0)
            else:
                self.desired_conditions.grid(row=5, column=2)

        # functional code ends



        # GUI code starts
      
        # pie chart and percentages
        self.soil_humidity = Label(main, text='Soil Humidity', bg=LABEL_COLOR)
        self.soil_humidity.grid(row=1, columnspan=2)
        
        self.pie_chart = Label(main, text='test pie', bg=LABEL_COLOR)
        self.pie_chart.grid(row=2, rowspan=2)
        
        self.soil_percentage_dry = Label(main, text='Dry', bg=LABEL_COLOR)
        self.soil_percentage_dry.grid(row=2, column=1)
        
        self.soil_percentage_humid = Label(main, text='Humid', bg=LABEL_COLOR)
        self.soil_percentage_humid.grid(row=3, column=1)
        
        # status, user take action
        self.status = Label(main, text='Humidity Status', bg=LABEL_COLOR)
        self.status.grid(row=4, column=0, columnspan=2)

        self.add_water = Label(main, text='ADD WATER', bg=WARNING_LABEL)
        # self.add_water.grid(row=5 ,column=0)

        self.less_water = Label(main, text='LESS WATER', bg=WARNING_LABEL2)
        # self.less_water.grid(row=5, column=1)

        self.desired_conditions = Label(main, text='Desired Conditions', bg=BALANCED_LABEL)
        # self.desired_conditions.grid(row=5, column=2)
        
        # drop_down down boxes 
        self.limits = Label(main, text='Set Limits', bg=LABEL_COLOR)
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

        self.dry_drop_down = OptionMenu(main, self.clicked, *self.percentages, command=display_required_action)
        self.dry_drop_down.config(bg=BUTTON_COLOR)
        self.dry_drop_down.grid(row=7, column=0)

        self.divider = Label(main, text='-')
        self.divider.grid(row=7, column=1)

        self.humid_drop_down= OptionMenu(main, self.clicked, *self.percentages) #change automatically according to dry percentage
        self.humid_drop_down.config(bg=BUTTON_COLOR)
        self.humid_drop_down.grid(row=7, column=3)
        # GUI code ends


gui_class = humidity_checker_gui(root)
root.mainloop()