from manim import *
import numpy as np

def TwoD_throw_func(P, Q):
    return bezier(np.array([P, (P + Q)/2 + np.linalg.norm(Q-P)*np.array([0,0,1]), Q]))

throw_heights = np.array([[[0, 1], [1, 1], [3, 0]], [[4, 0], [2, 1], [2, 1]]])

class TwoDimsiteSwap(ThreeDScene):
    def construct(self):
        throws = []
        for i in range(np.shape(throw_heights)[0]):
            for j in range(np.shape(throw_heights)[1]):
                start = np.array([j, i, 0])
                end = start + np.array([throw_heights[i][j][0], throw_heights[i][j][1]])
                throws.append(ParametricFunction(TwoD_throw_func(start, end), t_range=[0,1]))
        for throw in throws:
            self.add(throw)