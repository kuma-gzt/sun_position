"""This module contains a single class used to plot the vertical and horizontal
sun-path diagrams"""

import os
from math import radians, degrees
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import AutoMinorLocator
import sun_path_diagrams.config as cfg


class PlotSunPath:
    """This class will plot the horizontal and vertical sun-path diagrams"""
    def __init__(self, horizon_coords, horizon_coords_point, lat, lon, dt,
                 timezone, title, hz_chart, vt_chart, plt_point, path):
        self.horizon_coords = horizon_coords
        self.horizon_coords_point = horizon_coords_point
        self.lat = lat
        self.lon = lon
        self.date = dt.strftime('%Y-%b-%d')
        self.time = dt.strftime('%H:%M')
        self.timezone = timezone
        self.title = title
        self.hz_chart = int(hz_chart)
        self.vt_chart = int(vt_chart)
        self.plt_point = int(plt_point)
        self.path = path

    def plot_diagrams(self):
        """Plots the vertical and horizontal sun path diagrams"""
        chart_data = self.__get_chart_data()
        if self.hz_chart:
            self.__horizontal_sunpath(chart_data)
        if self.vt_chart:
            self.__vertical_sunpath(chart_data)

    def __vertical_sunpath(self, chart_data):
        """Plots the vertical sun-path diagram"""
        fig, ax = plt.subplots()
        fig.set_size_inches(cfg.fig_zize['width'], cfg.fig_zize['height'])

        # create lines for legend
        lines = [matplotlib.lines.Line2D([0], [0], linestyle=item[0],
                 color=cfg.equisols_symb['color']) for item in
                 cfg.equisols.values()]

        # create labels for legend
        labels = [item[1] for item in cfg.equisols.values()]

        for key, value in chart_data.items():
            if key[0] == 'p':
                azim = value[0]
                alt = value[1]
                # plot user curve
                ax.plot([degrees(i) for i in azim], alt,
                        color=cfg.user_symb['color'],
                        linewidth=cfg.user_symb['linewidth'])
                # line and label for legend
                lines.append(matplotlib.lines.Line2D([0], [0],
                             color=cfg.user_symb['color']))
                labels.append(key[1:4] + ' ' + key[4:6])

                # plot user's mark
                if self.plt_point:
                    azim = self.horizon_coords_point[0]
                    alt = self.horizon_coords_point[1]
                    ax.plot(azim, alt, color=cfg.user_symb_point['color'],
                            marker=cfg.user_symb_point['marker'],
                            markersize=cfg.user_symb_point['markersize'])
                    lines.append(matplotlib.lines.Line2D([0], [0],
                                 color=cfg.user_symb_point['color'],
                                 marker=cfg.user_symb_point['marker'],
                                 markersize=cfg.user_symb_point['markersize'],
                                 linewidth=cfg.user_symb_point['linewidth']))
                    labels.append('Sun position')
            elif key == 'hours':
                # plot analemmas
                analemmas = self.__get_analemmas(value)
                for _, value_ in analemmas.items():
                    ax.plot([degrees(i) for i in value_[0]], value_[1],
                            color=cfg.ana_symb['color'],
                            linestyle=cfg.ana_symb['linestyle'],
                            linewidth=cfg.ana_symb['linewidth'])
                # plot hour labels
                for item in value:
                    if item[0] == 'Jun21':
                        # range starts at 1 so we don't plot the 25th hour
                        for j in range(1, len(item[1])):
                            ax.annotate(item[3][j],
                                        xy=(degrees(item[1][j]), item[2][j]),
                                        xytext=cfg.hour_symb['xytext'],
                                        textcoords='offset points',
                                        color=cfg.hour_symb['color'],
                                        size=cfg.hour_symb['size'])
            else:
                azim = value[0]
                alt = value[1]
                # plot equinoxes and solstices curves
                ax.plot([degrees(i) for i in azim], alt,
                        color=cfg.equisols_symb['color'],
                        linewidth=cfg.equisols_symb['linewidth'],
                        linestyle=cfg.equisols[key][0])

        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.tick_params(axis='both', labelsize='8')
        ax.tick_params(which='minor', length=2)

        ax.set_aspect(3)

        ax.set_ylim(bottom=0, top=90)
        y_ticks, y_labels = self.__get_yticks(0, 91, 10)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)

        ax.set_xlim(left=0, right=radians(360))
        x_ticks, x_labels = self.__get_xticks(0, 361, 30)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels)

        ax.grid(color=cfg.grid_symb['color1'],
                linestyle=cfg.grid_symb['linestyle'],
                linewidth=cfg.grid_symb['linewidth'])

        ax.set_title(self.title)
        ax.set_xlabel('Azimuth')
        ax.set_ylabel('Altitude')

        fig.legend(lines, labels, loc='lower right', fontsize='small',
                   handlelength=4, frameon=False)
        text = f'Vertical Sun Path Diagram \nLatitude: {self.lat}° \
                \nLongitude: {self.lon}° \nDate: {self.date}'
        if self.plt_point:
            text = text + '\nTime: ' + self.time
        fig.text(0.01, 0.02, text, fontsize='small', linespacing=1.5)

        file_name = f'VerticalSunPath_{self.date}.png'
        plt.savefig(os.path.join(self.path, file_name))
        #plt.show()
        plt.close()

    def __horizontal_sunpath(self, chart_data):
        """Plots the horizontal sun-path diagram"""
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        fig.set_size_inches(cfg.fig_zize['width'], cfg.fig_zize['height'])

        # create lines for legend
        lines = [matplotlib.lines.Line2D([0], [0], linestyle=item[0],
                 color=cfg.equisols_symb['color']) for item in
                 cfg.equisols.values()]

        # create labels for legend
        labels = [item[1] for item in cfg.equisols.values()]

        for key, value in chart_data.items():
            if key[0] == 'p':
                # calculate the revised azimuth and altitude
                azim, alt = self.__revised_azim_alt(value[0], value[1],
                                                    self.lat)
                # plot date user curve
                ax.plot(azim, alt, color=cfg.user_symb['color'],
                        linewidth=cfg.user_symb['linewidth'])

                # plot hours in the date user curve
                # ax.plot(azim, alt, color=cfg.user_symb['color'],
                #         marker=cfg.user_symb['marker'])

                # line and label for legend
                lines.append(matplotlib.lines.Line2D([0], [0],
                             color=cfg.user_symb['color']))
                labels.append(key[1:4] + ' ' + key[4:6])

                # plot user's mark
                if self.plt_point:
                    azim = radians(self.horizon_coords_point[0])
                    alt = self.horizon_coords_point[1]
                    ax.plot(azim, alt, color=cfg.user_symb_point['color'],
                            marker=cfg.user_symb_point['marker'],
                            markersize=cfg.user_symb_point['markersize'])
                    lines.append(matplotlib.lines.Line2D([0], [0],
                                 color=cfg.user_symb_point['color'],
                                 marker=cfg.user_symb_point['marker'],
                                 markersize=cfg.user_symb_point['markersize'],
                                 linewidth=cfg.user_symb_point['linewidth']))
                    labels.append('Sun position')

                # draw minor ticks every 5 degrees
                az, al = self.__get_hz_minor_ticks(5)
                ax.plot(az, al, color=cfg.grid_symb['color2'],
                        linewidth=cfg.grid_symb['linewidth'])
            elif key == 'hours':
                # plot analemmas
                analemmas = self.__get_analemmas(value)
                for _, value_ in analemmas.items():
                    ax.plot(value_[0], value_[1], color=cfg.ana_symb['color'],
                            linestyle=cfg.ana_symb['linestyle'],
                            linewidth=cfg.ana_symb['linewidth'])
                # plot hour labels
                for item in value:
                    # range starts at 1 so we don't plot the 25th hour
                    for j in range(1, len(item[1])):
                        if item[0] == 'Jun21' and self.lat >= 0:
                            ax.annotate(item[3][j],
                                        xy=(item[1][j], item[2][j]),
                                        xytext=self.__repo_labels(item[1][j],
                                                                  self.lat),
                                        textcoords='offset points',
                                        color=cfg.hour_symb['color'],
                                        size=cfg.hour_symb['size'],
                                        horizontalalignment='center',
                                        verticalalignment='center')
                        if item[0] == 'Dec21' and self.lat < 0:
                            ax.annotate(item[3][j],
                                        xy=(item[1][j], item[2][j]),
                                        xytext=self.__repo_labels(item[1][j],
                                                                  self.lat),
                                        textcoords='offset points',
                                        color=cfg.hour_symb['color'],
                                        size=cfg.hour_symb['size'],
                                        horizontalalignment='center',
                                        verticalalignment='center')
            else:
                azim, alt = self.__revised_azim_alt(value[0], value[1],
                                                    self.lat)
                ax.plot(azim, alt, color=cfg.equisols_symb['color'],
                        linewidth=cfg.equisols_symb['linewidth'],
                        linestyle=cfg.equisols[key][0])

        ax.set_title(self.title)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set(aspect='equal', rorigin=90)
        ax.set_rmax(0)
        ax.set_rmin(90)
        r_ticks, r_labels = self.__get_yticks(10, 81, 10)
        ax.set_rgrids(r_ticks, r_labels, angle=cfg.grid_symb['angle'],
                      color=cfg.grid_symb['color3'],
                      size=cfg.grid_symb['size'])

        theta_ticks, theta_labels = self.__get_xticks(0, 360, 15)
        ax.set_thetagrids(theta_ticks, theta_labels,
                          color=cfg.grid_symb['color2'],
                          size=cfg.grid_symb['size'])

        ax.grid(color=cfg.grid_symb['color1'],
                linestyle=cfg.grid_symb['linestyle'],
                linewidth=cfg.grid_symb['linewidth'])

        fig.legend(lines, labels, loc='lower right', fontsize='small',
                   handlelength=4, frameon=False)
        text = f'Horizontal Sun Path Diagram \nLatitude: {self.lat}° \
                \nLongitude: {self.lon}° \nDate: {self.date}'
        if self.plt_point:
            text = text + '\nTime: ' + self.time
        fig.text(0.01, 0.02, text, fontsize='small', linespacing=1.5)

        file_name = f'HorizontalSunPath_{self.date}.png'
        plt.savefig(os.path.join(self.path, file_name))
        #plt.show()
        plt.close()

    def __get_chart_data(self):
        """Process the data for the plotting functions"""
        whole_hours = []
        key_dates = ['Jun21', 'Mar21', 'Dec21']
        chart_data = {}

        for key, value in self.horizon_coords.items():
            azimuths = value[0]
            altitudes = value[1]

            if key in key_dates:
                # convert azimuth degrees to radians
                azimuth_rad = [radians(i) for i in azimuths]
                chart_data[key] = (azimuth_rad, altitudes)

            # plot input's date
            if key[0] == 'p':
                # convert azimuth degrees to radians
                azimuth_rad = [radians(i) for i in azimuths]
                chart_data[key] = (azimuth_rad, altitudes)

            off_ut = self.timezone

            # get the coordinates for whole hours
            azims, alts, hours = self.__get_hours(azimuths, altitudes, off_ut)
            whole_hours.append((key, azims, alts, hours))

        chart_data['hours'] = whole_hours

        return chart_data

    def __revised_azim_alt(self, azim, alt, lat):
        """For latitudes between -30 and 30 degrees there are lines that plots
        across the circle. This method adds new coordinates to move these lines
        off the circle plot"""

        if lat > -30 and lat < 30:
            alt_sort = alt.copy()
            alt_sort.sort()
            for item in alt_sort:
                ndx = alt.index(item)
                if degrees(azim[ndx]) >= 270:
                    azim.insert(ndx + 1, 5.5)
                    alt.insert(ndx + 1, -89)
                    azim.insert(ndx + 2, 6.27)
                    alt.insert(ndx + 2, -89)
                    return azim, alt
                elif degrees(azim[ndx]) >= 180 and degrees(azim[ndx]) < 270:
                    azim.insert(ndx + 1, 3.14)
                    alt.insert(ndx + 1, -89)
                    azim.insert(ndx + 2, 3.67)
                    alt.insert(ndx + 2, -89)
                    return azim, alt

        return azim, alt

    def __get_hours(self, azimuths, altitudes, off_ut):
        """Calculate whole hours positions"""
        azims = []
        alts = []
        hours = []

        count = off_ut - 1
        for i in azimuths:
            index = azimuths.index(i)
            if count == 24:
                count = 0
            count = count + 1
            azims.append(radians(i))
            alts.append(altitudes[index])
            hours.append(count)

        hour_pairs = [(-1, 23), (-2, 22), (-3, 21), (-4, 20), (-5, 19),
                      (-6, 18), (-7, 17), (-8, 16), (-9, 15), (-10, 14),
                      (-11, 13), (-12, 12)]

        for item in hour_pairs:
            if item[0] in hours:
                ndx = hours.index(item[0])
                hours[ndx] = item[1]

        return azims, alts, hours

    def __get_analemmas(self, hours):
        """Get the analemma coordinates"""
        min_hour = 24
        max_hour = 0

        for i in hours:
            if min(i[3]) < min_hour:
                min_hour = min(i[3])
            if max(i[3]) > max_hour:
                max_hour = max(i[3])

        analemmas = {}

        for i in range(min_hour, max_hour + 1):
            azims = []
            alts = []
            for j in hours:
                if i in j[3]:
                    p = j[3].index(i)
                    azims.append(j[1][p])
                    alts.append(j[2][p])
            analemmas[str(i)] = (azims, alts)

        return analemmas

    def __get_hz_minor_ticks(self, interval):
        """Given the interval, gets the minor ticks for the horizontal sun-path 
        diagram. Note that minor thicks are not available for polar charts,
        hence this hack"""
        ticks = range(0, 360, interval)
        tmp = [radians(i) for i in ticks]

        return [tmp, tmp], [[1]*int(360/interval), [0]*int(360/interval)]

    def __get_xticks(self, start, end, interval):
        """Given the start, end and interval, get the ticks and labels for the
        x-axis and theta-axis"""
        ticks = range(start, end, interval)
        labels = []
        for i in ticks:
            if i == 0 or i == 360:
                labels.append('N')
            elif i == 90:
                labels.append('E')
            elif i == 180:
                labels.append('S')
            elif i == 270:
                labels.append('W')
            else:
                labels.append(str(i) + '°')

        return ticks, labels

    def __get_yticks(self, start, end, interval):
        """Given the start, end and interval, get the ticks and labels for the 
        y-axis and r-axis"""
        ticks = range(start, end, interval)
        labels = [str(i) + '°' for i in ticks]

        return ticks, labels

    def __repo_labels(self, x, lat):
        """Reposition the hour labels"""
        if lat >= 60 or lat <= -60:
            x = degrees(x)
            if x >= 345:
                pos = (0, -6)
            elif x < 15:
                pos = (0, -6)
            elif x >= 15 and x < 45:
                pos = (-2, -6)
            elif x >= 45 and x < 75:
                pos = (-4, -6)
            elif x >= 75 and x < 105:
                pos = (-5, 0)
            elif x >= 105 and x < 135:
                pos = (-4, 6)
            elif x >= 135 and x < 165:
                pos = (-2, 6)
            elif x >= 165 and x < 195:
                pos = (0, 6)
            elif x >= 195 and x < 225:
                pos = (2, 6)
            elif x >= 225 and x < 255:
                pos = (4, 6)
            elif x >= 255 and x < 285:
                pos = (5, 0)
            elif x >= 285 and x < 315:
                pos = (4, -6)
            elif x >= 315 and x < 345:
                pos = (2, -6)
            else:
                pos = (0, 6)
        elif lat >= 0 and lat < 60:
            pos = (0, 6)
        elif lat < 0 and lat > -60:
            pos = (0, -6)
        else:
            pos = (0, 6)

        return pos