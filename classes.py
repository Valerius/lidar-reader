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
    self.centroids = []
    self.scans = []

  def build_clustered_scans(self):
    for timestamp in self.timestamps:
      self.scans.append(self.create_clustered_scan_from_timestamp(timestamp))
  
  def create_scan_from_timestamp(self, timestamp):
    index = self.timestamps.index(timestamp)
    return Scan(self.coordinates[index], timestamp, index)

  def create_clustered_scan_from_timestamp(self, timestamp):
    index = self.timestamps.index(timestamp)
    return ClusteredScan(self.coordinates[index], timestamp, index)

  def create_scan_from_index(self, index):
    return Scan(self.coordinates[index], self.timestamps[index], index)

  def render_scans(self):
    for timestamp in self.timestamps:
      scan = self.create_scan_from_timestamp(timestamp)
      scan.render_scan()
    return len(self.timestamps)
  
  def render_clustered_scans(self):
    for timestamp in self.timestamps:
      scan = self.create_clustered_scan_from_timestamp(timestamp)
      scan.render_clustered_scan()
    return len(self.timestamps)
  
  def get_centroids(self):
    for timestamp in self.timestamps:
      scan = self.create_clustered_scan_from_timestamp(timestamp)
      scan.get_centroids()
      self.centroids.append(scan.centroids)

  def get_minimal_centroid_differences(self):
    result = []
    if self.get_centroids == []:
      self.get_centroids()
    previous_scan_centroids = None

    for scan_centroids in self.centroids:
      if previous_scan_centroids != None:
        result.append(clustering.get_closest_centroids(scan_centroids, previous_scan_centroids))
      previous_scan_centroids = scan_centroids
    return result

  def get_matching_clusters(self):
    self.build_clustered_scans()
    result = []
    previous_scan = None
    for i, scan in enumerate(self.scans):
      if i > 0:
        result.append(scan.calculate_jaccard_similarity(previous_scan))
      previous_scan = scan
    return result

class RecordingWithScans(object):
  pass

# Scan class
class Scan:
  def __init__(self, coordinates, timestamp, index):
    self.coordinates = np.array(coordinates)
    self.timestamp = timestamp
    self.index = index

  def render_scan(self):
    x = [s[0] for s in self.coordinates]
    y = [s[1] for s in self.coordinates]
    plt.scatter(x, y)
    plt.ylim(0, 4000)
    plt.title('Scan: %d' % self.index)
    plt.savefig('snapshots/scan-%d' % self.index)
    plt.close()

class ClusteredScan(Scan):
  def __init__(self, coordinates, timestamp, index):
    super().__init__(coordinates, timestamp, index)
    self.clustering = DBSCAN(eps=300, min_samples=2).fit(self.coordinates)
    self.clusters = []
    self.centroids = []

  def build_clusters(self):
    previous_label = 0
    cluster_coordinates = []

    for label, coordinate in zip(self.clustering.labels_, self.coordinates):
      if label >= 0:
        if label > previous_label:
          self.clusters.append(Cluster(cluster_coordinates, previous_label))
          previous_label = label
          cluster_coordinates = []
        cluster_coordinates.append(coordinate)

  def get_centroids(self):
    self.build_clusters()
    for cluster in self.clusters:
      self.centroids.append(cluster.get_centroid())

  def render_clustered_scan(self):
    core_samples_mask = np.zeros_like(self.clustering.labels_, dtype=bool)
    core_samples_mask[self.clustering.core_sample_indices_] = True
    labels = self.clustering.labels_

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = rendering.get_colors(unique_labels)

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)
        #pdb.set_trace()
        xy = self.coordinates[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                markeredgecolor='k', markersize=14)

        xy = self.coordinates[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                markeredgecolor='k', markersize=6)
    plt.title('Clustered scan: %d' % self.index)
    plt.savefig('clustered-snapshots/scan-%d' % self.index)
    plt.close()

  def calculate_jaccard_similarity(self, previous_scan):
    self.build_clusters()
    previous_scan.build_clusters()
    return clustering.find_closest_clusters(self.clusters, previous_scan.clusters)

class Cluster:
  def __init__(self, coordinates, label):
    self.coordinates = coordinates
    self.label = label

  def get_centroid(self):
    amount = len(self.coordinates)
    if amount != 0:
      return (self.get_x_centroid(amount), self.get_y_centroid(amount))
  
  def get_y_centroid(self, amount):
    y = [c[1] for c in self.coordinates]
    return sum(y) / amount
  
  def get_x_centroid(self, amount):
    x = [c[0] for c in self.coordinates]
    return sum(x) / amount

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y
