import math as m
from sklearn import metrics
import numpy as np
from classes import *

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



def find_closest_clusters(current_clusters, previous_clusters):
  result = []
  for i, cc in enumerate(current_clusters):
    for j, pc in enumerate(previous_clusters):
      cc_centroid = cc.get_y_centroid(len(cc))
      pc_centroid = pc.get_y_centroid()

      distance = calculate_coordinate_distance(cc_centroid[0], pc_centroid[0], cc_centroid[1], pc_centroid[1])

      result.append((distance, cc_centroid, pc_centroid, cc, pc))

  return min(result, key = lambda t: t[0])


def calculate_adjusted_rand_score(list1, list2):
  return metrics.adjusted_rand_score(np.array(list1), np.array(list2))