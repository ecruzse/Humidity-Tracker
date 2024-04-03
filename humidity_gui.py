from tkinter import * 
import customtkinter as ct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import requests
import datetime

ct.set_appearance_mode('dark')
ct.set_default_color_theme('green')

root = ct.CTk()
root.title('Humidity Checker')
root.geometry('600x500')

label_font = ct.CTkFont(size=20, family='Arial')
warning_label_font = ct.CTkFont(size=17, family='Arial', weight='bold')

LABEL_COLOR = '#9ea1a2'
BUTTON_COLOR = '#1167b1'
WARNING_LABEL_YELLOW = '#eed202'
WARNING_LABEL_ORANGE = '#ff9966'
BALANCED_LABEL = '#339900' #00FF00

class humidity_checker_gui:
    def __init__(self, main): #main==root
        self.main = main
        self.current_time = datetime.datetime.now()
        self.day_num = self.current_time.day
        self.humidity_percentage = 30
        self.response = requests.get('https://api.weather.gov/gridpoints/HGX/65,97/forecast') # National Weather Service API URL for Houston
        self.humidity_percentage = self.response.json()['properties']['periods'][self.day_num]['relativeHumidity']['value']
        self.probability_pf_precipitation = self.response.json()['properties']['periods'][self.day_num]['detailedForecast']
        frame = Frame(self.main)
        frame.grid()
        
        def forget_label(label_name):
            label_name.grid_forget()

        def display_required_action(desired_percentage):
            desired_float_percentage = float(desired_percentage.strip('%'))
            # float_dry_value =  float(TEMP_DRY_VAL.strip('%'))
            
            if  self.humidity_percentage > desired_float_percentage + 5:
                forget_label(self.add_water)
                forget_label(self.desired_conditions)
                self.less_water.grid(row=5, column=0)
            elif self.humidity_percentage < desired_float_percentage - 5:
                forget_label(self.less_water)
                forget_label(self.desired_conditions)
                self.add_water.grid(row=5 ,column=0)
            else:
                forget_label(self.less_water)
                forget_label(self.add_water)
                self.desired_conditions.grid(row=5, column=0)
      
        # pie chart and percentages
        def display_pie_graph():
            fig = plt.figure(figsize=(3,1), dpi=100)
            fig.set_size_inches(6,3)
            fig.patch.set_facecolor('black') #changes background of canvas that contains the pie graph 

            labels = 'Dry', 'Humid'
            sizes = 70,30 # CHANGE TO MAKE NON STATIC 
            explode = (0.3,0)

            plt.style.use('ggplot') #changes the pie graph's color using matplotlib

            plt.pie(sizes, 
                    explode=explode, 
                    labels=labels, 
                    pctdistance=.3, 
                    labeldistance=.3)
            plt.axis('equal')
            plt.legend(sizes, 
                        title='Percentages %',
                        loc="center right",
                        bbox_to_anchor=(.4, 0, .70, .85),
                        prop = { "size": 16 })

            canvasbar = FigureCanvasTkAgg(fig, master=self.main)
            canvasbar.draw()
            canvasbar.get_tk_widget().grid(row=1)
        
        self.soil_humidity = ct.CTkLabel(self.main, text='Soil Humidity')
        self.soil_humidity.grid(row=1, columnspan=2)
    
        # status, user take action
        self.status = ct.CTkLabel(self.main, text='Humidity Status', font=label_font)
        self.status.grid(row=4, column=0, columnspan=3, sticky='W')

        self.add_water = ct.CTkLabel(self.main, text='ADD WATER', bg_color=WARNING_LABEL_ORANGE, width=600, font=warning_label_font, text_color='black')

        self.less_water = ct.CTkLabel(self.main, text='TOO HUMID', bg_color=WARNING_LABEL_YELLOW, width=600, font=warning_label_font, text_color='black')

        self.desired_conditions = ct.CTkLabel(self.main, text='Desired Conditions', bg_color=BALANCED_LABEL, width=600, font=warning_label_font)
        
        display_pie_graph()

        # drop_down down boxes 
        self.limits = ct.CTkLabel(self.main, text='Set Desired Humidity Percentage', font=label_font)
        self.limits.grid(row=6, column=0, columnspan=3, sticky='W')

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

        self.dry_drop_down = ct.CTkOptionMenu(master=root, values=self.percentages, command=display_required_action)
        self.dry_drop_down.grid(row=7, column=0)
        
        self.api_forecast = ct.CTkLabel(self.main, text=f'National Weather Service Forecast', font=label_font)
        self.api_forecast.grid(row=8, column=0, columnspan=3, sticky='W')
        
        self.probability_pf_precipitation = ct.CTkLabel(self.main, text=f'{self.probability_pf_precipitation}')
        self.probability_pf_precipitation.grid(row=9, column=0, columnspan=3, sticky='W')
        # GUI code ends
            
gui_class = humidity_checker_gui(root)
root.mainloop()


        