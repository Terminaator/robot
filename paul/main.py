from ai import ai
from vision import vision

from mainboard import mainboard

mainboard.start()
vision.start()
ai.start()

vision.join()
mainboard.join()
ai.join()

