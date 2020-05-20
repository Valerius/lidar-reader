# # This code uses the similaritymeasures library for comparing functions. We are thankful for the usage of this library. Citation below.
# @article{Jekel2019,
#   author = {Jekel, Charles F and Venter, Gerhard and Venter, Martin P and Stander, Nielen and Haftka, Raphael T},
#   doi = {10.1007/s12289-018-1421-8},
#   issn = {1960-6214},
#   journal = {International Journal of Material Forming},
#   month = {may},
#   title = {{Similarity measures for identifying material parameters from hysteresis loops using inverse analysis}},
#   url = {https://doi.org/10.1007/s12289-018-1421-8},
#   year = {2019}
# }

# # This code uses the scikit-learn library. We are thankful for the usage of this library. Citation below.
# @article{scikit-learn,
#  title={Scikit-learn: Machine Learning in {P}ython},
#  author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
#          and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
#          and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and
#          Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
#  journal={Journal of Machine Learning Research},
#  volume={12},
#  pages={2825--2830},
#  year={2011}
# }

import math as m
from sklearn import metrics
import numpy as np
from classes import *
# Similaritymeasures
import similaritymeasures

def calculate_coordinate_distance(x1, x2, y1, y2):
  return m.sqrt((max(x1, x2) - min(x1, x2))**2 + (max(y1, y2) - min(y1, y2))**2)

def get_closest_centroids(centroids, previous_centroids):
  smallest_distance = 0
  for i, c in enumerate(centroids):
    for j, pc in enumerate(previous_centroids):
      distance = calculate_coordinate_distance(c[0], pc[0], c[1], pc[1])
      if distance < smallest_distance or (i == 0 and j == 0):
        smallest_distance = distance
  return smallest_distance

def compare_clusters(cluster1, cluster2):
  return similaritymeasures.area_between_two_curves(cluster1.coordinates_to_array(), cluster2.coordinates_to_array())

def compare_scans(scan1, scan2):
  minimum_area = None
  minimum_clusters = None
  for c1 in scan1.clusters:
    if len(c1.coordinates) > scan1.clusters_coordinates_last_decile:
      for c2 in scan2.clusters:
        if len(c2.coordinates) > scan2.clusters_coordinates_last_decile:
          area = compare_clusters(c1, c2)
          if minimum_area == None or area < minimum_area:
            minimum_area = area
            minimum_clusters = (c1, c2)
  return minimum_clusters

def calculate_cluster_distance(cluster1, cluster2):
  centroids_x = [cluster1.centroid.x, cluster2.centroid.x]
  return max(centroids_x) - min(centroids_x)
