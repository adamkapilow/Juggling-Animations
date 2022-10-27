from unicodedata import decimal
from manim import *
import numpy as np

"""
Returns a pair of NumberLines depicting two jugglers juggling the same pattern in sync,
in addition to a specified collection of throws to alter into a prechac pattern.
Inputs:
scene - A Scene object to render to
throw_heights - list of periodic throw heights in the pattern
endpoints - list of integers of length 2, start and end beats of diagram
prechac_positions - list of positions mod the period to turn into passes
show_hands -- boolean, whether the hands are labeled or not
line_spacing -- How far apart are the lines from each other vertically
Returns:
lines -- A list of NumberLine objects containing throws and throw height labels of the jugglign patterns
selves_to_change -- A list of selves as CurvedArrows to change into passes
"""
def siteswap_line(scene, throw_heights, endpoints, prechac_positions=[], show_hands=True, line_spacing=12):
    N = len(throw_heights)
    top_line = NumberLine(x_range = [endpoints[0], endpoints[1]], tick_size=0.2)
    top_line.position = 0
    bottom_line = NumberLine(x_range = [endpoints[0], endpoints[1]], tick_size=0.2)
    bottom_line.position = 0
    lines = VGroup(top_line, bottom_line).arrange(line_spacing*DOWN)
    for k in range(2):
        label_dict = {}
        for i in range(endpoints[0], endpoints[1] + 1):
            label_dict[i] = DecimalNumber(throw_heights[i%N], 0, edge_to_fix=ORIGIN)
        if k == 0:
            top_line.add_labels(label_dict, direction=UP, font_size=70)
        else:
            bottom_line.add_labels(label_dict, direction=DOWN, font_size=70)
    if show_hands:
        hand_values = ["R", "L"]
        for i in range(2):
            for j in range(endpoints[0], endpoints[1] + 1):
                label = lines[i].labels[j - endpoints[0]]
                if i == 0:
                    hand = Text(hand_values[j % 2]).next_to(label, UP)
                    lines[0].add(hand)
                else:
                    hand = Text(hand_values[j % 2]).next_to(label, DOWN)
                    lines[1].add(hand)
    selves_to_change = [[], []]
    for i in range(endpoints[0], endpoints[1] + 1):
        throw = throw_heights[i % N]
        catch = i + throw
        bottom_arrow = CurvedArrow(bottom_line.n2p(i), bottom_line.n2p(catch), angle=-PI/1.5)
        top_arrow = CurvedArrow(top_line.n2p(i), top_line.n2p(catch), angle=PI/1.5)
        bottom_arrow.throw_pos = i
        bottom_arrow.catch_pos = catch
        top_arrow.throw_pos = i
        top_arrow.catch_pos = catch
        if i % N in prechac_positions:
            selves_to_change[0].append(top_arrow)
            selves_to_change[1].append(bottom_arrow)
        else:
            top_line.add(top_arrow)
            bottom_line.add(bottom_arrow)

    
    return lines, selves_to_change
    
"""
Performs an animation turning a collection of selves into passes, and generates the corresponding updaters to use for Prechac-like Transformations.
Inputs:
scene - A Scene object to render to
throw_heights - list of periodic throw heights in the pattern
endpoints - list of length 2, start and end of diagram
prechac_positions - list of positions mod the period to turn into passes
lines - list of 
Returns:
global_position -- ValueTracker which when modified appropriately translates one of the siteswap lines and the self throws, stretching the passes.
period_tracker -- ValueTracker which when modified translates the endpoints of the passes only. In a Prechac transformation they are translated by the period, the length of throw_heights.
"""
def build_updaters(scene, throw_heights, prechac_positions, endpoints, lines, selves_to_change):
    N = len(throw_heights)
    passes = [[], []]
    top_line = lines[0]
    bottom_line = lines[1]
    scene.add(lines)
    for i in range(2):
        for throw in selves_to_change[i]:
            scene.add(throw)
    period_shifting_line = 1
    global_position = ValueTracker(0)
    period_tracker = ValueTracker(0)
    def pass_updater(arrow : Arrow):
        if arrow.throw_line == period_shifting_line:
            period_multiplier = 1
        else:
            period_multiplier = 0
        updated_catch = arrow.catch_pos + period_multiplier*period_tracker.get_value()
        arrow.put_start_and_end_on(lines[arrow.throw_line].n2p(arrow.throw_pos), 
                                    lines[arrow.catch_line].n2p(updated_catch))

    pass_colors = [BLUE, ORANGE]
    for i in range(2):
        for throw in selves_to_change[i]:
            new_pass = Arrow(lines.submobjects[i].n2p(throw.throw_pos), 
                                lines.submobjects[1 - i].n2p(throw.catch_pos), color=pass_colors[i])
            new_pass.throw_pos = throw.throw_pos
            new_pass.catch_pos = throw.catch_pos
            new_pass.throw_line = i
            new_pass.catch_line = 1-i
            new_pass.add_updater(pass_updater)
            passes[i].append(new_pass)
    
    
    def translation_updater(mob):
        mob.shift((global_position.get_value() - mob.position)*RIGHT)
        mob.position = global_position.get_value()

    self_to_pass_transforms = []
    for i in range(2):
        for j in range(len(passes[i])):
            self_to_pass_transforms.append(Transform(selves_to_change[i][j], passes[i][j], 
                                            replace_mobject_with_target_in_scene=True))
        
    scene.wait(2)
    for i in range(2):
        for j in range(endpoints[0], endpoints[1] + 1):
            if j % N in prechac_positions:
                lines[i].labels[j - endpoints[0]].set(color=pass_colors[i])
    self_to_pass_animations = AnimationGroup(*self_to_pass_transforms, run_time=3)
    scene.play(self_to_pass_animations)
    scene.wait(2)

    def label_updater(mob : DecimalNumber, base_throw, sign, period_multiplier):
        mob.set_value(base_throw + sign*(global_position.get_value()) + period_multiplier*period_tracker.get_value())

    
    for i in range(2):
        for j in range(endpoints[0], endpoints[1] + 1):
            if (j % N) in prechac_positions:
                label = lines[i].labels[j - endpoints[0]]
                label.set(num_decimal_places=1)
                base_throw = throw_heights[j%N]
                if i == 0:
                    label.add_updater(lambda mob : label_updater(mob, base_throw, -1, 0))
                else:
                    label.add_updater(lambda mob : label_updater(mob, base_throw, 1, 1))
    
    lines[0].add_updater(translation_updater)
    return global_position, period_tracker

"""
A scene that uses the preceding methods to explore Prechac-like transformations on an even period patten, 5313.
"""
class even_prechac_anim(Scene):
    def construct(self):
        throw_heights = [5, 3, 1, 3]
        N = len(throw_heights)
        prechac_positions = [0]
        endpoints = [-10, 10]
        lines, selves_to_change = siteswap_line(self, throw_heights, endpoints, prechac_positions)
        global_position, period_tracker = build_updaters(self, throw_heights, prechac_positions, endpoints, lines, selves_to_change)

        self.play(global_position.animate.set_value(N/2 - 1), run_time=3)
        self.wait(2)
        self.play(global_position.animate.set_value(N/2 + 1), run_time=3)
        self.wait(2)
        self.play(period_tracker.animate.set_value(-N), run_time = 3)
        self.wait(2)
        anims = []
        anims.append(period_tracker.animate.set_value(0))
        anims.append(global_position.animate.set_value(0))
        anim_group = AnimationGroup(*anims, run_time=3)
        self.play(anim_group)
        self.wait(3)
        self.play(global_position.animate.set_value(N/2), run_time=3)
        self.wait(2)
        self.play(period_tracker.animate.set_value(-N), run_time = 3)
        self.wait(2)
        
"""
A Scene that uses the previous methods to animate the Prechac transformation on an odd period pattern, 423. 
"""
class odd_prechac_anim(Scene):
    def construct(self):
        throw_heights = [4, 2, 3]
        N = len(throw_heights)
        prechac_positions = [0]
        endpoints = [-12, 10]
        lines, selves_to_change = siteswap_line(self, throw_heights, endpoints, prechac_positions)
        global_position, period_tracker = build_updaters(self, throw_heights, prechac_positions, endpoints, lines, selves_to_change)

        self.play(global_position.animate.set_value(N/2), run_time=3)
        self.wait(2)
        self.play(period_tracker.animate.set_value(-N), run_time = 3)
        self.wait(3)