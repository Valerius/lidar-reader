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
  def __init__(self, coordinates, angles, timestamps):
    self.coordinates = coordinates
    self.angles = angles
    self.timestamps = timestamps
    self.scan_list = ScanList(coordinates, angles, timestamps)

class Scan:
  def __init__(self, coordinates, angles, timestamp, index):
    clustering = self.cluster(coordinates)
    coordinate_list = CoordinateList(coordinates, angles)
    self.coordinate_list = coordinate_list
    self.timestamp = timestamp
    self.index = index
    self.clustering = clustering
    self.clusters = list()
    self.outliers = list()
    self.cluster_selection = None

    self.create_clusters(clustering, coordinate_list)

  def cluster(self, coordinates, eps = 300, min_samples = 2):
    return DBSCAN(eps, min_samples).fit(coordinates)

  def create_clusters(self, clustering, coordinate_list, precision = 25):
    previous_label = 0
    cluster_coordinates = []
    cluster_coordinates_counts = []

    for index, (label, coordinate) in enumerate(zip(clustering.labels_, coordinate_list.coordinates)):
      if label >= 0:
        if label > previous_label or (index + 1) is len(clustering.labels_):
          cluster_coordinates_counts.append(len(cluster_coordinates))
          self.clusters.append(Cluster(cluster_coordinates, previous_label))
          previous_label = label
          cluster_coordinates = []
        cluster_coordinates.append(coordinate)
      else:
        self.outliers.append(coordinate)
    self.cluster_selection = np.percentile(cluster_coordinates_counts, 100 - precision)

  def render(self):
    rendering.render_scatter_plot(
      self.coordinate_list.x_to_list(), self.coordinate_list.y_to_list(),
      0, 4000, 'Scan: %d' % self.index,
      'scans/scan-%d' % self.index,
      'scans'
    )

  def render_clusters(self):
    rendering.render_clustered_scan(
      self.clustering,
      self.outliers,
      self.clusters,
      0,
      4000,
      'Clustered scan: %d' % self.index,
      'clustered-snapshots/scan-%d' % self.index,
      'clustered-snapshots'
    )

class ScanList:
  def __init__(self, coordinates, angles, timestamps):
    self.scans = self.create_scans(coordinates, angles, timestamps)
    self.matches = list()
    self.deltas = list()
    self.fitted = list()

  def create_scans(self, coordinates, angles, timestamps):
    return list(Scan(c, a, t, i) for i, (c, a, t) in enumerate(zip(coordinates, angles, timestamps)))

  def render(self):
    for scan in self.scans:
      scan.render()

  def render_clusters(self):
    for scan in self.scans:
      scan.render_clusters()

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
        rendering.render_matching_clusters(match[0], match[1], 'Scan: %d' % index, 'matching-clusters/%d' % index, 'matching-clusters')

  def delta(self):
    if not self.matches:
      self.match()
    for match in self.matches:
      if match is not None:
        self.deltas.append(clustering.calculate_cluster_distance(match[0], match[1]))
      else:
        self.deltas.append(None)

  def render_deltas(self):
    if not self.deltas:
      self.delta()
    rendering.render_linegraph(self.deltas)
  
  def fit(self):
    if not self.deltas:
      self.delta()
    
    self.fitted = np.polynomial.Polynomial.fit(
      np.arange(len(self.deltas)), self.deltas, 3
    ).linspace(len(self.deltas))[1]

  def render_complete(self):
    if not self.fitted:
      self.fit()
    incrementation = 0.0
    xmin = 0
    xmax = 0
    fig = plt.figure(figsize=(30, 2))
    ax = fig.add_subplot(111)

    for index, scan in enumerate(self.scans):
      if index > 0:
        incrementation += self.fitted[index - 1]
        ax.plot(scan.coordinate_list.x_list_incr(incrementation), scan.coordinate_list.y_to_list(), 'o',
          markerfacecolor=tuple([0, 0, 0, 1]), markeredgecolor='k', markersize=0.5)
        xmax = max(scan.coordinate_list.x_list_incr(incrementation))
      else:
        xmin = min(scan.coordinate_list.x_to_list())
        ax.plot(scan.coordinate_list.x_to_list(), scan.coordinate_list.y_to_list(), 'o',
          markerfacecolor=tuple([0, 0, 0, 1]), markeredgecolor='k', markersize=0.5)
    ax.set_xlim([xmin,xmax])
    plt.tight_layout()
    plt.title('complete')
    plt.savefig('complete')
    plt.close()

class Coordinate:
  def __init__(self, x, y, angle):
    self.x = x
    self.y = y
    self.angle = angle

class CoordinateList:
  def __init__(self, coordinates, angles = None):
    try:
      self.coordinates = self.create_coordinates(coordinates, angles)
    except:
      self.coordinates = list(coordinates)

  def create_coordinates(self, coordinates, angles):
    return list(Coordinate(c[0], c[1], a) for c, a in zip(coordinates, angles))

  def to_list(self):
    return list((c.x, c.y) for c in self.coordinates)

  def x_to_list(self):
    return list(c.x for c in self.coordinates)

  def y_to_list(self):
    return list(c.y for c in self.coordinates)

  def x_list_incr(self, incr):
    return list(c.x + incr for c in self.coordinates)

  def y_list_incr(self, incr):
    return list(c.y + incr for c in self.coordinates)

  def to_array(self):
    return np.array(self.to_list())

  def len(self):
    return len(self.coordinates)

class Cluster:
  def __init__(self, coordinates, label):
    self.coordinate_list = CoordinateList(coordinates = coordinates)
    self.label = label
    self.centroid = Centroid(coordinates)

class Centroid:
  def __init__(self, coordinates):
    self.x = self.get_centroid([c.x for c in coordinates])
    self.y = self.get_centroid([c.y for c in coordinates])

  def get_centroid(self, coordinates):
    return np.median(coordinates)
