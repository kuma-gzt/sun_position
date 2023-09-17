import sys
import fileinput
import logging
from input_formatting import InputFormatting
from algorithms import SunPosition
from charting import PlotSunPath
import math
import datetime

logging.basicConfig(filename='src/sun_position/logs/sun_position.log',
            format='%(levelname)s:%(asctime)s:%(message)s', encoding='utf-8',
            level=logging.DEBUG, filemode='a', datefmt='%Y%m%dT%I:%M:%S')

def main(args=None):
    """This is the entry point for the package"""
    if args is None:
        args = sys.argv[1:]
        #print(args)
        lat = float(args[0])
        lon = float(args[1])
        year = int(args[2])
        month = int(args[3])
        day = int(args[4])
        hour = int(args[5])
        minute = int(args[6])
        second = int(args[7])
        daylight = int(args[8])
        title = args[9]
        path = args[10]

        dt = datetime.datetime(year, month, day, hour, minute, second,
                               True if daylight == 1 else False)

        sunpos = SunPosition(lat, lon, dt.isoformat(), daylight)
        horizon_coords = sunpos.sun_position()
        plot = PlotSunPath(horizon_coords, title, lat, lon, 
                           dt.strftime('%Y-%b-%d'), path)
        plot.plot_horizontal_sunpath()


    # for line in fileinput.input():
    #     if fileinput.isfirstline():
    #         print("First line")
    #     else:
    #         tmp = InputFormatting(line, fileinput.lineno(),
    #                               fileinput.filename())
    #         sun_param = tmp.scan()
    #         if sun_param is None:
    #             pass
                #print(f"ERROR: Line {fileinput.lineno()} cannot be processed. See log for more details.")
                #logging.error('Line %s in the file %s cannot be processed. The program will continue with the next line',
                          #fileinput.lineno(), fileinput.filename())
    #         else:
    #             sunpos = SunPosition(*sun_param)
                #sunpos.sun_position()
                #azimuth, altitude = sunpos.sun_pos_day()
                #plot = PlotChart(azimuth, altitude)
                #plot.plot()
                #day = sunpos.sun_pos_day()
    #             months_dic = sunpos.sun_position()
                #az = months_dic['jun_jul'][0]
                #al = months_dic['jun_jul'][1]
    #             plot = PlotChart(months_dic)
    #             plot.plot()
                #print(months_dic['jan_dec'][0])
                #print(months_dic['jan_dec'][1])

#def read_lines():
    #"""Read the lines and call the InputFormatting class for each one"""
    #for line in fileinput.input():
        #if fileinput.isfirstline():
            #print("First line")
        #else:
            #print("here")
            #tmp = InputFormatting(line, fileinput.lineno(),
                                  #fileinput.filename())
            #sun_param = tmp.scan()
            #if sun_param is None:
                #print("here")
                #pass
                #print(f"ERROR: Line {fileinput.lineno()} cannot be processed. See log for more details.")
                #logging.error('Line %s in the file %s cannot be processed. The program will continue with the next line',
                          #fileinput.lineno(), fileinput.filename())
            #else:
                #print("here")
                #sunpos = SunPosition(*sun_param)
                #azim_lst, alt_lst = sunpos.sun_pos_day()

                #print(azim_lst)
                #print(alt_lst)

if __name__ == "__main__":
    sys.exit(main())


