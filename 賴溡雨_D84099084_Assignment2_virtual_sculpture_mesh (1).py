import math
import random
import compas
import compas.geometry as cg
from compas.geometry import Box, Polyhedron
from compas.geometry import Translation
from compas_cgal.subdivision import catmull_clark
from compas_view2.app import App
import compas.datastructures as cd

# Input
mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

viewer = App()
for fkey in mesh.faces():
    cen = mesh.face_centroid(fkey)
    frame = cg.Frame.from_plane(mesh.face_plane(fkey))

    for i in range(64):
        r = random.uniform(0.2,0.6)
    box = cg.Box(frame, r, r, r)
    V, F = box.to_vertices_and_faces()
    VF6 = catmull_clark((V, F), 6)
    S6 = Polyhedron(*VF6)
    S6.transform(Translation.from_vector([4, 0, 0]))
    viewer.add(S6)
viewer.run()





