This program has been designed to generate potential routes among the United
States' top 1000 cities by population (using the dataset us-cities-top1k.csv,
obtained from the sample datasets offered by the Plotly Python graphing
library) in an effort to tackle a variation of the Traveling Salesman Problem by
using genetic algorithms. The algorithm can be run by executing main.py after
ensuring that geopy, folium, and colour have all been installed to the current
Python environment, likely by using pip. Once main.py is started successfully,
you will be prompted first for the amount of generations of route
populations to create, and then for the amount of routes to include in each
generation. The former is locked to a range of 1-1000, although it is heavily
recommended to stay within 1-100 for efficiency's sake, and the latter is also
limited to 1-1000, with 100 being a good standard value. After chooosing values
for these parameters, different key routes and route statistics can be viewed
from the numbered list displayed, and interactive route maps can optionally be
chosen to be saved, which are formatted as HTML files that can be opened and
navigated with any web browser by double-clicking the downloaded file. After
viewing one route from the menu, you can choose to either view another route
from the dataset or quit the program entirely. No data from one run will carry
over to another unless route maps are saved, in which case the file(s) would
remain.
