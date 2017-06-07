# coding=utf-8
# This module has been taken from https://github.com/swharden/Python-GUI-examples
# Thank you swharden

import pyaudio
import time
import numpy as np
import threading


def getFFT(data, rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    data *= np.hamming(len(data))
    fft = np.fft.fft(data)
    fft = np.abs(fft)
    freq = np.fft.fftfreq(len(fft), 1.0 / rate)
    return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


class SWHear:
    def __init__(self, device=None, rate=None, updatesPerSecond=10):
        self.p = pyaudio.PyAudio()
        self.chunk = 4096  # gets replaced automatically
        self.updatesPerSecond = updatesPerSecond
        self.chunksRead = 0
        self.device = device
        self.rate = rate

    def valid_low_rate(self, device):
        """set the rate to the lowest supported audio rate."""
        for testrate in [44100]:
            if self.valid_test(device, testrate):
                return testrate
        return None

    def valid_test(self, device, rate=44100):
        """given a device ID and a rate, return TRUE/False if it's valid."""
        try:
            self.info = self.p.get_device_info_by_index(device)
            if not self.info["maxInputChannels"] > 0:
                return False
            stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                 input_device_index=device, frames_per_buffer=self.chunk,
                                 rate=int(self.info["defaultSampleRate"]), input=True)
            stream.close()
            return True
        except:
            return False

    def valid_input_devices(self):
        mics = []
        for device in range(self.p.get_device_count()):
            if self.valid_test(device):
                mics.append(device)
        return mics

    def initiate(self):
        if self.device is None:
            self.device = self.valid_input_devices()[0]  # pick the first one
        if self.rate is None:
            self.rate = self.valid_low_rate(self.device)
        self.chunk = int(self.rate / self.updatesPerSecond)  # hold one tenth of a second in memory
        if not self.valid_test(self.device, self.rate):
            self.device = self.valid_input_devices()[0]  # pick the first one
            self.rate = self.valid_low_rate(self.device)
        self.datax = np.arange(self.chunk) / float(self.rate)

    def close(self):
        self.keepRecording = False  # the threads should self-close
        while self.t.isAlive():  # wait for all threads to close
            time.sleep(.1)
        self.stream.stop_stream()
        self.p.terminate()

    def stream_readchunk(self):
        try:
            self.data = np.fromstring(self.stream.read(self.chunk), dtype=np.int16)
            self.fftx, self.fft = getFFT(self.data, self.rate)

        except Exception as E:
            self.keepRecording = False
        if self.keepRecording:
            self.stream_thread_new()
        else:
            self.stream.close()
            self.p.terminate()
        self.chunksRead += 1

    def stream_thread_new(self):
        self.t = threading.Thread(target=self.stream_readchunk)
        self.t.start()

    def stream_start(self):
        self.initiate()
        self.keepRecording = True  # set this to False later to terminate stream
        self.data = None  # will fill up with threaded recording data
        self.fft = None
        self.dataFiltered = None  # same
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                  rate=self.rate, input=True, frames_per_buffer=self.chunk)
        self.stream_thread_new()
