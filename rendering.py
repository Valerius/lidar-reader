# This code uses the NumPy library. We are thankful for the usage of this library. Citation below.
@book{oliphant2006guide,
  title={A guide to NumPy},
  author={Oliphant, Travis E},
  volume={1},
  year={2006},
  publisher={Trelgol Publishing USA}
}

import matplotlib.pyplot as plt
# Stats library
import numpy as np
import pdb

def get_colors(amount):
  return [plt.cm.get_cmap("Spectral")(each) for each in np.linspace(0, 1, amount)]

def render_scatter_plot(x, y, ymin, ymax, title, savefig):
  plt.scatter(x, y)
  plt.ylim(ymin, ymax)
  plt.title(title)
  plt.savefig(savefig)
  plt.close()

def render_clustered_scan(clustering, outliers, clusters, ymin, ymax, title, savefig):
  colors = get_colors(len(clusters))
  for outlier in outliers:
    plt.plot(outlier.x, outlier.y, 'o', markerfacecolor=tuple([0, 0, 0, 1]),
      markeredgecolor='k', markersize=6
    )
  for cluster, color in zip(clusters, colors):
    for coordinate in cluster.coordinates:
      plt.plot(coordinate.x, coordinate.y, 'o', markerfacecolor=tuple(color),
        markeredgecolor='k', markersize=14
      )

  plt.ylim(ymin, ymax)
  plt.title(title)
  plt.savefig(savefig)
  plt.close()

def render_matching_clusters(cluster1, cluster2, title, savefig):
  colors = get_colors(2)

  for coordinate in cluster1.coordinates:
    plt.plot(coordinate.x, coordinate.y, 'o', markerfacecolor=colors[0],
      markeredgecolor='k', markersize=6
    )

  for coordinate in cluster2.coordinates:
    plt.plot(coordinate.x, coordinate.y, 'o', markerfacecolor=colors[1],
      markeredgecolor='k', markersize=6
    )
  
  plt.title(title)
  plt.savefig(savefig)
  plt.close()
    

# def render_clustered_scan(self):
#   core_samples_mask = np.zeros_like(self.clustering.labels_, dtype=bool)
#   core_samples_mask[self.clustering.core_sample_indices_] = True
#   labels = self.clustering.labels_

#   # Black removed and is used for noise instead.
#   unique_labels = set(labels)
#   colors = rendering.get_colors(unique_labels)

#   for k, col in zip(unique_labels, colors):
#       if k == -1:
#           # Black used for noise.
#           col = [0, 0, 0, 1]

#       class_member_mask = (labels == k)
#       #pdb.set_trace()
#       xy = self.coordinates[class_member_mask & core_samples_mask]
#       plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#               markeredgecolor='k', markersize=14)

#       xy = self.coordinates[class_member_mask & ~core_samples_mask]
#       plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#               markeredgecolor='k', markersize=6)
#   plt.title('Clustered scan: %d' % self.index)
#   plt.savefig('clustered-snapshots/scan-%d' % self.index)
#   plt.close()
