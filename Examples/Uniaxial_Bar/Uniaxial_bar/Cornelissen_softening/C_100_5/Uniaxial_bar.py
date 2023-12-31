# This code is generated by Dr. Manish Kumar with the collaboration of Dr. Enrico Salvati and Dr. Roberto Alessi.
# Contact email: Manish Kumar <mkumar2@me.iitr.ac.in>, Enrico Salvati <enrico.salvati@uniud.it>, Group website https://simed.uniud.it/
# This code is to model linear softening using CZ-PFM for the uniaxial bar. The mesh is generated in the code. 
# The material is assumed as linear isotropic elastic. No strain decomposition is considered in this case.
# To convert this code for other models (AT1, AT2, different softening), the required info is provided in the code at the appropriate places. 
# Displacement and phase fields are exported as .pvd for post-processing. Force and displacement data are exported into a text file.
# Copyright (C) <2023>  <Manish Kumar>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
 
# All the required libraries are imported into the code
from fenics import *               # FEniCS library
from mshr import *
import matplotlib.pyplot as plt    # Plotting Library
from ufl import nabla_div
import numpy as np
from ufl import replace
import sys, os, shutil, math

# Define Material Properties
E = 30000.0                           # Young's Modulus
nu = 0.2                              # Poisson ratio
lmbda = (E*nu)/((1+nu)*(1-2*nu))      # lame's constant 
mu = E/(2*(1+nu))                     # lame's constant

# Define the data for the phase field
ell = 5.                              # characteristic length

Gc = 0.12                             # critical fracture energy
c_w = pi                              # scaling parameter of dissipation energy 
                                          # c_w = 2.0 for AT2 model
                                          # c_w = 8./3. for AT1 model
                                          # c_w = pi for CZ-PFM model

# Mesh Data
length = 200.                                    # length of specimen
num_elem = 4000                                   # number of elements in specimen
mesh = IntervalMesh(num_elem,0., length)         # 1D mesh generator
num_elem = mesh.num_cells()                      # Calculate number of elements in mesh
print('\n','Number of element =', num_elem)      # To print number of elements
#plot(mesh)                                      # To plot the mesh
#plt.show()                                      # To show the mesh plot

# identify the domain to record force
remain = CompiledSubDomain("x[0] >= 200 - tol",tol = 1E-14)                # here it is the right end of the bar    
boundaries = MeshFunction("size_t", mesh,mesh.topology().dim()-1)         
boundaries.set_all(0)
remain.mark(boundaries, 1)                                                 #  mark remain as 1
ds = Measure("ds",subdomain_data=boundaries)                               

# Create function space for displacement and phase
V_u = FunctionSpace(mesh, 'Lagrange', 1)                  # for displacement field
V_alpha = FunctionSpace(mesh, 'Lagrange', 1)              # for phase field

# Define the function, test and trial fields
u, du, v = Function(V_u), TrialFunction(V_u), TestFunction(V_u)                             # Functions, Trial Functions and Test functions for displacement field
alpha, dalpha, beta = Function(V_alpha), TrialFunction(V_alpha), TestFunction(V_alpha)      # Functions, Trial Functions and Test functions for phase field
u.rename('displacement','displacement')
alpha.rename('damage','damage')

# Identify the boundaries to apply boundary conditions
left =  CompiledSubDomain("near(x[0], side) && on_boundary", side = 0.0)               # Left edge to fix
right =  CompiledSubDomain("near(x[0], side) && on_boundary", side = length)           # Right edge to apply displacement

bcl = DirichletBC(V_u, Constant(0.0), left)                                           # define boundary condition


# define functions
def w(alpha):
    """Dissipated energy functional as a function of the phase field """
    # to model softening    
    return 2*alpha - alpha**2
    # to model AT2    
    #return alpha**2
    # to model AT1    
    #return alpha

def a(alpha):
    """Stiffness modulation as a function of the phase field """
    k_ell = Constant(1.e-6)                                        #  residual stiffness
    # to model softening 
    # for Linear
    #a_1 = Constant(320./pi)
    #a_2 = -0.5
    #a_3 = 0.
    # for Cornelissen
    a_1 = Constant(320./pi)
    a_2 = 1.3868
    a_3 = 0.6567
    Q_d = a_1*alpha + a_1*a_2*alpha**2 + a_1*a_2*a_3*alpha**3
    return ((1-alpha)**2)/((1-alpha)**2 + Q_d) +k_ell
    # to model AT2 or AT1
    # return (1-alpha)**2) +k_ell
    

def eps(u):
    """Strain tensor as a function of the displacement"""
    return grad(u)

def sigma_0(u):
    """Stress tensor of the undamaged material as a function of the displacement"""
    mu    = E / (2.0*(1.0 + nu))
    lmbda = (E * nu) / ((1.0 - 2.0*nu)*(1.0 + nu))
    return E*(eps(u))

def sigma(u,alpha):
    """Stress tensor of the damaged material as a function of the displacement and the phase field"""
    return (a(alpha))*sigma_0(u)

# Apply the limit on the phase field
initial_alpha=Constant(0)                         # define initial lower limit
lb = interpolate(initial_alpha, V_alpha)          # Apply lower limit
ub = interpolate(Constant("1."), V_alpha)         # Apply upper limit

# Governing Equations
elastic_energy = 0.5*inner(sigma(u,alpha), eps(u))*dx                                             # Strain Energy
dissipated_energy = Gc/float(c_w)*(w(alpha)/ell + ell*dot(grad(alpha), grad(alpha)))*dx           # Dissipation Energy
total_energy = elastic_energy + dissipated_energy                                                 # Total energy

# First directional derivative wrt displacement field
E_u = derivative(total_energy,u,v)
Jd = derivative(E_u, u, du) 

# First and second directional derivative wrt phase field
E_alpha = derivative(total_energy,alpha,beta)
E_alpha_alpha = derivative(E_alpha,alpha,dalpha)

# define loading steps
num_steps = 90
disp_app = 0.216/num_steps

u_R = Expression(('disp_app*(n+1)'),disp_app = disp_app, n=0., degree=0)          # Define loading as expression so that it can be updated for next step
bcr = DirichletBC(V_u, u_R, right)                                                # define boundary condition
bc_disp = [bcl, bcr]                                                              # Apply boundary conditions

# Define solver parameters for the displacement field
problem_u = NonlinearVariationalProblem(E_u, u, bc_disp, Jd)
solver_u = NonlinearVariationalSolver(problem_u)
prm = solver_u.parameters
prm["newton_solver"]["relative_tolerance"] = 1E-5
prm["newton_solver"]["absolute_tolerance"] = 1E-5
prm["newton_solver"]["linear_solver"] = 'mumps'

# Define class and solver parameters for the phase field
class DamageProblem(OptimisationProblem):

    def f(self, x):
        """Function to be minimized"""
        alpha.vector()[:] = x
        return assemble(total_energy)

    def F(self, b, x):
        """Gradient (first derivative)"""
        alpha.vector()[:] = x
        assemble(E_alpha, b)

    def J(self, A, x):
        """Hessian (second derivative)"""
        alpha.vector()[:] = x
        assemble(E_alpha_alpha, A)


solver_alpha_tao = PETScTAOSolver()
solver_alpha_tao.parameters.update({"method": "tron","linear_solver" : "umfpack",
                                    "line_search": "gpcg", "report": False, "maximum_iterations": 1000, "gradient_absolute_tol": 1.0e-07, "gradient_relative_tol": 1.0e-07})

# Boundary conditions for phase field
bc = DirichletBC(V_alpha, Constant(0.0), left)         # define boundary condition
bc.apply(lb.vector())                                  # Apply boundary condition on lower limit
bc.apply(ub.vector())                                  # Apply boundary condition on upper limit

bc = DirichletBC(V_alpha, Constant(0.0), right)        # define boundary condition
bc.apply(lb.vector())                                  # Apply boundary condition on lower limit
bc.apply(ub.vector())                                  # Apply boundary condition on upper limit

# Function to define the staggered solving procedure                               
def alternate_minimization(u,alpha,tol=1.e-5,maxiter=1000,alpha_0=interpolate(Constant("0.0"), V_alpha)):
    # initialization
    iter = 1; err_alpha = 1
    alpha_error = Function(V_alpha)
    # iteration loop
    while err_alpha>tol and iter<maxiter:
        # solve elastic problem
        solver_u.solve()
        # solve phase field problem

        solver_alpha_tao.solve(DamageProblem(), alpha.vector(), lb.vector(), ub.vector())# test error
        alpha_error.vector()[:] = alpha.vector() - alpha_0.vector()
        err_alpha = np.linalg.norm(alpha_error.vector().get_local(), ord = np.Inf)        
        # update iteration
        alpha_0.assign(alpha)
        iter=iter+1
    print("Iteration:  %2d, Error: %2.8g, alpha_max: %.8g" %(iter-1, err_alpha, alpha.vector().max()))
    return (err_alpha, iter)

    
savedir = "results/"                            # directory to export files
if os.path.isdir(savedir):
    shutil.rmtree(savedir)
file_alpha = File(savedir+"/alpha.pvd")         # define file name for phase field files
file_u = File(savedir+"/u.pvd")                 # define file name for displacement field files

# initialization of vectors to store force and displacement
forces = np.zeros((num_steps+1, 2))

# function for postprocessing 
def postprocessing():
    forces[n+1] = np.array([u(200),assemble(sigma(u,alpha)[0]*ds(1))])
    # Dump solution to file
    file_alpha << (alpha,n)                            # Phase field
    file_u << (u,n)                                    # Displacement field
    np.savetxt(savedir+'/forces.txt', forces)          # record force displacement data


# Execution of the loading steps
for n in range(num_steps):
    u_R.n = n                                                       # Update loading according to the load step
    # solve alternate minimization
    alternate_minimization(u,alpha,maxiter=1000)                    # call solver function
    postprocessing()                                                # call postprocessing function
    print("\nEnd of timestep %d with load %g"%(n, disp_app*(n+1)))  # print completion of load step in terminal
    print("-----------------------------------------")
    lb.vector()[:] = alpha.vector()                                 # updating the lower bound to account for the irreversibility

