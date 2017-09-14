import collections
import threading
import time

import myo
import myo as libmyo
libmyo.init('./lib')

class MyoListener(myo.DeviceListener):

  def __init__(self, queue_size=8):
    self.lock = threading.Lock()
    self.emg_data_queue = collections.deque(maxlen=queue_size)

  def on_connect(self, device, timestamp, firmware_version):
    device.set_stream_emg(myo.StreamEmg.enabled)

  def on_emg_data(self, device, timestamp, emg_data):
    with self.lock:
      self.emg_data_queue.append((timestamp, emg_data))

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)


hub = myo.Hub()
try:
  listener = MyoListener()
  hub.run(200, listener)
  while True:
    print(listener.get_emg_data())
    time.sleep(1.0)
finally:
  hub.shutdown()