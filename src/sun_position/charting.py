import matplotlib.pyplot as plt
import matplotlib
from math import radians
import json
import os

class PlotSunPath:
    def __init__(self, horizon_coords, title, lat, lon, date, path):
        self.horizon_coords = horizon_coords
        self.title = title
        self.lat = lat
        self.lon = lon
        self.date = date
        self.path = path

    def plot_horizontal_sunpath(self):
        """Plot the horizontal sun-path diagram"""
        # load the plot configuration file
        cfg = self.__config()

        whole_hours = []

        # line type and labels
        equisols = {'Jun21':((0, (7, 1, 1, 1, 1, 1, 1, 1)), 'Jun 21'),                    
                    'Mar21':((0, (7, 1, 1, 1, 1, 1)), 'Mar-Sep 21'),                    
                    'Dec21':((0, (7, 1, 1, 1)), 'Dec 21')}
 
        # create lines for legend
        lines = [matplotlib.lines.Line2D([0], [0], linestyle=item[0], 
                color='black') for item in equisols.values()]
        
        # create labels for legend
        labels = [item[1] for item in equisols.values()] 

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        fig.set_size_inches(cfg['fig_size_width'], cfg['fig_size_height'])

        for key, value in self.horizon_coords.items():
            azimuths = value[0]
            altitudes = value[1]

            # TODO verify the correctdness of formula below
            off_ut = round(self.lon/15)

            # get the coordinates for whole hours
            azims, alts, hours = self.__get_hours(azimuths, altitudes, off_ut)
            whole_hours.append((azims, alts, hours))

            if key in equisols:
                # convert azimuth degrees to radians
                azimuth_rad = [radians(i) for i in azimuths]
                
                ax.plot(azimuth_rad, altitudes, color='black', linewidth=1, 
                        linestyle=equisols[key][0])

                # draw ticks every 5 degrees
                az, al = self.__getticks(5)
                ax.plot(az, al, color='black', linewidth=0.5)

                # plot whole hours labels
                if key == 'Jun21':
                    for i in range(0, len(hours)):
                        ax.annotate(hours[i], xy=(azims[i], alts[i]),
                        xytext=(-3, 5), textcoords='offset points',
                        color='black', size='8')

            # plot input's date 
            if key[0] == 'p':
                # convert azimuth degrees to radians
                azimuth_rad = [radians(i) for i in azimuths]
                ax.plot(azimuth_rad, altitudes, color=cfg['color_input'], 
                        linewidth=1)
                # line and label for legend
                lines.append(matplotlib.lines.Line2D([0], [0], 
                             color=cfg['color_input']))
                labels.append(key[1:4] + ' ' + key[4:6])

        # plot analemmas
        analemmas = self.__get_analemmas(whole_hours)
        
        for key, value in analemmas.items():
            ax.plot(value[0], value[1], color='black', linestyle='solid', 
                    linewidth=0.5)

        ax.set(aspect='equal', rorigin=90)
        ax.set_rmax(0)
        ax.set_rmin(90)
        ax.set_rgrids((10, 20, 30, 40, 50, 60, 70, 80, 90),
                      ('10°','20°','30°','40°','50°','60°','70°','80°',''),
                      angle=52, color='gray', size='8')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetagrids((0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165,
                           180, 195, 210, 225, 240, 255, 270, 285, 300, 315,
                           330, 345),
                          ('N', '15°', '30°', '45°', '60°', '75°', 'E°', '105°',
                           '120°', '135°', '150°', '165°', 'S', '195°', '210°',
                           '225°', '240°', '255°', 'W', '285°', '300°', '315°',
                           '330°', '345°'), size='8')
        ax.grid(color='#d8d8d8', linestyle='-', linewidth=0.5)
        ax.set_title(self.title)
        
        fig.legend(lines, labels, loc='lower right', fontsize='small', 
                    handlelength=4, frameon=False)
        text = f'Horizontal Sun Path Diagram \nLatitude: {self.lat}° \
                \nLongitude: {self.lon}° \nDate: {self.date}'
        fig.text(0.01, 0.02, text, fontsize='small', linespacing=1.5)

        plt.savefig(self.path)
        plt.show()

    def __get_hours(self, azimuths, altitudes, off_ut):
        """Calculate whole hours positions"""

        azims = []
        alts = []
        hours = []

        count = off_ut
        for i in azimuths:
            index = azimuths.index(i)
            if index%2 == 0:
                count = count + 1
                azims.append(i)
                alts.append(altitudes[index])
                hours.append(count)

        azims_ = [radians(i) for i in azims]
        return azims_, alts, hours

    def __get_analemmas(self, hours):
        """Get the analemma coordinates"""

        min_hour = 25
        max_hour = -1

        for i in hours:
            if min(i[2]) < min_hour:
                min_hour = min(i[2])
            if max(i[2]) > max_hour:
                max_hour = max(i[2])

        analemmas = {}

        for i in range(min_hour, max_hour + 1):
            azims = []
            alts = []
            for j in hours:
                if i in j[2]:
                    p = j[2].index(i)
                    azims.append(j[0][p])
                    alts.append(j[1][p])
            analemmas[str(i)] = (azims, alts)

        return analemmas

    def __getticks(self, interval):
        """Get the ticks coordinates at interval"""
        ticks = range(0, 360, interval)
        tmp = [radians(i) for i in ticks]

        return [tmp, tmp], [[1]*int(360/interval), [0]*int(360/interval)]

    def __config(self):
        """Read the config file for plotting options"""
        charting_dir = os.path.dirname(os.path.abspath(__file__))
        config_pth = 'conf/config.json'
        abs_file_path = os.path.join(charting_dir, config_pth)
        with open(abs_file_path) as config:
            return json.load(config)
