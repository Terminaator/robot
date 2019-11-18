from vision import Vision
from ai import AI


vision = Vision()
ai = AI()

ai.start()
vision.start()
ai.join()
vision.join()

