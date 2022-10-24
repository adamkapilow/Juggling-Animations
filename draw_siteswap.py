from manim import *
from manim.mobject.geometry.tips import ArrowTriangleTip, ArrowTriangleFilledTip    


def draw_siteswap(scene : Scene, throw_heights, radius=2):
    loop_radius = 0.05
    N = len(throw_heights)
    vertices = []
    labels = []
    for i in range(N):
        new_angle = np.pi/2 - i*TAU/N
        vertex = radius*np.array([np.cos(new_angle), np.sin(new_angle), 0])
        vertices.append(vertex)
        label_position = vertex + (0.4)*(1/radius)*vertex
        label = Text(str(throw_heights[i])).move_to(label_position)
        labels.append(label)
    scene.polygon = Polygon(*vertices)
    scene.labels = labels
    arcs = []
    for i in range(N):
        start = vertices[i]
        catch_index = (i + throw_heights[i]) % N
        end = vertices[catch_index]
        if i == catch_index:
            loop_center = start + (loop_radius/np.linalg.norm(start))*start
            start_angle = angle_of_vector(start)
            arc = Arc(radius=loop_radius, 
                      start_angle = start_angle-PI,
                      angle = -TAU + 0.5,
                      arc_center=loop_center,
                      color=PINK)
            arc.add_tip(ArrowTriangleFilledTip(color=PINK))
            arc.throw_index = i
            arc.catch_index = i
        else:
            arc = CurvedArrow(start, end, angle=-TAU/4, color=PINK)
            arc.throw_index = i
            arc.catch_index = catch_index
        arcs.append(arc)
        scene.polygon.add(arc)
    scene.arcs = arcs

class fivethreeone(Scene):
    def construct(self):
        draw_siteswap(self, [5, 3, 1], radius=3)
        self.add(self.polygon)
        for label in self.labels:
            self.add(label)
        self.play(Rotate(self.polygon, TAU/3, about_point=ORIGIN))
        


class sixfourfiveone(Scene):
    def construct(self):
        draw_siteswap(self, [6, 4, 5, 1], radius=3)
        self.add(self.polygon)
        for arc in self.arcs:
            self.add(arc)
        for label in self.labels:
            self.add(label)