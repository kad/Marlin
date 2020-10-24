import os
import shutil

Import("env")

FIXES_DIR = os.path.join("buildroot","share","PlatformIO","fixes")
assert os.path.isdir(FIXES_DIR)

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-arduinoststm32-maple")
assert os.path.isdir(FRAMEWORK_DIR)

dtostrf_src = os.path.join(FIXES_DIR, "dtostrf.c")
dtostrf_dst = os.path.join(FRAMEWORK_DIR, "STM32F1", "cores", "maple", "avr", "dtostrf.c")
assert os.path.isfile(dtostrf_src) and os.path.isfile(dtostrf_dst)

if os.stat(dtostrf_src).st_size != os.stat(dtostrf_dst).st_size:
    shutil.copy(dtostrf_src, dtostrf_dst)
