# *- coding: utf-8 -*-
""" Simple (really simple) module to provide text to speech output in a chat window."""
import logging as original_logging
logger = original_logging.getLogger('core.output')
from accessible_output2 import outputs
import sys

speaker = None
retries = 0

def speak(text, interrupt=0):
    global speaker, retries
    if not speaker:
        setup()
    try:
        speaker.speak(text, interrupt)
    except:
        if retries < 5:
            retries = retries + 1
            speak(text)

def setup ():
    global speaker
    logger.debug("Initializing output subsystem.")
    try:
        speaker = outputs.auto.Auto()
    except:
        logger.exception("Output: Error during initialization.")

def enable_sapi():
    speaker = outputs.sapi.SAPI5()
