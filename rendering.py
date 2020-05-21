# # This code uses the NumPy library. We are thankful for the usage of this library. Citation below.
# @book{oliphant2006guide,
#   title={A guide to NumPy},
#   author={Oliphant, Travis E},
#   volume={1},
#   year={2006},
#   publisher={Trelgol Publishing USA}
# }

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

  for coordinate in cluster1.coordinate_list.coordinates:
    plt.plot(coordinate.x, coordinate.y, 'o', markerfacecolor=colors[0],
      markeredgecolor='k', markersize=6
    )

  for coordinate in cluster2.coordinate_list.coordinates:
    plt.plot(coordinate.x, coordinate.y, 'o', markerfacecolor=colors[1],
      markeredgecolor='k', markersize=6
    )
  
  plt.title(title)
  plt.savefig(savefig)
  plt.close()

def render_linegraph(lst):
  for index, item in enumerate(lst):
    if item != None and item > 50 and item < 500:
      plt.plot(index, item, 'o', markerfacecolor=tuple([0, 0, 0, 1]),
        markeredgecolor='k', markersize=6
      )
  plt.title('distances')
  plt.savefig('distances/distances')
  plt.close()

# def render_train_recording(self):
# # Lege plot ophalen met bepaalde verhouding, zodat het op een trein lijkt
# recording = render_scatter_plot(0, 0, ymin, ymax, "Recording", savefig)
# # Scans ophalen en over itereren
#   for rotation in rotations:
# # Eerst acceleratie van trein ophalen tussen 2 scans en vervolgens berekenen hoeveel x-as veranderd
#     acceleration = calculate_cluster_acceleration(vorige scan, huidige scan)
# # Voeg huidige acceleratie toe aan x-as
#     x += acceleration
# # Per rotation de scan ophalen en toevoegen aan een variabele van een plaatje
#     rotation.append(recording)
# # Aan einde van alle rotations plot renderen en opslaan
# recording.save()
