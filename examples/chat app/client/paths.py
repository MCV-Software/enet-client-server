# -*- coding: utf-8 -*-
import os
from platform_utils import paths as paths_

def app_path():
    return paths_.app_path()

def locale_path():
    return os.path.join(app_path(), "locales")

def sound_path():
    return os.path.join(app_path(), "sounds")
