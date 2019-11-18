from vision import Vision
from ai import AI


vision = Vision()
ai = AI()

vision.start()
ai.start()
vision.join()
ai.join()

