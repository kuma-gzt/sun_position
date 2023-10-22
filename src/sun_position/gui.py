"""This module contains Tkinter GUI code for the package."""
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
        self.daylight = tk.StringVar()
        self.latitude = tk.StringVar(value='35')
        self.longitude = tk.StringVar(value='-105')
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

        # daylight
        self.daylight_chkbox = ttk.Checkbutton(self.date_lbl_frame,
                                               text='DST',
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
                                        text='Browse output directory',
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
                                             text='Date and Time',
                                             labelanchor='nw',
                                             padding=5)
        self.location_lbl_frame = ttk.LabelFrame(self.main_window,
                                                 text='Location',
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
        self.month_lbl.grid(column=2, row=1, sticky='E', padx=(30, 1),
                            pady=(0, 10))
        self.month_spin.grid(column=3, row=1, sticky='W', pady=(0, 10))

        # day
        self.day_lbl.grid(column=4, row=1, sticky='E', padx=(30, 1),
                          pady=(0, 10))
        self.day_spin.grid(column=5, row=1, sticky='W', pady=(0, 10))

        # hour
        self.hour_lbl.grid(column=0, row=2, sticky='E')
        self.hour_spin.grid(column=1, row=2, sticky='W')

        # minute
        self.minute_lbl.grid(column=2, row=2, sticky='E', padx=(10, 1))
        self.minute_spin.grid(column=3, row=2, sticky='W')

        # daylight
        self.daylight_chkbox.grid(column=5, row=2, sticky='E')

        # latitude
        self.latitude_lbl.grid(column=0, row=3, sticky='E')
        self.latitude_entry.grid(column=1, row=3, sticky='W')

        # longitude
        self.longitude_lbl.grid(column=2, row=3, sticky='E', padx=(46, 1))
        self.longitude_entry.grid(column=3, row=3, sticky='W')

        # title
        self.title_entry.grid(column=0, row=4, sticky='W')

        # horizontal checkbox
        self.hz_chart_chkbox.grid(column=0, row=5, sticky='W', pady=(10, 5))

        # vertical checkbox
        self.vt_chart_chkbox.grid(column=0, row=6, sticky='W', pady=(0, 5))

        # data checkbox
        self.data_chkbox.grid(column=0, row=7, sticky='W', pady=(0, 10))

        # output directory
        self.outputdir_btn.grid(column=0, row=8, sticky='W', pady=(0, 10))
        self.outputdir_lbl.grid(column=0, row=9, sticky='W')

        # buttons
        self.quit_button.grid(column=0, row=10, padx=5, pady=(15, 5),
                              sticky='WE')
        self.getcharts_button.grid(column=1, row=10, padx=5, pady=(15, 5),
                                   sticky='WE')

        # label frames
        self.date_lbl_frame.grid(column=0, row=1, padx=5, pady=(15, 15),
                                 sticky='WE')
        self.location_lbl_frame.grid(column=0, row=2, padx=5, pady=(15, 15),
                                     sticky='WE')
        self.output_lbl_frame.grid(column=0, row=3, padx=5, pady=(15, 15),
                                   sticky='WE')

        # frames
        #self.intro_frame.grid(column=0, row=0, padx=5, pady=5, sticky='WE')
        self.button_frame.grid(column=0, row=4, padx=10, pady=(35, 10),
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
        daylight = self.daylight.get()
        lat = float(self.latitude.get())
        lon = float(self.longitude.get())
        title = self.title.get()
        path = self.outputdir.get()

        # test for date and time correctness
        tmp = [self.val.year_validation(year), self.val.month_validation(month),
               self.val.day_validation(day), self.val.hour_validation(hour),
               self.val.minute_validation(minute)]

        if not all(tmp):
            self.val.error_msgbox('Invalid date or time value', '')
            return
        else:
            try:
                # second is zero
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

        sunpos = SunPosition(lat, lon, dt.isoformat(), daylight)
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

    def error_msgbox(self, message, detail):
        """Error message box"""
        messagebox.showerror(title='Input error', message=message,
                             detail=detail)


if __name__ == '__main__':
    app = SunPathGUI()
    app.main_window.mainloop()