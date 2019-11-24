from ai import ai
from vision import vision

from mainboard import mainboard

mainboard.start()
ai.start()
vision.start()

mainboard.join()
ai.join()
vision.join()

