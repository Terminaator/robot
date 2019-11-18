from ai import AI
from vision import Vision

vision = Vision()
ai = AI()

ai.start()
vision.start()
ai.join()
vision.join()

