from manim import *
import numpy as np

def diagram(throw_heights, endpoints, throws_to_modify=[], angle=-np.pi/2):
    line = NumberLine(x_range=endpoints)
    N = len(throw_heights)
    h = max(throw_heights)
    label_dict = {}
    throws = []

    for i in range(endpoints[0], endpoints[1] + 1):
        label_dict[i] = DecimalNumber(throw_heights[i%N], 1, edge_to_fix=ORIGIN)
        catch_pos = i + throw_heights[i % N]
        throw = CurvedArrow(line.n2p(i), line.n2p(catch_pos), angle=-PI/1.2)
        throw.throw_pos = i
        throw.catch_pos = catch_pos
        line.add(throw)
        throws.append(throw)
    line.add_labels(label_dict, font_size=70)
    return line, throws
    

def swap_throw_heights(throw_heights, a, b):
    N = len(throw_heights)
    swapped_throw_heights = []
    a, b = (a % N, b % N)
    if a > b:
        a, b = (b, a)
    #Now assume a < b
    for i in range(N):
        if i == a:
            new_throw = throw_heights[b] + b - a
        elif i == b:
            new_throw = throw_heights[a] + a - b
        else:
            new_throw = throw_heights[i]
        swapped_throw_heights.append(new_throw)
    return swapped_throw_heights



class fivethreeone(Scene):
    def construct(self):
        throw_heights = [5, 3, 1]
        period_positions = [2]
        swap_positions = [0, 1]
        N = len(throw_heights)
        Angle = -PI/1.2
        endpoints = [-15, 15]
        period_tracker = ValueTracker(0)
        swap_tracker = ValueTracker(0)
        def get_throw_height(beat):
            t = swap_tracker.get_value()
            swap_modifier = (1-t)*throw_heights[beat % N] + t*swapped_throw_heights[beat % N]
            if beat % N in period_positions:
                return swap_modifier + period_tracker.get_value()
            else:
                return swap_modifier

        line, throws = diagram(throw_heights, endpoints, angle=Angle)
        self.add(line)
        for throw in throws:
            self.add(throw)
        self.play(line.animate.shift(RIGHT))
        def throw_updater(throw : CurvedArrow):
            catch_position = throw.throw_pos + get_throw_height(throw.throw_pos)
            throw.become(CurvedArrow(line.n2p(throw.throw_pos), 
                         line.n2p(catch_position), 
                         angle=Angle, 
                         color=throw.color))
        
        def label_updater(label : DecimalNumber):
            label.set_value(get_throw_height(label.position))
        for i in range(endpoints[0], endpoints[1] + 1):
            throw = throws[i - endpoints[0]]
            throw.add_updater(throw_updater)
            if i % N in period_positions or i % N in swap_positions:
                throw.set(color=ORANGE)
                label = line.labels[i - endpoints[0]]
                label.set(num_decimal_places=1, color=ORANGE)
                label.position = i
                label.add_updater(label_updater)
        self.wait()
        swapped_throw_heights = swap_throw_heights(throw_heights, 0, 1)
        #print(throw_heights)
        #print(swapped_throw_heights)
        print(get_throw_height(0))
        self.play(swap_tracker.animate.set_value(1), run_time=3)
        self.play(period_tracker.animate.set_value(3), run_time=3)
        print(get_throw_height(0))
       
        
       
        
        
            


        


class arrow_test(Scene):
    def construct(self):
        arrow = CurvedArrow(ORIGIN, 2*RIGHT)
        self.add(arrow)
        self.add(Dot(arrow.get_tip().point_from_proportion(1)))
        self.wait()
        self.play(arrow.animate.put_start_and_end_on(ORIGIN, -4*RIGHT))
        self.add(Dot(arrow.point_from_proportion(1)))
        self.wait()
