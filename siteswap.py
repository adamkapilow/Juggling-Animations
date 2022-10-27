from manim import *
import numpy as np

"""
This file contains methods around building an animation showing that a 
juggling pattern of period N can be visualized on an N hour polygonal clock.
"""

"""
A parametrization for a cylinder of radius 1.
"""
def cylinderParam(u, v):
    return cylindrical_to_cartesian(1, u, v)

"""
Takes in a points cylindrical coordinates, and outputs its
Cartesian coordinates as a numpy array.
"""
def cylindrical_to_cartesian(r, u, v):
    return np.array([r*np.cos(u), r*np.sin(u), v])

"""
Takes in a point's Cartesian coordinates, and outputs its cyclindrical coordinates
as a numpy array. We choose a singularity along the negative y axis. 
"""
def cartesian_to_cylindrical(x, y, z):
    if(x > 0):
        u = np.arctan(y/x)
    elif (x < 0):
        u = np.arctan(y/x) + np.pi
    elif y > 0:
        u = np.pi/2
    else:
        u = 0
    #u = angle_of_vector(np.array([x,y,z]))
    r = np.sqrt(x**2 + y**2)
    return np.array([r, u, z])

"""
A homomotopy visualizing the map (x, y, z) --> (1+y)e^{-2*pi*ix} where horizontal lines wrap around a circle of radius 1 + the y value. 
Inputs:
x, y, z, t - floats indicating the spatial and temporal coordinates of the homotopy
Axes -- optional Axes object. If supplied the homotopy will be performed in its coordinates.
"""
def wrap_homotopy(x : float, y : float, z : float, t : float, Axes=None):
    if Axes != None:
        axes_coordinates = Axes.p2c(np.array([x,y,z]))
        cylindrical_start = cartesian_to_cylindrical(*axes_coordinates, 0)
        cylindrical_end = np.array([1 + axes_coordinates[1], 
                                    -2*np.pi*axes_coordinates[0]/3 + 2*np.pi/3, 
                                    0])
        array_homotopy = cylindrical_to_cartesian(*((1-t)*cylindrical_start + t*cylindrical_end))
        array_homotopy = Axes.c2p(array_homotopy[0], array_homotopy[1])
        return tuple(array_homotopy)
    else:
        cylindrical_start = cartesian_to_cylindrical(x, y, z)
        cylindrical_end = np.array([1 +y, -2*np.pi*x/3 + 2*np.pi/3, 0])
        array_homotopy = cylindrical_to_cartesian(*((1-t)*cylindrical_start + t*cylindrical_end))
        return tuple(array_homotopy)

"""
Returns a quadratic Bezier curve connecting two points on the x-axis of a given 
Axes object. 
"""
def throw_func(i, j, axes):
    midpoint = axes.c2p((i + j)/2, (j - i))
    return bezier(np.array([axes.c2p(i, 0), midpoint, axes.c2p(j, 0)]))
    #return lambda t: np.array([t, -(1/3)*(t-P[0])*(t-Q[0]), 0])


#An animation that applies a given homotopy to the center of a mobject,
#changing its position but not its shape or size.
class center_only_homotopy(Animation):
    def __init__(self, mobject, homotopy=None, **kwargs):
        self.homotopy = homotopy
        self.start = mobject.get_center()
        super().__init__(mobject, **kwargs)
    def function_at_time_t(self, t: float):
        return lambda p : self.homotopy(*p,t)
    def interpolate_mobject(self, alpha: float):
        t = self.rate_func(alpha)
        self.mobject.move_to(self.function_at_time_t(t)(self.start))


"""
A Scene showing that a juggling pattern of period 3 can be recorded 
on a 3 hour triangular clock.
"""
class siteswap(Scene):
    def construct(self):
        config.frame_height = 12
        x_start = 1
        x_end = 9
        axes = Axes(x_range=(-2,x_end,1), axis_config={"include_numbers": True, "include_ticks":True})
        P = [1, 0]
        Q = [np.cos(TAU/3), np.sin(TAU/3)]
        R = [np.cos(-TAU/3), np.sin(-TAU/3)]
        self.add(Polygon(axes.c2p(*P), axes.c2p(*Q), axes.c2p(*R), color='#785EF0'))
        wrapping_objects = []
        center_wrapping_objects = []
        self.add(axes)
        throw_heights = [5, 3, 1]
        colors = ['#648FFF', '#DC267F', '#FFB000']
        for i in range(1, x_end+1):
            color = colors[i%3]
            throw_height = throw_heights[(i - 1) % 3]
            throw = ParametricFunction(throw_func(i, i + throw_height, axes), t_range=[0, 1], color=color)
            wrapping_objects.append(throw)
            dot = Dot(color=color).move_to(axes.c2p(i, 0))
            square = Square(0.5, color=color).move_to(axes.c2p(i + throw_height, 0))
            center_wrapping_objects.append(dot)
            center_wrapping_objects.append(square)
        homotopies = []
        for ob in wrapping_objects:
            self.add(ob)
            homotopies.append(Homotopy(mobject=ob, homotopy= lambda x, y, z, t : wrap_homotopy(x,y,z,t, Axes=axes), rate_func=smooth, run_time=8))
        for ob in center_wrapping_objects:
            self.add(ob)
            homotopies.append(center_only_homotopy(ob, homotopy= lambda x, y, z, t : wrap_homotopy(x,y,z,t, Axes=axes), rate_func=smooth, run_time=8))
        grp = AnimationGroup(*homotopies, lag_ratio=0)
        self.wait(3)
        self.play(grp)
        self.wait()