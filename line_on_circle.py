from manim import *

from draw_siteswap import draw_siteswap

class line_on_circle(Scene):
    def construct(self):
        Radius = 3.5
        circle = Circle(Radius).set_color(WHITE)
        angle = ValueTracker(0)
        throw_heights = [8,6,4,6,1]
        N = len(throw_heights)
        '''tick_points = []
        for i in range(N):
            new_angle = np.pi/2 - i * TAU/N
            tick_points.append(Radius*np.array([np.cos(new_angle), np.sin(new_angle), 0]))
        self.add(Polygon(*tick_points))'''
        def point_updater(mobject):
            epsilon = 0.2
            new_center = [Radius*np.cos(angle.get_value()), Radius*np.sin(angle.get_value()), 0]
            mobject.move_to(new_center)
            angle_to_tick = -angle.get_value()*N/TAU + N/4
            if np.abs(angle_to_tick - np.round(angle_to_tick)) < epsilon:
                mobject.set_color(RED)
            else:
                mobject.set_color(BLUE)
        P = Circle(0.5, fill_opacity=1)
        P.add_updater(point_updater)
        line = Line()
        line.add_updater(lambda mobject: mobject.put_start_and_end_on(ORIGIN, P.get_center()))
        self.add(P)
        self.add(line)
        '''def mover(mobject, dt):
            mobject.increment_value(dt)
        angle.add_updater(mover)'''
        self.play(Create(circle))
        draw_siteswap(self, throw_heights, radius=Radius)
        self.add(self.polygon)
        for arc in self.arcs:
            self.add(arc)
        self.play(angle.animate.set_value(-2*TAU), run_time=10, rate_func=linear)
        self.wait(4)
