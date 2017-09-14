


import myo as libmyo
libmyo.init('./lib')
import time

def main():
    try:
        hub = libmyo.Hub()
    except MemoryError:
        print("Myo Hub could not be created. Make sure Myo Connect is running.")
        return

    feed = libmyo.device_listener.Feed()
    hub.run(1000, feed)
    try:
        print("Waiting for a Myo to connect ...")
        myo = feed.wait_for_single_device(2)
        if not myo:
            print("No Myo connected after 2 seconds.")
            return

        print("Hello, Myo! Requesting RSSI ...")
        myo.request_rssi()
        while hub.running and myo.connected and not myo.rssi:
            print("Waiting for RRSI...")
            time.sleep(0.001)
        print("RSSI:", myo.rssi)
        print("Goodbye, Myo!")
    except KeyboardInterrupt:
        print("Keyboard Interrupt.")
    else:
        print("Myo disconnected.")
    finally:
        print("Shutting down Myo Hub ...")
        hub.shutdown()

if __name__ == "__main__":
    main()
