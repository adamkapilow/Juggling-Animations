from manim import *
import numpy as np

"""
This file contains functions and scenes concering decorating
a rotating polygon with labels and arrows.
"""

#uncomment to set default colors to black, on a white background
""" 
confing.camera.background_color = WHITE
Text.set_default(color=BLACK)
Arrow.set_default(color=BLACK)
NumberLine.set_default(color=BLACK)
DecimalNumber.set_default(color=BLACK) """


"""
This function returns a loop with an arrow attached to a given vertex of a polygon.
Inputs:
throw_index -- Integer less than the number of sides in the polygon, 
               specifying which vertex to base the loop at
polygon -- a Polygon object
loop_radius -- A float specifying the radius of the loop
Returns:
VGroup of the loop, a ParametricFunction, and a Polygon acting as the triangular tip.
"""
def get_loop(throw_index, polygon, loop_radius):
    angle_remaining = 0.1*TAU
    start = polygon.get_vertices()[throw_index]
    center_to_start = start - polygon.get_center()
    center = start + (loop_radius/np.linalg.norm(center_to_start))*(center_to_start)
    start_angle = angle_of_vector(center_to_start) - PI
    end_angle = start_angle + TAU - angle_remaining
    def circle_param(t):
        return center + loop_radius*np.array([np.cos(t), np.sin(t), 0])
    loop = ParametricFunction(circle_param, t_range=[start_angle, end_angle])
    altitude = start - circle_param(end_angle)
    tip_displacement = np.array([altitude[1], -altitude[0], 0])/np.sqrt(3)
    vertex1 = circle_param(end_angle) + tip_displacement
    vertex2 = circle_param(end_angle) - tip_displacement
    tip = Polygon(start, vertex1, vertex2, fill_opacity=1, color=loop.color)
    return VGroup(loop, tip)

"""
Returns a CurvedArrow pointing between two specified vertices on a polygon.
Inputs:
throw_index -- Tail of CurvedArrow
catch_index -- Tip of CurvedArrow
polygon -- Polygon object to attach to
"""
def get_arc(throw_index, catch_index, polygon):
    start = polygon.get_vertices()[throw_index]
    end = polygon.get_vertices()[catch_index]
    arc = CurvedArrow(start, end, angle=-TAU/4)
    arc.throw_index = throw_index
    arc.catch_index = catch_index
    return CurvedArrow(start, end, angle=-TAU/4)

"""
Sets up a scene to have a polygon with prescribed labels on the vertices, with or without arcs drawn between vertices, to other specified parameters. The polygon's vertices start pointing north, increasing in index moving clockwise.
Inputs:
scene -- A Scene object to render to
N -- number of vertices for the polygon
polygon_radius -- Optional, the radius of the circumcircle for the polygon.
label_values -- Optional, a list of values for labels on the vertices of the polygon.
fixed_labels -- Optional, boolean whether to include an additional set of labels 
                which don't move with the polygon.
draw_arcs -- Optional boolean, whether to draw arcs on the polygon, only to be used when the label values are given as throw heights in a siteswap.
Returns:
Nothing, but adds attributes scene.polygon, scene.moving_labels, scene.fixed_labels, scene.arcs 
to scene, also adds all these objects to the scene, displaying them.
"""
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
        moving_position = scene.polygon.get_center() + 1.5*shift_dir
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
                arc = get_arc(throw_index, catch_index, scene.polygon)
                arcs.append(arc)
                scene.polygon.add(arc)
            else:
                loop = get_loop(i, scene.polygon, 0.5)
                scene.polygon.add(loop)
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
    scene.add(scene.polygon)

"""
A wrapped for rotation_scene, used specifically to draw a siteswap on a polygon.
Inputs:
scene -- A Scene object to render to
throw_heights -- A list of integers specifying the throw heights in a juggling pattern
polygon_radius -- Optional, radius of the circumcircle of the polygon 
                  containing the pattern diagram.
loop_radius -- Optional, radius of any loops in the siteswap diagram, 
               arrows landing on the same beat they were thrown at, corresponding to
               throw heights that are a multiple of the period.
"""
def draw_siteswap(scene, throw_heights, polygon_radius=1.5, loop_radius=0.5):
    rotation_scene(scene, len(throw_heights), polygon_radius=polygon_radius, 
                   label_values=throw_heights, fixed_labels=False, 
                   draw_arcs=True, loop_radius=0.5)


"""
A scene depicting the siteswap 531, and showing its invariance under rotation. 
"""
class fivethreeone(Scene):
    def construct(self):
        draw_siteswap(self, [5, 3, 1])
        self.play(Rotate(self.polygon))

"""
A scene that rotates a twelve hour clock one hour forward.
"""
class rotation_twelve_once(Scene):
    def construct(self):
       self.camera.background_color=WHITE
       rotation_scene(self, 12)
       self.play(Rotate(self.polygon, -2*np.pi/12, run_time=3))
       self.wait(5)


"""
A scene that rotates a twelve hour clock 4 hours forward.
"""
class rotation_twelve_four(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        rotation_scene(self, 12)
        self.play(Rotate(self.polygon, -4*2*np.pi/12, run_time=3))
        self.wait(5)

"""
A scene that rotates a twelve hour clock one hour backward.
"""
class rotation_twelve_back(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        radius = 1.5
        rotation_scene(self, 12, polygon_radius=radius)
        self.play(Rotate(self.polygon, 4*np.pi/12, run_time=3))
        self.wait(3)


"""
A scene that rotates a twelve hour clock forward twelve hours, done
one hour at a time, keeping track of the elapsed rotation.
"""
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


"""
A scene demonstrating the fact that for each tickmark T on the clock,
there is a unique rotation of the clock sending the top tickmark to T.
"""
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


        
"""
A scene demonstrating the fact that the sliding action on the number line
sending 0 to 4 corresponds to the rotating action on the clock sending time 0 to time 4.
"""
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

"""
A scene demonstrating the fact that addition on the number line corresponds to
composition of rotating actions on the clock.
"""
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

"""
A scene demonstrating the fact that for any number x on the number line,
there is a unique sliding action sending 0 to x.
"""
class slide(Scene):
    def construct(self):
        #self.camera.background_color = WHITE
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

"""
A scene depicting the siteswap 6451, showing that it is invariant under rotation.
"""
class sixfourfiveone(Scene):
    def construct(self):
        #self.camera.background_color = WHITE
        draw_siteswap(self, [6, 4, 5, 1], polygon_radius=2.3)
        self.wait()
        self.play(Rotate(self.polygon, -3*TAU/4, OUT, self.polygon.get_center()), run_time=3)
        self.wait(6)