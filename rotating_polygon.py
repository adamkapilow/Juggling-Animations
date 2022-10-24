from manim import *
import numpy as np

Text.set_default(color=BLACK)
Arrow.set_default(color=BLACK)
NumberLine.set_default(color=BLACK)
DecimalNumber.set_default(color=BLACK)


def get_loop_angle_and_center(loop, polygon):
    start = polygon.get_vertices()[loop.throw_index]
    center_to_start = start - polygon.get_center()
    loop_center = start + (loop.radius/np.linalg.norm(center_to_start))*(center_to_start)
    start_angle = angle_of_vector(center_to_start) - PI
    return start_angle, loop_center

def loop_updater(loop, polygon):
    angle_remaining = 0.01
    start_angle, center = get_loop_angle_and_center(loop, polygon)
    new_loop = Arc(radius = loop.radius, start_angle = start_angle, angle = TAU-angle_remaining, arc_center = center)
    loop.become(new_loop)
    arrow_end = new_loop.point_from_proportion(0)
    arrow_start = new_loop.point_from_proportion(.9)
    loop.arrow.put_start_and_end_on(arrow_start, arrow_end)

def arc_updater(arc, polygon):
    start = polygon.get_vertices()[arc.throw_index]
    end = polygon.get_vertices()[arc.catch_index]
    arc.become(CurvedArrow(start, end, angle=-TAU/4))


def rotation_scene(scene : Scene, N : int, polygon_radius=1.5, label_values = None, fixed_labels=True, draw_arcs=False, loop_radius=0.5):
    if label_values == None:
        label_values = list(range(N))
    vertices = []
    for i in range(N):
        angle = np.pi/2 - 2*i*np.pi/N
        vertices.append(polygon_radius*np.array([np.cos(angle), np.sin(angle), 0]))
    scene.polygon = Polygon(*vertices)
    scene.add(scene.polygon)
    def get_moving_position(i):
        shift_dir = scene.polygon.get_vertices()[i] - scene.polygon.get_center()
        moving_position = scene.polygon.get_center() + 1.3*shift_dir
        return moving_position
    def label_updater(label):
        label.move_to(get_moving_position(label.index))

    scene.moving_labels = []
    if fixed_labels:
        scene.fixed_labels = []
    if draw_arcs:
        arcs = []
        for i in range(N):
            throw_index = i
            catch_index = (i + label_values[i]) % N
            if throw_index != catch_index:
                arc = CurvedArrow(LEFT, RIGHT)
                arc.throw_index = throw_index
                arc.catch_index = catch_index
                arc_updater(arc, scene.polygon)
                arc.add_updater(lambda arc: arc_updater(arc, scene.polygon))
                arcs.append(arc)
                scene.add(arc)
            else:
                loop = Arc()
                loop.throw_index = i
                loop.catch_index = i
                loop.radius = loop_radius
                loop.arrow = Arrow()
                loop_updater(loop, scene.polygon)
                loop.add_updater(lambda loop: loop_updater(loop, scene.polygon))
                arcs.append(arc)
                scene.add(loop)
                scene.add(loop.arrow)
        scene.arcs = arcs
    for i in range(N):
        moving_label = Text(str(label_values[i]))
        moving_label.index = i
        moving_label.add_updater(label_updater)
        label_updater(moving_label)
        scene.moving_labels.append(moving_label)
        scene.add(moving_label)
        if fixed_labels:
            shift_dir = scene.polygon.get_vertices()[i] - scene.polygon.get_center()
            label_position = scene.polygon.get_center() + 2*shift_dir
            fixed_label = Text(str(i), color=ORANGE).move_to(label_position)
            scene.fixed_labels.append(fixed_label)
            scene.add(fixed_label)
            
def draw_siteswap(scene, throw_heights, polygon_radius=1.5, loop_radius=0.5):
    rotation_scene(scene, len(throw_heights), polygon_radius=polygon_radius, 
                   label_values=throw_heights, fixed_labels=False, 
                   draw_arcs=True, loop_radius=0.5)


class fivethreeone(Scene):
    def construct(self):
        draw_siteswap(self, [5, 3, 1])
        self.play(Rotate(self.polygon))

class rotation_twelve_once(Scene):
    def construct(self):
       self.camera.background_color=WHITE
       rotation_scene(self, 12)
       self.play(Rotate(self.polygon, -2*np.pi/12, run_time=3))
       self.wait(5)


        
class rotation_twelve_four(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        rotation_scene(self, 12)
        self.play(Rotate(self.polygon, -4*2*np.pi/12, run_time=3))
        self.wait(5)

class rotation_twelve_back(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        radius = 1.5
        rotation_scene(self, 12, polygon_radius=radius)
        self.play(Rotate(self.polygon, 4*np.pi/12, run_time=3))
        self.wait(3)

class rotation_twelve_twelve(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        rotation_scene(self, 12)
        rotation_tracker = Text("Rotating 1 turn").align_on_border(UP + LEFT)
        self.add(rotation_tracker)
        for i in range(12):
            turn_text = "Rotating " + str(i + 1) + " turn"
            if i != 0:
                turn_text += "s"
            rotation_tracker.become(Text(turn_text), match_center=True)
            self.play(Rotate(self.polygon, -2*PI/12))
            self.wait(0.5)
        self.wait(3)

class tick_map(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        rotation_scene(self, 12)
        end = self.fixed_labels[5].get_center()
        start = self.polygon.get_vertices()[0]
        moving_arrow = Arrow(ORIGIN, start)
        self.add(moving_arrow)
        fixed_arrow = Arrow(end + end/2, end, color=ORANGE)
        self.add(fixed_arrow)
        anim_list = []
        anim_list.append(Rotate(moving_arrow, -5*TAU/12, about_point=ORIGIN))
        anim_list.append(Rotate(self.polygon, -5*TAU/12))
        self.wait(0.5)
        animations = AnimationGroup(*anim_list, lag_ratio=0, run_time=4)
        self.play(animations)
        self.wait(4)


        

class slide_and_rotate(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        radius=1
        rotation_scene(self, 12, polygon_radius=radius)
        for mobject in self.mobjects:
            mobject.shift(1.7*DOWN)
        line = NumberLine(x_range=[-6,18], include_numbers=True, font_size=40, decimal_number_config={"color":BLACK, "num_decimal_places":0})
        line.align_on_border(UP).shift(DOWN*0.5)
        line2 = line.copy().next_to(line, DOWN)
        line2.set_color(ORANGE)
        self.add(line2)
        self.add(line)
        time = ValueTracker(0)
        self.polygon.angle = time.get_value()
        line.position = time.get_value()
        line_start = line.n2p(0)
        line_end = line2.n2p(4)
        line_moving_arrow = Arrow(line_start + UP*1.5, line_start)
        line_fixed_arrow = Arrow(line_end + 2*DOWN, line_end+ 0.5*DOWN, color=ORANGE)
        self.add(line_fixed_arrow)
        self.add(line_moving_arrow)
        polygon_end = self.fixed_labels[4].get_center()
        shift_dir = polygon_end - self.polygon.get_center()
        polygon_fixed_arrow =Arrow(self.polygon.get_center() + 1.6*shift_dir, polygon_end, color=ORANGE)
        polygon_start = self.polygon.get_vertices()[0]
        polygon_moving_arrow = Arrow(self.polygon.get_center(), polygon_start)
        self.add(polygon_fixed_arrow)
        self.add(polygon_moving_arrow)
        def line_updater(mobject : Mobject):
            mobject.shift((time.get_value() - mobject.position)*RIGHT)
            line_moving_arrow.shift((time.get_value() - mobject.position)*RIGHT)
            mobject.position = time.get_value()
        def polygon_updater(mobject : Mobject):
            mobject.rotate((time.get_value() - mobject.angle)*(-TAU/12))
            polygon_moving_arrow.rotate((time.get_value() - mobject.angle)*(-TAU/12), about_point=mobject.get_center())
            mobject.angle = time.get_value()
        line.add_updater(line_updater)
        self.polygon.add_updater(polygon_updater)
        self.wait()
        self.play(time.animate.set_value(4), run_time=4)
        self.wait(4)

class homomorphism(Scene):
    def construct(self):
        Text.set_default(color=WHITE)
        Arrow.set_default(color=WHITE)
        radius=0.9
        rotation_scene(self, 12, polygon_radius=radius)
        for mobject in self.mobjects:
            mobject.shift(1.8*DOWN)
        line = NumberLine(x_range=[-6,18], include_numbers=True, color=WHITE)
        line.align_on_border(UP).shift(DOWN*0.5)
        line2 = line.copy().next_to(line, DOWN)
        line2.set_color(ORANGE)
        moving_arrow = Arrow(line.n2p(0)+2*UP, line.n2p(0))
        self.add(moving_arrow)
        arrow3 = Arrow(line2.n2p(3)+2*DOWN, line2.n2p(3)+0.5*DOWN, color=ORANGE)
        arrow5 = Arrow(line2.n2p(5)+2*DOWN, line2.n2p(5)+0.5*DOWN, color=ORANGE)
        self.add(line2)
        self.add(line)
        self.add(arrow3)
        self.add(arrow5)
        time = ValueTracker(0)
        self.polygon.angle = time.get_value()
        line.position = time.get_value()
        moving_arrow.position = time.get_value()
        def line_updater(mobject : Mobject):
            mobject.shift((time.get_value() - mobject.position)*RIGHT)
            mobject.position = time.get_value()
        def polygon_updater(mobject : Mobject):
            mobject.rotate((time.get_value() - mobject.angle)*(-TAU/12))
            mobject.angle = time.get_value()
        line.add_updater(line_updater)
        moving_arrow.add_updater(line_updater)
        self.polygon.add_updater(polygon_updater)
        self.play(time.animate.set_value(3), run_time=3)
        self.wait(2)
        self.play(time.animate.set_value(5), run_time=3)
        self.wait(6)
        
class slide(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        line = NumberLine(x_range=[-12,12], include_numbers=True, font_size=75)
        line2 = NumberLine(x_range=[-8,8], include_numbers=True, font_size=75)
        line.shift(0.8*UP)
        line2.shift(0.8*DOWN)
        line2.set_color(ORANGE)
        end = line2.n2p(3)
        self.add(line)
        self.add(line2)
        start = line.n2p(0)
        moving_arrow = Arrow(start + 3*UP, start + UP*0.5)
        arrow = Arrow(end+3*DOWN, end + DOWN*0.8, color=ORANGE)
        self.add(arrow)
        self.add(moving_arrow)

        line_shift = line.animate.shift(3*RIGHT)
        arrow_shift = moving_arrow.animate.shift(3*RIGHT)
        anims = AnimationGroup(line_shift, arrow_shift, lag_ratio=0, run_time=3)
        self.wait()
        self.play(anims)
        self.wait(6)

class sixfourfiveone(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        draw_siteswap(self, [6, 4, 5, 1], polygon_radius=2.3)
        self.wait()
        self.play(Rotate(self.polygon, -3*TAU/4, OUT, self.polygon.get_center()), run_time=3)
        self.wait(6)

config.background_color = BLACK