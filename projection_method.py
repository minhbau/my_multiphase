#!/usr/bin/python
from mesh import Mesh_1d,Mesh_2d
from fields import Fields_2d 
from boundary_conditions import *
from fields_2d_velocity import U,V
from initial_conditions import *
import numpy as np



#create 2d mesh
meshx = Mesh_1d(0.,4.,2,2,'mesh_x')
meshy = Mesh_1d(0.,2,0.5,0.5,'mesh_y')
meshx.plot_edgeVsIndex()
meshx.plot_centerVsIndex()
meshy.plot_edgeVsIndex()
meshy.plot_centerVsIndex()
mesh = Mesh_2d(meshx,meshy,'mesh')
print "Mesh created.\n"
print "Mesh size: (",mesh.nx,', ',mesh.ny,")"
mesh.write()

CFL = 0.8
u_inf = 1
max_iterations = 10000
#todo defined a IC function for this problem
#todo modify BC
u = U(mesh,BC_empty,IC_test_interpolation_u)
v = V(mesh,BC_empty,IC_test_interpolation_v)
p = Fields_2d(mesh,BC_fixedValue_1,IC='default')
fields_list = [u,v,p]

n_steps=10000 #Interval that u,v and p are write
Re=100.0   #Reynolds number
#nu=1e-6
mu = 1e-2
rho=1.0 
t=0.0
dt=CFL*meshx.min_delta/u_inf/Re

#write all fields into time directory
for i,item in enumerate(fields_list):
    item.write(str(t))


#write all fields into time directory
for i,item in enumerate(fields_list):
    item.write(str(t))

u_star = U(mesh)
v_star = V(mesh)

#main loop
for n in range(max_iterations):
    print "iteration: ",n,"\n"
    u_old = u
    v_old = v
    for i,item in enumerate(fields_list):
        item.applyBC()


    # Step 1: Update velocity to intermediate step
    Ax = u.uphi_x_vedge(u)+v.vphi_y_vedge(u)
    Dx = mu*(u.ddx2()+u.ddy2())
    Ay = u.uphi_x_hedge(v)+v.vphi_y_hedge(v)
    Dy = mu*(v.ddx2()+v.ddy2())
    fbx = Fields_2d(mesh,ftype='vedge')#currently its zero
    fby = Fields_2d(mesh,ftype='hedge')#currently its zero
            
    u_star = u + (dt*(-1.*Ax+fbx+1./rho*(Dx)))
    v_star = v + (dt*(-1.*Ay+fby+1./rho*(Dy)))

    # Step 2: Solve projection poisson problem
    u_star.applyBC()
    v_star.applyBC()


    break
    
            



