from ai import ai
from vision import vision

from mainboard import mainboard

vision.start()
mainboard.start()
ai.start()

vision.join()
mainboard.join()
ai.join()

