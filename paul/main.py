from ai import ai
from vision import vision

from mainboard import mainboard

ai.start()
vision.start()
mainboard.start()
ai.join()
vision.join()
mainboard.join()