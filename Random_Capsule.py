import math
import random
import compas
import compas.geometry as cg
from compas_view2.app import App


def rw(current_coor, previous_radius):

    # Probability to steer the steps
    steer_prob = random.random()
    acceleration = [0, 0, 0]
    if steer_prob < 0.99:
        acceleration[0] = random.gauss(10, 0.7)
        acceleration[1] = random.gauss(0, 0.7)
        acceleration[2] = random.gauss(0, 0.7)
    elif steer_prob < 0.99:
        acceleration[0] = random.gauss(0, 0.7)
        acceleration[1] = random.gauss(10, 0.7)
        acceleration[2] = random.gauss(0, 0.7)
    elif steer_prob < 0.98:
        acceleration[0] = random.gauss(0, 0.7)
        acceleration[1] = random.gauss(0, 0.7)
        acceleration[2] = random.gauss(5, 0.1)
    else:
        acceleration[0] = random.gauss(7, 0.01)
        acceleration[1] = random.gauss(7, 0.01)
        acceleration[2] = random.gauss(0.7, 0.01)
        

    direction = cg.Vector(*acceleration)
    direction.unitize()

    # probability to influence the density of the
    # spheres according to height values
    # -> Determine the step size
    height = current_coor[2]
    step_size = abs(random.gauss(height * 0.9, 0.1))
    direction.scale(step_size)
    new_coor = current_coor.transformed(cg.Translation.from_vector(direction))

    line = cg.Line(new_coor,[3, 3, 3])
    # Determine its radius
    radius = abs(step_size - previous_radius)
    
    # Draw the capsule
    capsule = cg.Capsule(line, radius)
    return capsule, new_coor, radius


previous_radius = 0.01
current_coor = cg.Point(0, 0, 0)
geometries = []
for i in range(100):
    capsule, current_coor, previous_radius = rw(
        current_coor, previous_radius)
    geometries.append(capsule)

if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
