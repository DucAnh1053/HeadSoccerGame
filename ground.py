import pymunk
import pymunk.pygame_util
from settings import WIDTH, HEIGHT


class Ground():
    def __init__(self, space):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (WIDTH/2, HEIGHT - 80)
        shape = pymunk.Poly.create_box(body, (WIDTH, 160))
        shape.elasticity = 0.7
        shape.friction = 0.65
        space.add(body, shape)
        self.body = body
        self.shape = shape
