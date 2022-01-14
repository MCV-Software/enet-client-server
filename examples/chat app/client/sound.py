# -*- coding: utf-8 -*-
import threading
import os
import subprocess
import paths
import sound_lib
import output
from sound_lib import recording, stream
from sound_lib import output, input

def recode_audio(filename, quality=10):
    subprocess.call(r'"%s" --downmix -q %r "%s"' % (os.path.join(paths.app_path(), 'oggenc2.exe'), quality, filename))

def get_recording(filename):
    val = recording.WaveRecording(filename=filename)
    return val

class RepeatingTimer(threading.Thread):
    """Call a function after a specified number of seconds, it will then repeat again after the specified number of seconds
Note: If the function provided takes time to execute, this time is NOT taken from the next wait period

t = RepeatingTimer(30.0, f, args=[], kwargs={})
t.start()
t.cancel() # stop the timer's actions
"""

    def __init__(self, interval, function, daemon=True, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = daemon
        self.interval = float(interval)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    stop = cancel

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            if not self.finished.is_set():  #In case someone has canceled while waiting
                try:
                    self.function(*self.args, **self.kwargs)
                except:
                    print("Execution failed. Function: %r args: %r and kwargs: %r" % (self.function, self.args, self.kwargs))

class soundSystem(object):

    def __init__(self):
        """ Sound Player."""
        # Set the output and input default devices.
        try:
            self.output = output.Output()
            self.input = input.Input()
        except:
            pass
        self.files = []
        self.cleaner = RepeatingTimer(60, self.clear_list)
        self.cleaner.start()

    def clear_list(self):
        if len(self.files) == 0: return
        try:
            for i in range(0, len(self.files)):
                if self.files[i].is_playing == False:
                    self.files[i].free()
                    self.files.pop(i)
        except IndexError:
            pass

    def play(self, sound, argument=False):
        sound_object = stream.FileStream(file="%s/%s" % (paths.sound_path(), sound))
        self.files.append(sound_object)
        sound_object.play()

sound = None

def setup():
    global sound
    sound = soundSystem()
