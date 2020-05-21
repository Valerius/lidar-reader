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

# Data structure explained:
# A RECORDING has many SCANS
# A SCAN has one COORDINATE_LIST with many COORDINATES
# A SCAN has one CLUSTER_LIST with many CLUSTERS
# A CLUSTER has one COORDINATE_LIST with many COORDINATES
# A CLUSTER has one CENTROID

class Recording:
  def __init__(self, coordinates, timestamps):
    self.coordinates = coordinates
    self.timestamps = timestamps

  def scan(self):
    return RecordingWithScans.from_parent(self)

  def cluster(self):
    return RecordingWithClusteredScans.from_parent(self.scan())

class RecordingWithScans(Recording):
  @classmethod
  def from_parent(cls, parent):
    return cls(parent.coordinates, parent.timestamps)

  def __init__(self, coordinates, timestamps):
    super(RecordingWithScans, self).__init__(coordinates, timestamps)
    self.scan_list = ScanList(coordinates, timestamps)

  def cluster(self):
    return RecordingWithClusteredScans.from_parent(self)

class RecordingWithClusteredScans(RecordingWithScans):
  @classmethod
  def from_parent(cls, parent):
    return cls(parent.coordinates, parent.timestamps, parent.scan_list)

  def __init__(self, coordinates, timestamps, scan_list):
    super(RecordingWithClusteredScans, self).__init__(coordinates, timestamps)
    self.scan_list = ClusteredScanList.from_parent(coordinates, timestamps, scan_list)

  def match(self):
    self.scan_list.match()

  def delta_match(self):
    self.scan_list.delta_match()

  def render_delta_matches(self):
    self.scan_list.render_delta_matches()

class Scan:
  def __init__(self, coordinates, timestamp, index):
    self.coordinate_list = CoordinateList(coordinates)
    self.timestamp = timestamp
    self.index = index

  def cluster(self):
    return ClusteredScan.from_parent(self)

  def render(self):
    rendering.render_scatter_plot(
      self.coordinate_list.x_to_list(), self.coordinate_list.y_to_list(),
      0, 4000, 'Scan: %d' % self.index,
      'snapshots/scan-%d' % self.index
    )

class ClusteredScan(Scan):
  @classmethod
  def from_parent(cls, parent):
    return cls(parent.coordinate_list, parent.timestamp, parent.index)

  def __init__(self, coordinate_list, timestamp, index):
    super(ClusteredScan, self).__init__(coordinate_list.to_list(), timestamp, index)
    clustering = self.cluster(coordinate_list.to_list())
    self.clustering = clustering
    self.cluster_selection = None
    self.clusters = list()
    self.outliers = list()

    self.create_clusters(clustering, coordinate_list.coordinates)

  def cluster(self, coordinates):
    return DBSCAN(eps=300, min_samples=2).fit(coordinates)

  def create_clusters(self, clustering, coordinates):
    previous_label = 0
    cluster_coordinates = []
    cluster_coordinates_counts = []

    for index, (label, coordinate) in enumerate(zip(clustering.labels_, coordinates)):
      if label >= 0:
        if label > previous_label or (index + 1) is len(clustering.labels_):
          cluster_coordinates_counts.append(len(cluster_coordinates))
          self.clusters.append(Cluster(cluster_coordinates, previous_label))
          previous_label = label
          cluster_coordinates = []
        cluster_coordinates.append(coordinate)
      else:
        self.outliers.append(coordinate)
    self.cluster_selection = np.percentile(cluster_coordinates_counts, 75)

  def render(self):
    rendering.render_clustered_scan(
      self.clustering,
      self.outliers,
      self.clusters,
      0,
      4000,
      'Clustered scan: %d' % self.index,
      'clustered-snapshots/scan-%d' % self.index
    )

  def render_scan(self):
    super(ClusteredScan, self).render()

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class CoordinateList:
  def __init__(self, coordinates):
    try:
      self.coordinates = list(Coordinate(c[0], c[1]) for c in coordinates)
    except:
      self.coordinates = list(coordinates)

  def to_list(self):
    return list((c.x, c.y) for c in self.coordinates)

  def x_to_list(self):
    return list(c.x for c in self.coordinates)

  def y_to_list(self):
    return list(c.y for c in self.coordinates)

  def to_array(self):
    return np.array(self.to_list())

  def len(self):
    return len(self.coordinates)

class ScanList:
  def __init__(self, coordinates, timestamps):
    self.scans = list(Scan(c, t, i) for i, (c, t) in enumerate(zip(coordinates, timestamps)))

  def render(self):
    for scan in self.scans:
      scan.render()

class ClusteredScanList(ScanList):
  @classmethod
  def from_parent(cls, coordinates, timestamps, parent):
    return cls(coordinates, timestamps, parent.scans)

  def __init__(self, coordinates, timestamps, scans):
    super(ClusteredScanList, self).__init__(coordinates, timestamps)
    self.cluster(scans)
    self.matches = list()
    self.delta_matches = list()
    self.fitted_delta_matches = list()
    
  def cluster(self, scans):
    for index, scan in enumerate(scans):
      self.scans[index] = scan.cluster()

  def render(self):
    for scan in self.scans:
      scan.render()

  def render_scans(self):
    for scan in self.scans:
      scan.render_scan()

  def match(self):
    previous_scan = None
    for scan in self.scans:
      if previous_scan is not None:
        self.matches.append(clustering.compare_scans(previous_scan, scan))
      previous_scan = scan

  def render_matches(self):
    if not self.matches:
      self.match()
    for index, match in enumerate(self.matches):
      if match != None:
        rendering.render_matching_clusters(match[0], match[1], 'Scan: %d' % index, 'matching-clusters/%d' % index)

  def delta_match(self):
    if not self.matches:
      self.match()
    for match in self.matches:
      if match is not None:
        self.delta_matches.append(clustering.calculate_cluster_distance(match[0], match[1]))
      else:
        self.delta_matches.append(None)

  def render_delta_matches(self):
    if not self.delta_matches:
      self.delta_match()
    rendering.render_linegraph(self.delta_matches)

  def fitted_delta_match(self):
    if not self.delta_matches:
      self.delta_match()
    
    self.fitted_delta_matches = np.polynomial.Polynomial.fit(
      np.arange(len(self.delta_matches)), self.delta_matches, 3
    ).linspace(len(self.delta_matches))[1]

class Cluster:
  def __init__(self, coordinates, label):
    self.coordinate_list = CoordinateList(coordinates)
    self.label = label
    self.centroid = Centroid(coordinates)

class Centroid:
  def __init__(self, coordinates):
    self.x = self.get_centroid([xc.x for xc in coordinates])
    self.y = self.get_centroid([xc.y for xc in coordinates])

  def get_centroid(self, coordinates):
    return np.median(coordinates)


# class Recording:
#   def __init__(self, coordinates, timestamps):
#     self.coordinate_list = CoordinateList(coordinates)
#     self.timestamps = timestamps


#     self.matching_clusters = []
#     self.deltas = []

#   def create_scan(self, scan_coordinates, timestamp, index):
#     return Scan(scan_coordinates, timestamp, index)

#   def cluster(self):
#     if self.scans == []:
#       self.create_scans()
#     for scan in self.scans:
#       scan.create_clusters()
#     self.clustered = True
#     print('Clustering complete')

#   def render_scans(self):
#     if self.scans == []:
#       self.create_scans()
#     for scan in self.scans:
#       scan.render()

#   def render_clusters(self):
#     if self.scans == [] or not self.clustered:
#       self.cluster()
#     for scan in self.scans:
#       scan.render_clusters()

#   def match_clusters(self):
#     if self.matching_clusters == []:
#       self.cluster()
#     previous_scan = None
#     for scan in self.scans:
#       if previous_scan != None:
#         self.matching_clusters.append(clustering.compare_scans(scan, previous_scan))
#       previous_scan = scan
#     print('Clusters matched')

#   def render_matching_clusters(self):
#     self.match_clusters()
#     for index, match in enumerate(self.matching_clusters):
#       if match != None:
#         rendering.render_matching_clusters(match[0], match[1], 'Scan: %d' % index, 'matching-clusters/%d' % index)
      
#   def calculate_deltas(self):
#     self.match_clusters()
#     for match in self.matching_clusters:
#       if match != None:
#         self.deltas.append(clustering.calculate_cluster_distance(match[0], match[1]))
#       else:
#         self.deltas.append(None)
#     print('Deltas calculated')

#   def render_delta(self):
#     self.calculate_deltas()
#     rendering.render_linegraph(self.deltas)

# class RecordingWithScans(Recording):
#   @classmethod
#   def from_parent(cls, parent):
#     return cls(parent.coordinates, parent.timestamps)

#   def __init__(self, coordinates, timestamps):
#     super(RecordingWithScans, self).__init__(coordinates, timestamps)
#     self.scans = ScanList(coordinates, timestamps)

# class RecordingWithClusteredScans(RecordingWithScans):
#   @classmethod
#   def from_parent(cls, parent):
#     return cls(parent.coordinates, parent.timestamps)

#   def __init__(self, coordinates, timestamps):
#     super(RecordingWithClusteredScans, self).__init__(coordinates, timestamps)
#     self.clustering = DBSCAN(eps=300, min_samples=2).fit(self.coordinates.to_list())


# class Scan:
#   def __init__(self, coordinates, timestamp, index):
#     self.coordinate_list = CoordinateList(coordinates)
#     self.timestamp = timestamp
#     self.index = index
#     self.clustering = None
#     self.clusters = []
#     self.outliers = []
#     self.cluster_selection = None

#   def cluster(self):
#     self.clustering = DBSCAN(eps=300, min_samples=2).fit(self.coordinates_to_list())

#   def create_clusters(self):
#     self.cluster()
#     previous_label = 0
#     cluster_coordinates = []
#     cluster_coordinates_counts = []

#     for label, coordinate in zip(self.clustering.labels_, self.coordinate_list):
#       if label >= 0:
#         if label > previous_label:
#           cluster_coordinates_counts.append(len(cluster_coordinates))
#           self.clusters.append(Cluster(cluster_coordinates, previous_label))
#           previous_label = label
#           cluster_coordinates = []
#         cluster_coordinates.append(coordinate)
#       else:
#         self.outliers.append(coordinate)
#     self.clusters_coordinates_last_decile = np.percentile(cluster_coordinates_counts, 90)

#   def render(self):
#     rendering.render_scatter_plot(
#       self.x_coordinates_to_list(), self.y_coordinates_to_list(),
#       0, 4000, 'Scan: %d' % self.index,
#       'snapshots/scan-%d' % self.index
#     )
    
#   def render_clusters(self):
#     if self.clusters == []:
#       self.create_clusters()

#     rendering.render_clustered_scan(
#       self.clustering,
#       self.outliers,
#       self.clusters,
#       0,
#       4000,
#       'Clustered scan: %d' % self.index,
#       'clustered-snapshots/scan-%d' % self.index
#     )

# class Coordinate:
#   def __init__(self, x, y):
#     self.x = x
#     self.y = y

# class CoordinateList:
#   def __init__(self, coordinates):
#     try:
#       self.coordinates = list(Coordinate(c[0], c[1]) for c in coordinates)
#     except:
#       self.coordinates = list(coordinates)

#   def to_list(self):
#     return list((c.x, c.y) for c in self.coordinates)
    
#   def to_array(self):
#     return np.array(list((c.x, c.y) for c in self.coordinates))

#   def x_to_list(self):
#     return list(c.x for c in self.coordinates)

#   def y_to_list(self):
#     return list(c.y for c in self.coordinates)

# class ScanList:
#   def __init__(self, coordinates, timestamps):
#     self.scans = list(Scan(c, t, i) for i, (c, t) in enumerate(zip(coordinates, timestamps)))

# class Cluster:
#   def __init__(self, coordinates, label):
#     self.coordinates = coordinates
#     self.label = label
#     self.centroid = self.get_centroid(coordinates)

#   def get_centroid(self, coordinates):
#     amount = len(coordinates)
#     if amount != 0:
#       return Centroid(coordinates)

#   def coordinates_to_list(self):
#     return [(c.x, c.y) for c in self.coordinates]

#   def coordinates_to_array(self):
#     return np.array(self.coordinates_to_list())

# class Centroid:
#   def __init__(self, coordinates):
#     self.x = self.get_centroid([xc.x for xc in coordinates])
#     self.y = self.get_centroid([xc.y for xc in coordinates])

#   def get_centroid(self, coordinates):
#     return sum(coordinates) / len(coordinates)
