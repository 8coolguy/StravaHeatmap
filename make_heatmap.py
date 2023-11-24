#!/usr/bin/env python
#from  heatmaps.download_data import *
from heatmaps.download_data import *

from sklearn.cluster import MeanShift
import pandas as pd
import gmplot
import sys
import os
try:
    import cPickle as pickle
except:
    import pickle


def heatmap(client=None,sig=.5,z=13):
    print(os.getcwd())
    map_html = 'templates/heatmaps/heatmap.html'
    map_html="heatmap.html"
    sigma = sig
    all_act = get_data(client)
    #print(all_act)
    print("Making heatmap")
    heatmap = pd.concat(all_act, ignore_index=True)
    points =heatmap[['lat','lon']]
    print(points.shape)
    print("Clustering Points")
    clustering = MeanShift(bandwidth=1).fit(points)
    center_cluster=clustering.labels_.mode()[0]
    print(center_cluster)
    center_lat, center_lon = heatmap['lat'].mode()[0], heatmap['lon'].mode()[0]
    #center_lat,center_lon =
    heatmap = heatmap[heatmap['lat'] <= (center_lat + sigma * center_lat)]
    heatmap = heatmap[heatmap['lat'] >= (center_lat - sigma * center_lat)]
    heatmap = heatmap[heatmap['lon'] >= (center_lon + sigma * center_lon)]
    heatmap = heatmap[heatmap['lon'] <= (center_lon - sigma * center_lon)]
    
    print("Plotting")
    gmap = gmplot.GoogleMapPlotter(center_lat, center_lon, zoom=z)
    gmap.heatmap(heatmap['lat'], heatmap['lon'])
    gmap.draw(map_html)

if __name__ == '__main__':

    # try:
    heatmap(sig = .3)
    # print("Done")
    # except:
    #print("Error in making heatmap")
    # sys.exit()


