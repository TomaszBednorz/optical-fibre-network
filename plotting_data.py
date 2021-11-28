import gmplot
from data_structures import *

def visualization(buildings: list,poles: list,edges: list = None):
    # Create the map plotter:
    apikey = 'AIzaSyBal6A70lGi745Rm8Fdk0o5FZEleeHhBLI' # (your API key here)
    gmap = gmplot.GoogleMapPlotter(50.165997404672005, 19.625832486967628, 17, apikey=apikey)

    # Highlight buildings:
    for i in range(len(buildings)):
        buildings[i] = (buildings[i].vert_coord,buildings[i].hori_coord)

    building_y, building_x = zip(*buildings)

    gmap.scatter(building_y, building_x, color='r', size=4, marker=False)

    # Highlight poles:
    for i in range(len(poles)):
        poles[i] = (poles[i].vert_coord,poles[i].hori_coord)

    poles_y, poles_x = zip(*poles)

    gmap.scatter(poles_y, poles_x, color='k', size=2, marker=False, symbol = 'x')

    # Create connection between two buildings
    path = zip(*[
        (50.16542348975432, 19.624805930923117),
        (50.16521551792717, 19.624896933788143)])

    gmap.plot(*path, edge_width=4, color='b')

    # Draw the map to an HTML file:
    gmap.draw('map.html')