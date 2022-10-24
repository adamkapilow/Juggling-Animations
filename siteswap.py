from manim import *
import numpy as np

SCENE_HEIGHT = 8
epsilon = 10**-3

def cylinderParam(u, v):
    return cylindrical_to_cartesian(1, u, v)

def cylindrical_to_cartesian(r, u, v):
    return np.array([r*np.cos(u), r*np.sin(u), v])

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

def wrap_homotopy(x : float, y : float, z : float, t : float, Axes=None):
    #TODO: Improve performance of this, sucks to compute the arctan at all times, would be nice to just compute it once.
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

def simple_homotopy(x,y,z,t):
    end = cylindrical_to_cartesian(1, -2*np.pi*(x+1)/3, x)
    start = np.array([x,y,z])
    return tuple((1-t)*start + t*end)

def throw_func(P, Q):
    return bezier(np.array([P, (P + Q)/2 + (Q[0] - P[0])*UP, Q]))
    #return lambda t: np.array([t, -(1/3)*(t-P[0])*(t-Q[0]), 0])

def make_polygonal_prism(n, axes=None):
    #TODO: Change to also work in axes coordinates
    vertices = []
    for i in range(2*n):
        coords = cylindrical_to_cartesian(1, 2*np.pi*i/n, SCENE_HEIGHT*(i//n))
        if axes != None:
            vertices.append(axes.coords_to_point(*coords))
        else:
            vertices.append(coords)
    faces = [list(range(n)), list(range(n, 2*n))]
    for i in range(n):
        new_face = [i, i + n, n + ((i + 1) % n), (i + 1) % n,]
        faces.append(new_face)
    return Polyhedron(vertices, faces)

#An animation that applies a given homotopy to the center of a mobject
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



class siteswap(Scene):
    def construct(self):
        axes = Axes(x_range=(-6,10,1), axis_config={"include_numbers": True, "include_ticks":True})
        #prism not synced to axes
        #triangluar_prism = make_polygonal_prism(3).set_color(RED)
        #prism synced to axes
        # triangluar_prism = make_polygonal_prism(3, axes).set_color(RED)
        # self.add(triangluar_prism)
        #cylinder = Surface(cylinderParam, u_range=[0, TAU], v_range=[0,SCENE_HEIGHT])
        #self.add(cylinder)
        P = [1, 0]
        Q = [np.cos(TAU/3), np.sin(TAU/3)]
        R = [np.cos(-TAU/3), np.sin(-TAU/3)]
        self.add(Polygon(axes.c2p(*P), axes.c2p(*Q), axes.c2p(*R), color=RED))
        TickPoint = axes.coords_to_point(1, 0, 0)
        '''
        for t in np.linspace(0, 1, 10):
            space_coords = wrap_homotopy(*TickPoint, t, axes)
            axes_coords = axes.point_to_coords(space_coords)
            print(axes_coords)
        '''
        #self.set_camera_orientation(theta=0 * DEGREES, phi=15 * DEGREES, zoom=0.5)
        self.add(axes)
        throw_heights = [5, 3, 1]
        wrapping_objects = []
        center_wrapping_objects = []
        center_wrapping_objects.append(Dot(axes.c2p(1,0,0)))
        center_wrapping_objects.append(Dot(axes.c2p(4,0,0), color=PINK))
        center_wrapping_objects.append(Dot(axes.c2p(6,0,0), color=BLUE))
        #center_wrapping_objects.append(Dot(axes.c2p(-2,0,0)))
        #center_wrapping_objects.append(Dot(axes.c2p(1,0,0), color=PINK))
        #center_wrapping_objects.append(Dot(axes.c2p(3,0,0), color=BLUE))
        """ center_wrapping_objects.append(Dot([-2,0,0]))
        center_wrapping_objects.append(Dot([1,0,0], color=PINK))
        center_wrapping_objects.append(Dot([3,0,0], color=BLUE)) """
        wrapping_objects.append(ParametricFunction(throw_func(axes.c2p(1,0), axes.c2p(6, 0)), t_range=[0, 1-epsilon]))
        wrapping_objects.append(ParametricFunction(throw_func(axes.c2p(4,0), axes.c2p(9, 0)), t_range=[epsilon, 1]))
        """ line1 = ParametricFunction(lambda t: axes.c2p(t,0), t_range=[0,3], color=PINK)
        line2 = ParametricFunction(lambda t: axes.c2p(t,0), t_range=[3,5], color=BLUE)
        line3 = ParametricFunction(lambda t: axes.c2p(t,0), t_range=[3,6], color=BLUE)
        line4 = ParametricFunction(lambda t: axes.c2p(t,0), t_range=[6,8], color=PINK)
        wrapping_objects.append(line1)
        wrapping_objects.append(line2)
        wrapping_objects.append(line3)
        wrapping_objects.append(line4) """
        homotopies = []
        for ob in wrapping_objects:
            self.add(ob)
            #homotopies.append(Homotopy(mobject=ob, homotopy= lambda x, y, z, t : wrap_homotopy(x, y, z, t, axes)))
            homotopies.append(Homotopy(mobject=ob, homotopy= lambda x, y, z, t : wrap_homotopy(x,y,z,t, Axes=axes), rate_func=smooth, run_time=6))
        for ob in center_wrapping_objects:
            self.add(ob)
            homotopies.append(center_only_homotopy(ob, homotopy= lambda x, y, z, t : wrap_homotopy(x,y,z,t, Axes=axes), rate_func=smooth, run_time=6))
        grp = AnimationGroup(*homotopies, lag_ratio=0)
        self.wait(3)
        self.play(grp)
        
        #self.move_camera(phi = 0 * DEGREES, theta = -90 * DEGREES, zoom=0.65)
        #spiral = ParametricFunction(lambda x : np.array([*wrap_homotopy(x,0,0,1)]), t_range=[1,4])
        #self.add(spiral)
        self.wait()