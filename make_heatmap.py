#!/usr/bin/env python
from  heatmaps.download_data import *
import pandas as pd
import gmplot
import sys
import os
try:
    import cPickle as pickle
except:
    import pickle


def heatmap(client=None):
    print(os.getcwd())
    pass
    map_html = 'templates/heatmaps.heatmap.html'
    sigma = 1.00
    all_act = get_data(client)
    #print(all_act)
    print("Making heatmap")
    heatmap = pd.concat(all_act, ignore_index=True)

    center_lat, center_lon = heatmap['lat'].mode()[0], heatmap['lon'].mode()[0]
    center_lat,center_lon =37,-121
    heatmap = heatmap[heatmap['lat'] <= (center_lat + sigma * center_lat)]
    heatmap = heatmap[heatmap['lat'] >= (center_lat - sigma * center_lat)]
    heatmap = heatmap[heatmap['lon'] >= (center_lon + sigma * center_lon)]
    heatmap = heatmap[heatmap['lon'] <= (center_lon - sigma * center_lon)]
    
    print("Plotting")
    gmap = gmplot.GoogleMapPlotter(center_lat, center_lon, 13)
    gmap.heatmap(heatmap['lat'], heatmap['lon'])
    gmap.draw(map_html)

if __name__ == '__main__':

    # try:
    heatmap()
    # print("Done")
    # except:
    #print("Error in making heatmap")
    # sys.exit()


