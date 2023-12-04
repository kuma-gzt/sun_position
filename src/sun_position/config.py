"""This module holds configuration variables for the charts"""

# figure size in inches
fig_zize = {'width': 8, 'height': 8}

# line symbol and labels for equinoxes and solstices
equisols = {'Jun21': ((0, (7, 1, 1, 1, 1, 1, 1, 1)), 'Jun 21'),
            'Mar21': ((0, (7, 1, 1, 1, 1, 1)), 'Mar-Sep 21'),
            'Dec21': ((0, (7, 1, 1, 1)), 'Dec 21')}

# equinoxes and solstices lines symbology properties
equisols_symb = {'color': 'black', 'linewidth': 1}

# user selected date and time
user_symb = {'color': '#eb9800', 'linewidth': 1, 'marker': '.'}

# user selected date and time (point symbol)
user_symb_point = {'color': 'red', 'marker': 'o', 'markersize': '6',
                   'linewidth': 0}

# analemmas symbology properties
ana_symb = {'color': 'black', 'linestyle': 'solid', 'linewidth': 0.5}

# hour symbology properties
hour_symb = {'color': 'black', 'size': '7', 'xytext': (-3, 5)}

# grid symbology properties
grid_symb = {'color1': '#cecece', 'color2': 'black', 'color3': '#767676',
             'linestyle': '-', 'linewidth': 0.5, 'angle': 52, 'size': '8'}