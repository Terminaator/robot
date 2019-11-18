from paul.ai import AI
from paul.vision import Vision

vision = Vision()
ai = AI()

ai.start()
vision.start()
ai.join()
vision.join()

