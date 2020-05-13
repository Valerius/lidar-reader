class Recording:
  def __init__(self, coordinates, timestamps):
    self.coordinates = coordinates
    self.timestamps = timestamps

  def create_scan(self, scan_coordinates, timestamp):
    index = self.timestamps.index(timestamp)
    return Scan(scan_coordinates, timestamp, index)
  
  def create_scan_from_timestamp(self, timestamp):
    index = self.timestamps.index(timestamp)
    scan_coordinates = self.coordinates[index]
    return Scan(scan_coordinates, timestamp, index)

  def create_scan_from_index(self, index):
    return Scan(self.coordinates[index], self.timestamps[index], index)

  def render_scans(self):
    for timestamp in self.timestamps:
      scan = self.create_scan_from_timestamp(timestamp)
      scan.render_scan()

# Scan class
class Scan:
  def __init__(self, coordinates, timestamp, index):
    self.coordinates = coordinates
    self.timestamp = timestamp

  def render_scan(self):
    pass

