import gmplot

# Create the map plotter:
apikey = 'AIzaSyBal6A70lGi745Rm8Fdk0o5FZEleeHhBLI' # (your API key here)
gmap = gmplot.GoogleMapPlotter(50.165997404672005, 19.625832486967628, 17, apikey=apikey)

# Highlight buildings:
building_y, building_x = zip(*[
    (50.16542348975432, 19.624805930923117),
    (50.16521551792717, 19.624896933788143),
    (50.16538803559229, 19.624432547030786),
    (50.16512627770332, 19.623939738063434)])

gmap.scatter(building_y, building_x, color='#3B0B39', size=3, marker=False)

# Create connection between two buildings
path = zip(*[
    (50.16542348975432, 19.624805930923117),
    (50.16521551792717, 19.624896933788143)])

gmap.plot(*path, edge_width=1, color='red')

# Draw the map to an HTML file:
gmap.draw('map.html')