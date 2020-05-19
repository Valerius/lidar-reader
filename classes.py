# # This code uses the similaritymeasures library for comparing functions. We are thankful for the usage of this library. Citation below.
# @article{Jekel2019,
#   author = {Jekel, Charles F and Venter, Gerhard and Venter, Martin P and Stander, Nielen and Haftka, Raphael T},
#   doi = {10.1007/s12289-018-1421-8},
#   issn = {1960-6214},
#   journal = {International Journal of Material Forming},
#   month = {may},
#   url = {https://doi.org/10.1007/s12289-018-1421-8},
#   year = {2019}
# }

# # This code uses the scikit-learn library. We are thankful for the usage of this library. Citation below.
# @article{scikit-learn,
#   title={Scikit-learn: Machine Learning in {P}ython},
#   author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
#           and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
#           and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and
#           Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
#   journal={Journal of Machine Learning Research},
#   volume={12},
#   pages={2825--2830},
#   year={2011}
# }

# # This code uses the NumPy library. We are thankful for the usage of this library. Citation below.
# @book{oliphant2006guide,
#   title={A guide to NumPy},
#   author={Oliphant, Travis E},
#   volume={1},
#   year={2006},
#   publisher={Trelgol Publishing USA}
# }

import matplotlib.pyplot as plt
# For debugging purposes
import pdb
# Clustering module
from sklearn.cluster import DBSCAN
from sklearn import metrics
# Stats library
import numpy as np
# Similaritymeasures
import similaritymeasures
# Local modules
import rendering
import clustering

class Recording:
  def __init__(self, coordinates, timestamps):
    self.coordinates = coordinates
    self.timestamps = timestamps
    self.scans = []
    self.clustered = False
    self.matching_clusters = []
    self.deltas = []

  def create_scan(self, scan_coordinates, timestamp, index):
    return Scan(scan_coordinates, timestamp, index)

  def create_scans(self):
    for i, (c, t) in enumerate(zip(self.coordinates, self.timestamps)):
      self.scans.append(self.create_scan(c, t, i))

  def cluster(self):
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

  def render_clusters(self):
    if self.scans == [] or not self.clustered:
      self.cluster()
    for scan in self.scans:
      scan.render_clusters()

  def match_clusters(self):
    if self.matching_clusters == []:
      self.cluster()
      previous_scan = None
      for scan in self.scans:
        if previous_scan != None:
          self.matching_clusters.append(clustering.compare_scans(scan, previous_scan))
        previous_scan = scan

  def render_matching_clusters(self):
    self.match_clusters()
    for index, match in enumerate(self.matching_clusters):
      if match != None:
        rendering.render_matching_clusters(match[0], match[1], 'Scan: %d' % index, 'matching-clusters/%d' % index)
      
  def calculate_deltas(self):
    self.match_clusters()
    for match in self.matching_clusters:
      if match != None:
        self.deltas.append(clustering.calculate_cluster_distance(match[0], match[1]))
      else:
        self.deltas.append(None)

  def render_delta(self):
    self.calculate_deltas()
    rendering.render_linegraph(self.deltas)
      


class Scan:
  def __init__(self, coordinates, timestamp, index):
    self.coordinates = self.create_coordinates(coordinates)
    self.timestamp = timestamp
    self.index = index
    self.clustering = None
    self.clusters = []
    self.outliers = []
    self.clusters_coordinates_second_quartile = None

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
    self.clustering = DBSCAN(eps=350, min_samples=2).fit(self.coordinates_to_list())

  def create_clusters(self):
    self.cluster()
    previous_label = 0
    cluster_coordinates = []
    cluster_coordinates_counts = []

    for label, coordinate in zip(self.clustering.labels_, self.coordinates):
      if label >= 0:
        if label > previous_label:
          cluster_coordinates_counts.append(len(cluster_coordinates))
          self.clusters.append(Cluster(cluster_coordinates, previous_label))
          previous_label = label
          cluster_coordinates = []
        cluster_coordinates.append(coordinate)
      else:
        self.outliers.append(coordinate)
    self.clusters_coordinates_second_quartile = np.percentile(cluster_coordinates_counts, 75)

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

class Cluster:
  def __init__(self, coordinates, label):
    self.coordinates = coordinates
    self.label = label
    self.centroid = self.get_centroid(coordinates)

  def get_centroid(self, coordinates):
    amount = len(coordinates)
    if amount != 0:
      return Centroid(coordinates)

  def coordinates_to_list(self):
    return [(c.x, c.y) for c in self.coordinates]

  def coordinates_to_array(self):
    return np.array(self.coordinates_to_list())

class Centroid:
  def __init__(self, coordinates):
    self.x = self.get_centroid([xc.x for xc in coordinates])
    self.y = self.get_centroid([xc.y for xc in coordinates])

  def get_centroid(self, coordinates):
    return sum(coordinates) / len(coordinates)
