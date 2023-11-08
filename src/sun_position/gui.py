"""This module contains the Tkinter GUI code."""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import datetime
from algorithms import SunPosition
from charting import PlotSunPath


class SunPathGUI():
    "GUI dialog for the input of parameters and running of the program"
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Sun-Path Charts')
        self.main_window.resizable(False, False)
        self.main_window.configure(bg='#dcdad5')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.__create_variables()
        self.__create_frames()
        self.__create_lbl_frames()
        self.__create_widgets()
        self.__create_layouts()

    def __create_variables(self):
        """Create StringVar variables"""
        dt = datetime.datetime.now()
        self.year = tk.StringVar(value=dt.year)
        self.month = tk.StringVar(value=dt.month)
        self.day = tk.StringVar(value=dt.day)
        self.hour = tk.StringVar(value=dt.hour)
        self.minute = tk.StringVar(value=dt.minute)
        self.timezone = tk.StringVar()
        self.daylight = tk.StringVar()
        self.latitude = tk.StringVar(value='35')
        self.longitude = tk.StringVar(value='-105')
        self.obs_elev = tk.StringVar(value='0')
        self.press = tk.StringVar(value='')
        self.temp = tk.StringVar(value='')
        self.hz_chart = tk.StringVar(value=1)
        self.vt_chart = tk.StringVar(value=1)
        self.data = tk.StringVar()
        self.title = tk.StringVar(value='Chart title')
        self.outputdir = tk.StringVar(value=os.path.expanduser('~'))

    def __create_widgets(self):
        """Create widgets"""

        self.val = GUIValidation(self.main_window)

        # intro
        intro_txt = 'Sun-Path Charts Parameters'
        self.intro_lbl = ttk.Label(self.intro_frame, text=intro_txt,
                                   font=("TkDefaultFont", 12),
                                   anchor='e')

        # year
        self.year_lbl = ttk.Label(self.date_lbl_frame, text='Year: ')
        self.year_spin = ttk.Spinbox(self.date_lbl_frame, from_=1900, to=2100,
                                     increment=1, textvariable=self.year,
                                     width=5, validate='focusout',
                                     validatecommand=self.val.year_vcmd,
                                     invalidcommand=self.val.year_ivcmd)

        # month
        self.month_lbl = ttk.Label(self.date_lbl_frame, text='Month: ')
        self.month_spin = ttk.Spinbox(self.date_lbl_frame, from_=1, to=12,
                                      increment=1, textvariable=self.month,
                                      width=3, validate='focusout',
                                      validatecommand=self.val.month_vcmd,
                                      invalidcommand=self.val.month_ivcmd)

        # day
        self.day_lbl = ttk.Label(self.date_lbl_frame, text='Day: ')
        self.day_spin = ttk.Spinbox(self.date_lbl_frame, from_=1, to=31,
                                    increment=1, textvariable=self.day,
                                    width=3, validate='focusout',
                                    validatecommand=self.val.day_vcmd,
                                    invalidcommand=self.val.day_ivcmd)

        # hour
        self.hour_lbl = ttk.Label(self.date_lbl_frame, text='Hour: ')
        self.hour_spin = ttk.Spinbox(self.date_lbl_frame, from_=0, to=23,
                                     increment=1, textvariable=self.hour,
                                     width=3, validate='focusout',
                                     validatecommand=self.val.hour_vcmd,
                                     invalidcommand=self.val.hour_ivcmd)

        # minute
        self.minute_lbl = ttk.Label(self.date_lbl_frame, text='Minute: ')
        self.minute_spin = ttk.Spinbox(self.date_lbl_frame, from_=1, to=59,
                                       increment=1, textvariable=self.minute,
                                       width=3, validate='focusout',
                                       validatecommand=self.val.minute_vcmd,
                                       invalidcommand=self.val.minute_ivcmd)

        # time zone
        self.timezone_lbl = ttk.Label(self.date_lbl_frame, text='Time zone: ')
        ut = ('-12', '-11.5', '-11', '-10.5', '-10', '-9.5', '-9', '-8.5',
              '-8', '-7.5', '-7', '-6.5', '-6', '-5.5', '-5', '-4.5', '-4',
              '-3.5', '-3', '-2.5', '-2', '-1.5', '-1', '-0.5', '0', '+0.5',
              '+1', '+1.5', '+2', '+2.5', '+3', '+3.5', '+4', '+4.5', '+5',
              '+5.5', '+6', '+6.5', '+7', '+7.5', '+8', '+8.5', '+9', '+9.5',
              '+10', '+10.5', '+11', '+11.5', '+12')
        self.timezone_dropdown = ttk.Combobox(self.date_lbl_frame,
                                              textvariable=self.timezone,
                                              state='readonly', justify='left',
                                              width=5, values=ut)
        self.timezone_dropdown.current(24)

        # daylight
        self.daylight_chkbox = ttk.Checkbutton(self.date_lbl_frame,
                                               text='Daylight Saving Time',
                                               variable=self.daylight,
                                               onvalue=1,
                                               offvalue=0)

        # latitud
        self.latitude_lbl = ttk.Label(self.location_lbl_frame,
                                      text='Latitude: ')
        self.latitude_entry = ttk.Entry(self.location_lbl_frame,
                                        textvariable=self.latitude, width=10,
                                        validate='focusout',
                                        validatecommand=self.val.lat_vcmd,
                                        invalidcommand=self.val.lat_ivcmd)

        # longitude
        self.longitude_lbl = ttk.Label(self.location_lbl_frame,
                                       text='Longitude: ')
        self.longitude_entry = ttk.Entry(self.location_lbl_frame,
                                         textvariable=self.longitude, width=10,
                                         validate='focusout',
                                         validatecommand=self.val.lon_vcmd,
                                         invalidcommand=self.val.lon_ivcmd)

        # observer elevation
        self.obs_elev_lbl = ttk.Label(self.other_lbl_frame,
                                      text='Observer elevation (meters): ')
        self.obs_elev_entry = ttk.Entry(self.other_lbl_frame,
                                        textvariable=self.obs_elev, width=10,
                                        validate='focusout',
                                        validatecommand=self.val.obs_elev_vcmd,
                                        invalidcommand=self.val.obs_elev_ivcmd)

        # pressure
        self.press_lbl = ttk.Label(self.other_lbl_frame,
                                   text='Annual avg local pressure (mbars): ')
        self.press_entry = ttk.Entry(self.other_lbl_frame,
                                     textvariable=self.press, width=10,
                                     validate='focusout',
                                     validatecommand=self.val.press_vcmd,
                                     invalidcommand=self.val.press_ivcmd)

        # temp
        self.temp_lbl = ttk.Label(self.other_lbl_frame,
                                  text='Annual avg local temperature (°C): ')
        self.temp_entry = ttk.Entry(self.other_lbl_frame,
                                    textvariable=self.temp, width=10,
                                    validate='focusout',
                                    validatecommand=self.val.temp_vcmd,
                                    invalidcommand=self.val.temp_ivcmd)

        # output
        self.hz_chart_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                               text='Plot horizontal sun path',
                                               variable=self.hz_chart,
                                               onvalue=1,
                                               offvalue=0)

        self.vt_chart_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                               text='Plot vertical sun path',
                                               variable=self.vt_chart,
                                               onvalue=1,
                                               offvalue=0)

        self.data_chkbox = ttk.Checkbutton(self.output_lbl_frame,
                                           text='Save plotting data as csv file',
                                           variable=self.data,
                                           onvalue=1,
                                           offvalue=0)

        self.title_entry = ttk.Entry(self.output_lbl_frame,
                                     textvariable=self.title, width=45)
        self.outputdir_btn = ttk.Button(self.output_lbl_frame,
                                        text='Select output directory',
                                        command=self.__output_directory)
        self.outputdir_lbl = ttk.Label(self.output_lbl_frame,
                                       textvariable=self.outputdir, width=45)

        # buttons
        self.quit_button = ttk.Button(self.button_frame, text='Quit',
                                      command=self.main_window.destroy)
        self.getcharts_button = ttk.Button(self.button_frame,
                                           text='Get Charts',
                                           command=self.__get_charts)

    def __create_frames(self):
        """Create frames"""
        self.intro_frame = ttk.Frame(self.main_window)
        self.button_frame = ttk.Frame(self.main_window)

    def __create_lbl_frames(self):
        """Create label frames"""
        self.date_lbl_frame = ttk.LabelFrame(self.main_window,
                                             text='Date and time',
                                             labelanchor='nw',
                                             padding=5)
        self.location_lbl_frame = ttk.LabelFrame(self.main_window,
                                                 text='Location',
                                                 labelanchor='nw',
                                                 padding=5)
        self.other_lbl_frame = ttk.LabelFrame(self.main_window,
                                              text='Other parameters (not mandatory)',
                                              labelanchor='nw',
                                              padding=5)
        self.output_lbl_frame = ttk.LabelFrame(self.main_window,
                                               text='Output',
                                               labelanchor='nw',
                                               padding=5)

    def __create_layouts(self):
        """Create layouts"""
        # intro
        self.intro_lbl.grid(column=0, row=0, padx=5, pady=5, sticky='WE')

        # year
        self.year_lbl.grid(column=0, row=1, sticky='E', pady=(0, 10))
        self.year_spin.grid(column=1, row=1, sticky='W', pady=(0, 10))

        # month
        self.month_lbl.grid(column=2, row=1, sticky='E', padx=(10, 1),
                            pady=(0, 10))
        self.month_spin.grid(column=3, row=1, sticky='W', pady=(0, 10))

        # day
        self.day_lbl.grid(column=4, row=1, sticky='E', padx=(10, 1),
                          pady=(0, 10))
        self.day_spin.grid(column=5, row=1, sticky='W', pady=(0, 10))

        # hour
        self.hour_lbl.grid(column=0, row=2, sticky='E')
        self.hour_spin.grid(column=1, row=2, sticky='W')

        # minute
        self.minute_lbl.grid(column=2, row=2, sticky='E', padx=(10, 1))
        self.minute_spin.grid(column=3, row=2, sticky='W')

        # time zone
        self.timezone_lbl.grid(column=4, row=2, sticky='E', padx=(10, 1),
                               pady=(10, 10))
        self.timezone_dropdown.grid(column=5, row=2, sticky='W', pady=(10, 10))

        # daylight
        self.daylight_chkbox.grid(column=1, row=3, sticky='W', columnspan=3)

        # latitude
        self.latitude_lbl.grid(column=0, row=4, sticky='E')
        self.latitude_entry.grid(column=1, row=4, sticky='W')

        # longitude
        self.longitude_lbl.grid(column=2, row=4, sticky='E', padx=(46, 1))
        self.longitude_entry.grid(column=3, row=4, sticky='W')

        # observers elevation
        self.obs_elev_lbl.grid(column=0, row=5, sticky='E', pady=(10, 10))
        self.obs_elev_entry.grid(column=1, row=5, sticky='W')

        # pressure
        self.press_lbl.grid(column=0, row=6, sticky='E', pady=(0, 10))
        self.press_entry.grid(column=1, row=6, sticky='W')

        # temperature
        self.temp_lbl.grid(column=0, row=7, sticky='E', pady=(0, 10))
        self.temp_entry.grid(column=1, row=7, sticky='W')

        # title
        self.title_entry.grid(column=0, row=8, sticky='W')

        # horizontal checkbox
        self.hz_chart_chkbox.grid(column=0, row=9, sticky='W', pady=(10, 5))

        # vertical checkbox
        self.vt_chart_chkbox.grid(column=0, row=10, sticky='W', pady=(0, 5))

        # data checkbox
        self.data_chkbox.grid(column=0, row=11, sticky='W', pady=(0, 10))

        # output directory
        self.outputdir_btn.grid(column=0, row=12, sticky='W', pady=(0, 10))
        self.outputdir_lbl.grid(column=0, row=13, sticky='W')

        # buttons
        self.quit_button.grid(column=0, row=14, padx=5, pady=(15, 5),
                              sticky='WE')
        self.getcharts_button.grid(column=1, row=14, padx=5, pady=(15, 5),
                                   sticky='WE')

        # label frames
        self.date_lbl_frame.grid(column=0, row=1, padx=5, pady=(10, 10),
                                 sticky='WE')
        self.location_lbl_frame.grid(column=0, row=2, padx=5, pady=(10, 10),
                                     sticky='WE')
        self.other_lbl_frame.grid(column=0, row=3, padx=5, pady=(10, 10),
                                  sticky='WE')
        self.output_lbl_frame.grid(column=0, row=4, padx=5, pady=(10, 10),
                                   sticky='WE')

        # frames
        #self.intro_frame.grid(column=0, row=0, padx=5, pady=5, sticky='WE')
        self.button_frame.grid(column=0, row=5, padx=10, pady=(35, 10),
                               sticky='E')

    def __output_directory(self):
        """Dialog to select output directory"""
        self.outputdir.set(filedialog.askdirectory())

    def __get_charts(self):
        """Class the class to create the sun position charts"""

        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        hour = int(self.hour.get())
        minute = int(self.minute.get())
        timezone = self.timezone.get()
        daylight = self.daylight.get()
        lat = float(self.latitude.get())
        lon = float(self.longitude.get())
        obs_elev = float(self.obs_elev.get())
        press = float(self.press.get())
        temp = float(self.temp.get())
        title = self.title.get()
        path = self.outputdir.get()

        # test for date and time correctness
        tmp = [self.val.year_validation(year),
               self.val.month_validation(month), self.val.day_validation(day),
               self.val.hour_validation(hour),
               self.val.minute_validation(minute)]

        if not all(tmp):
            self.val.error_msgbox('Invalid date or time value', '')
            return
        else:
            try:
                # seconds are zero
                dt = datetime.datetime(year, month, day, hour, minute, 0,
                                       True if daylight == 1 else False)
            except:
                self.val.error_msgbox('Invalid date or time value',
                                      'Review the logs')
                return

        # test for coordinates correctness
        tmp = [self.val.lat_validation(lat), self.val.lon_validation(lon)]

        if not all(tmp):
            self.val.error_msgbox('Invalid coordinate values', '')
            return

        sunpos = SunPosition(lat, lon, dt.isoformat(), daylight, obs_elev,
                             press, temp)
        horizon_coords = sunpos.sun_position()
        plot = PlotSunPath(horizon_coords, title, lat, lon,
                           dt.strftime('%Y-%b-%d'), path)
        plot.plot_diagrams()


class GUIValidation():
    "GUI validation for the input parameters"
    def __init__(self, main_window):
        self.main_window = main_window

        # year
        self.year_vcmd = (self.main_window.register(self.year_validation),
                          '%P')
        self.year_ivcmd = (self.main_window.register(self.on_year_invalid),)

        # month
        self.month_vcmd = (self.main_window.register(self.month_validation),
                           '%P')
        self.month_ivcmd = (self.main_window.register(self.on_month_invalid),)

        # day
        self.day_vcmd = (self.main_window.register(self.day_validation), '%P')
        self.day_ivcmd = (self.main_window.register(self.on_day_invalid),)

        # hour
        self.hour_vcmd = (self.main_window.register(self.hour_validation),
                          '%P')
        self.hour_ivcmd = (self.main_window.register(self.on_hour_invalid),)

        # minute
        self.minute_vcmd = (self.main_window.register(self.minute_validation),
                            '%P')
        self.minute_ivcmd = (self.main_window.register(self.on_minute_invalid),)

        # latitude
        self.lat_vcmd = (self.main_window.register(self.lat_validation), '%P')
        self.lat_ivcmd = (self.main_window.register(self.on_lat_invalid),)

        # longitude
        self.lon_vcmd = (self.main_window.register(self.lon_validation), '%P')
        self.lon_ivcmd = (self.main_window.register(self.on_lon_invalid),)

        # observer elevation
        self.obs_elev_vcmd = (self.main_window.register(self.obs_elev_validation),
                              '%P')
        self.obs_elev_ivcmd = (self.main_window.register(self.on_obs_elev_invalid),)

        # pressure
        self.press_vcmd = (self.main_window.register(self.press_validation),
                           '%P')
        self.press_ivcmd = (self.main_window.register(self.on_press_invalid),)

        # temperature
        self.temp_vcmd = (self.main_window.register(self.temp_validation),
                          '%P')
        self.temp_ivcmd = (self.main_window.register(self.on_temp_invalid),)

    def year_validation(self, year):
        """Validate the year"""
        if int(year) < 1900 or int(year) > 2100:
            return False
        return True

    def on_year_invalid(self):
        """On invalid year"""
        self.error_msgbox('Invalid year',
                          'Year must be in the range 1900 to 2100')

    def month_validation(self, month):
        """Validate the month"""
        if int(month) < 1 or int(month) > 12:
            return False
        return True

    def on_month_invalid(self):
        """On invalid month"""
        self.error_msgbox('Invalid month',
                          'Month must be in the range 1 to 12')

    def day_validation(self, day):
        """Validate the day"""
        if int(day) < 1 or int(day) > 31:
            return False
        return True

    def on_day_invalid(self):
        """On invalid day"""
        self.error_msgbox('Invalid day',
                          'Day must be in the range 1 to 31')

    def hour_validation(self, hour):
        """Validate the hour"""
        if int(hour) < 0 or int(hour) > 23:
            return False
        return True

    def on_hour_invalid(self):
        """On invalid hour"""
        self.error_msgbox('Invalid hour',
                          'Hour must be in the range 0 to 24')

    def on_minute_invalid(self):
        """On invalid minute"""
        self.error_msgbox('Invalid minute',
                          'Minute must be in the range 1 to 59')

    def minute_validation(self, minute):
        """Validate the minute"""
        if int(minute) < 1 or int(minute) > 59:
            return False
        return True

    def lat_validation(self, lat):
        """Validate the latitude"""
        if float(lat) < -90 or float(lat) > 90:
            return False
        return True

    def on_lat_invalid(self):
        """On invalid latitude"""
        self.error_msgbox('Invalid latitude value',
                          'Latitudes must be in the range -90 to 90')

    def lon_validation(self, lon):
        """Validate the longitude"""
        if float(lon) < -180 or float(lon) > 180:
            return False
        return True

    def on_lon_invalid(self):
        """On invalid longitude"""
        self.error_msgbox('Invalid longitude value',
                          'Longitudes must be in the range -180 to 180')

    def obs_elev_validation(self, obs_elev):
        """Validate the observer elevation"""
        if float(obs_elev) < -420 or float(obs_elev) > 8850:
            return False
        return True

    def on_obs_elev_invalid(self):
        """On invalid observer elevation"""
        self.error_msgbox('Invalid observer elevation value',
                          'Elevation must be in the range -420 to 8850 meters')

    def press_validation(self, press):
        """Validate the atmospheric pressure"""
        if float(press) < 850 or float(press) > 1090:
            return False
        return True

    def on_press_invalid(self):
        """On invalid atmospheric pressure"""
        self.error_msgbox('Invalid atmospheric pressure value',
                          'Atmospheric pressure must be in the range 850 to 1090 mbars')

    def temp_validation(self, temp):
        """Validate the temperature"""
        if float(temp) < -90 or float(temp) > 57:
            return False
        return True

    def on_temp_invalid(self):
        """On invalid temperature"""
        self.error_msgbox('Invalid temperature value',
                          'Atmospheric pressure must be in the range -90 to 57 C')

    def error_msgbox(self, message, detail):
        """Error message box"""
        messagebox.showerror(title='Input error', message=message,
                             detail=detail)


if __name__ == '__main__':
    app = SunPathGUI()
    app.main_window.mainloop()