import matplotlib.pyplot as plt
# For debugging purposes
import pdb
# Clustering module
from sklearn.cluster import DBSCAN
from sklearn import metrics
# Stats library
import numpy as np
# Local modules
import rendering
import clustering

class Recording:
  def __init__(self, coordinates, timestamps):
    self.coordinates = coordinates
    self.timestamps = timestamps
    self.scans = []
    self.clustered = False

  def create_scan(self, scan_coordinates, timestamp, index):
    return Scan(scan_coordinates, timestamp, index)

  def create_scans(self):
    for i, (c, t) in enumerate(zip(self.coordinates, self.timestamps)):
      self.scans.append(self.create_scan(c, t, i))

  def create_clustered_scans(self):
    if self.scans == []:
      self.create_scans()
    for scan in self.scans:
      scan.create_clusters()
    self.clustered = True

  def render_scans(self):
    if self.scans == []:
      self.create_scans()
    for scan in self.scans:
      scan.render()

  def render_clustered_scans(self):
    if self.scans == [] or not self.clustered:
      self.create_clustered_scans()
    for scan in self.scans:
      scan.render_clusters()

class Scan:
  def __init__(self, coordinates, timestamp, index):
    self.coordinates = self.create_coordinates(coordinates)
    self.timestamp = timestamp
    self.index = index
    self.clustering = None
    self.clusters = []
    self.outliers = []

  def coordinates_to_list(self):
    return [(c.x, c.y) for c in self.coordinates]
  
  def x_coordinates_to_list(self):
    return [c.x for c in self.coordinates]

  def y_coordinates_to_list(self):
    return [c.y for c in self.coordinates]

  def create_coordinates(self, coordinates):
    result = []
    for coordinate in coordinates:
      result.append(Coordinate(coordinate[0], coordinate[1]))
    return np.array(result)

  def cluster(self):
    self.clustering = DBSCAN(eps=300, min_samples=2).fit(self.coordinates_to_list())

  def create_clusters(self):
    self.cluster()
    previous_label = 0
    cluster_coordinates = []

    for label, coordinate in zip(self.clustering.labels_, self.coordinates):
      if label >= 0:
        if label > previous_label:
          self.clusters.append(Cluster(cluster_coordinates, previous_label))
          previous_label = label
          cluster_coordinates = []
        cluster_coordinates.append(coordinate)
      else:
        self.outliers.append(coordinate)

  def render(self):
    rendering.render_scatter_plot(
      self.x_coordinates_to_list(), self.y_coordinates_to_list(),
      0, 4000, 'Scan: %d' % self.index,
      'snapshots/scan-%d' % self.index
    )
    
  def render_clusters(self):
    if self.clusters == []:
      self.create_clusters()

    rendering.render_clustered_scan(
      self.clustering,
      self.outliers,
      self.clusters,
      0,
      4000,
      'Clustered scan: %d' % self.index,
      'clustered-snapshots/scan-%d' % self.index
    )

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

# class CoordinatesList:
#   def __init__(self, coordinates):
#     self.coordinates = []

#   def create_(parameter_list):
#     pass

class Cluster:
  def __init__(self, coordinates, label):
    self.coordinates = coordinates
    self.label = label
    self.centroid = self.get_centroid(coordinates)

  def get_centroid(self, coordinates):
    amount = len(coordinates)
    if amount != 0:
      return Centroid(coordinates)

class Centroid:
  def __init__(self, coordinates):
    self.x = self.get_centroid([xc.x for xc in coordinates])
    self.y = self.get_centroid([xc.y for xc in coordinates])

  def get_centroid(self, coordinates):
    return sum(coordinates) / len(coordinates)
