# This code is generated by Dr. Manish Kumar with the collaboration of Dr. Enrico Salvati and Dr. Roberto Alessi.
# Contact email: Manish Kumar <mkumar2@me.iitr.ac.in>, Enrico Salvati <enrico.salvati@uniud.it>, Group website https://simed.uniud.it/
# This code is to model Cornelissen softening using CZ-PFM for the 3-point bend specimen. The mesh is generated in the code. 
# The material is assumed as linear isotropic elastic. The spectral strain decomposition is considered in this case.
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
from numpy.linalg import eig
from dolfin import *
from numpy import array
import time

# to record the computation time
comp_start = time.time()

#Compiler parameter
parameters["form_compiler"]["cpp_optimize"] = True
ffc_options = {"optimize": True, \
               "eliminate_zeros": True, \
               "precompute_basis_const": True, \
               "precompute_ip_const": True}

# Define Material Properties
E = 20000.                                        # Young's Modulus
nu = 0.2                                          # Poisson ratio
mu    = E/(2.0*(1.0 + nu))                        # lame's constant 
lmbda = (E * nu)/((1.0 - 2.0*nu)*(1.0 + nu))      # lame's constant

# Define the data for the phase field
ell = 2.5                              # characteristic length

Gc = 0.113                            # critical fracture energy
c_w = pi                              # scaling parameter of dissipation energy 
                                          # c_w = 2.0 for AT2 model
                                          # c_w = 8./3. for AT1 model
                                          # c_w = pi for CZ-PFM model
thickness = 100.                      # Thickness of the specimen    
# Mesh Data
mesh = Mesh('3_pt_bend.xml')      # import mesh as .xml
ndim = mesh.topology().dim()          # find dimensions of mesh
num_elem = mesh.num_cells()           # Calculate the number of elements in the mesh 
numnode = mesh.num_vertices()         # Calculate the number of nodes in the mesh
#print(num_elem)                      # To print number of elements
#plot(mesh)                                     # To plot the mesh
#plt.show()                                      # To show the mesh plot


# identify the domain to record force
remain = CompiledSubDomain("x[1] >= 103.0-tol and x[0] >= 224.7-tol and x[0] <= 225.3+tol ",tol = 1E-14)                # here it is the bottom edge of the specimen   
boundaries = MeshFunction("size_t", mesh,mesh.topology().dim()-1)
boundaries.set_all(0)
remain.mark(boundaries, 1)                       #  mark remain as 1
ds = Measure("ds",subdomain_data=boundaries)     


# Create function space for displacement and phase
V_u = VectorFunctionSpace(mesh, 'CG', 1)           # for displacement field
V_alpha = FunctionSpace(mesh, 'CG', 1)              # for phase field


# Define the function, test and trial fields
u, du, v = Function(V_u), TrialFunction(V_u), TestFunction(V_u)                             # Functions, Trial Functions and Test functions for displacement field
alpha, dalpha, beta = Function(V_alpha), TrialFunction(V_alpha), TestFunction(V_alpha)      # Functions, Trial Functions and Test functions for phase field
u.rename('displacement','displacement')
alpha.rename('damage','damage')

# Identify the boundaries to apply boundary conditions
tol = 1E-5
tol_v = 1e-20

# Bottom point on left side to fix
def boundary_D_l(x, on_boundary):
    return x[0] >= 49.0 - tol and x[0] <= 51.0 - tol and x[1] <= 0.0 + tol

# Bottom point on right side to apply boundary condition
def boundary_D_r(x, on_boundary):
    return x[0] >= 399.0 - tol and x[0] <= 401.0 - tol and x[1] <= 0.0 + tol

# Location to apply displacement
def boundary_D_t(x, on_boundary):
    return x[1] >= 103.0-tol and x[0] >= 224.9-tol and x[0] <= 225.1+tol 
        
bcl = DirichletBC(V_u, Constant((0.0 ,0.0)), boundary_D_l, method='pointwise')               # define boundary condition

bcr = DirichletBC(V_u.sub(1), Constant(0.0), boundary_D_r, method='pointwise')               # define boundary condition

# define functions
# Positive part of the decomposed strain
def eps_positive(u):    
    A = sym(grad(u))
    a = A[0,0]
    b = A[0,1]
    c = A[1,0]
    d = A[1,1]
    eig_1 = ((tr(A) + sqrt(tr(A)**2-4*det(A) + tol_v))/2)
    eig_2 = ((tr(A) - sqrt(tr(A)**2-4*det(A) + tol_v))/2)
    phi_1 = (eig_1 - b - d)/(a + c - eig_1)
    phi_2 = (eig_2 - b - d)/(a + c - eig_2)

    eig_v_1 = [phi_1/sqrt(phi_1**2 + 1), 1/sqrt(phi_1**2 + 1)]
    eig_v_2 = [phi_2/sqrt(phi_2**2 + 1), 1/sqrt(phi_2**2 + 1)]

    # Positive Strain Tensor
    sn_P = 0.5*(eig_1 + abs(eig_1))*np.outer(eig_v_1,eig_v_1) + 0.5*(eig_2 + abs(eig_2))*np.outer(eig_v_2,eig_v_2)
    sn_1 = as_matrix(sn_P.tolist())
    return sn_1

# Negative part of the decomposed strain
def eps_negative(u):    
    A = sym(grad(u))
    a = A[0,0]
    b = A[0,1]
    c = A[1,0]
    d = A[1,1]
    eig_1 = ((tr(A) + sqrt(tr(A)**2-4*det(A) + tol_v))/2)
    eig_2 = ((tr(A) - sqrt(tr(A)**2-4*det(A) + tol_v))/2)
    phi_1 = (eig_1 - b - d)/(a + c - eig_1)
    phi_2 = (eig_2 - b - d)/(a + c - eig_2)

    eig_v_1 = [phi_1/sqrt(phi_1**2 + 1)+tol_v, 1/sqrt(phi_1**2 + 1)]
    eig_v_2 = [phi_2/sqrt(phi_2**2 + 1)+tol_v, 1/sqrt(phi_2**2 + 1)]

         
    # Negative Strain Tensor
    sn_N = 0.5*(eig_1 - abs(eig_1))*np.outer(eig_v_1,eig_v_1) + 0.5*(eig_2 - abs(eig_2))*np.outer(eig_v_2,eig_v_2)
    sn_1 = as_matrix(sn_N.tolist())
    return sn_1

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
    #a_1 = Constant(255.3/pi)
    #a_2 = -0.5
    #a_3 = 0.
    # for Cornelissen
    a_1 = Constant(628.7/pi)
    a_2 = 1.3868
    a_3 = 0.6567
    Q_d = a_1*alpha + a_1*a_2*alpha**2 + a_1*a_2*a_3*alpha**3
    return ((1-alpha)**2)/((1-alpha)**2 + Q_d) +k_ell
    # to model AT2 or AT1
    # return (1-alpha)**2) +k_ell

def eps(u):
    """Strain tensor as a function of the displacement"""
    return sym(grad(u))

def sigma_0(u):
    """Stress tensor of the undamaged material as a function of the displacement"""
    return 2.0*mu*(eps(u)) + lmbda*tr(eps(u))*Identity(ndim)

def sigma(u,alpha):
    """Stress tensor of the damaged material as a function of the displacement and the phase field"""
    return (a(alpha))*sigma_0(u)
    

# Apply the limit on the phase field
initial_alpha=Constant(0)                         # define initial lower limit
lb = interpolate(initial_alpha, V_alpha)          # Apply lower limit
ub = interpolate(Constant("1."), V_alpha)         # Apply upper limit

elastic_energy_1 = 0.5*lmbda*(0.5*(tr(eps(u)) + abs(tr(eps(u)))))**2 + mu*tr(eps_positive(u)*eps_positive(u))           # Positive part of strain energy
elastic_energy_2 = 0.5*lmbda*(0.5*(tr(eps(u)) - abs(tr(eps(u)))))**2 + mu*tr(eps_negative(u)*eps_negative(u))            # Positive part of strain energy
elastic_energy = ((a(alpha))*elastic_energy_1 + elastic_energy_2)*thickness*dx                                           # strain energy
dissipated_energy = Gc/float(c_w)*(w(alpha)/ell + ell*dot(grad(alpha), grad(alpha)))*thickness*dx                        # Dissipation Energy
total_energy = elastic_energy + dissipated_energy                                                                       # total energy

# First and second directional derivative wrt displacement field
E_u = derivative(total_energy,u,v)
Jd = derivative(E_u, u, du)

# First and second directional derivative wrt phase field
E_alpha = derivative(total_energy,alpha,beta)
E_alpha_alpha = derivative(E_alpha,alpha,dalpha)

# define loading steps
num_steps = 1413                     # total number of load steps
num_of_large_load_step = 3           # number of large load steps
total_disp = -1.0                    # total applied displacement


u_R = Expression(('disp_A + disp_app*(n+1-B)'),disp_A = 0.0, disp_app = total_disp/(num_of_large_load_step +47), n=0., B=0., degree=0)         # Define loading as an expression so that it can be updated for next step
bct = DirichletBC(V_u.sub(1), u_R, boundary_D_t, method='pointwise')                  # define boundary condition
bc_disp = [bcl, bcr, bct]                                                             # Apply boundary conditions

# Define class and solver parameters for the displacement field
problem_u = NonlinearVariationalProblem(E_u, u, bc_disp, Jd)
solver_u = NonlinearVariationalSolver(problem_u)
prm = solver_u.parameters

prm["newton_solver"]["relative_tolerance"] = 5E-1
prm["newton_solver"]["absolute_tolerance"] = 5E-3
prm["newton_solver"]["convergence_criterion"] = "residual"
prm["newton_solver"]["error_on_nonconvergence"] = True
prm["newton_solver"]["linear_solver"] = 'mumps'
prm["newton_solver"]["lu_solver"]["symmetric"] = False 
prm["newton_solver"]["maximum_iterations"] = 5000
prm["newton_solver"]["relaxation_parameter"] = 1.0

prm["newton_solver"]["krylov_solver"]["nonzero_initial_guess"] = True 

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
solver_alpha_tao.parameters.update({"method": "tron","linear_solver" : "umfpack","preconditioner" : "petsc_amg",
                                    "line_search": "gpcg", "report": False, "maximum_iterations": 10000, "gradient_absolute_tol": 5.0e-04, "gradient_relative_tol": 5.0e-04})


# Boundary conditions for phase field
def boundary_D_d_c(x, on_boundary):
     return x[1] >= 103.0-tol and x[0] >= 222.4-tol and x[0] <= 227.6+tol 

bc = DirichletBC(V_alpha, Constant(0.0), boundary_D_d_c,method='pointwise')        # define boundary condition
bc.apply(lb.vector())                                  # Apply boundary condition on lower limit
bc.apply(ub.vector())                                  # Apply boundary condition on upper limit

def boundary_D_d_c(x, on_boundary):
     return x[1] <= 0.0+tol and x[0] >= 49.-tol and x[0] <= 51.+tol 

bc = DirichletBC(V_alpha, Constant(0.0), boundary_D_d_c,method='pointwise')        # define boundary condition
bc.apply(lb.vector())                                  # Apply boundary condition on lower limit
bc.apply(ub.vector())                                  # Apply boundary condition on upper limit

def boundary_D_d_c(x, on_boundary):
     return x[1] <= 0.0+tol and x[0] >= 399.-tol and x[0] <= 401.+tol 

bc = DirichletBC(V_alpha, Constant(0.0), boundary_D_d_c,method='pointwise')        # define boundary condition
bc.apply(lb.vector())                                  # Apply boundary condition on lower limit
bc.apply(ub.vector())                                  # Apply boundary condition on upper limit

# Function to define the staggered solving procedure                               
def alternate_minimization(u,alpha,tol=5.e-4,maxiter=10000,alpha_0=interpolate(Constant("0.0"), V_alpha)):
    # initialization
    iter = 1; err_alpha = 1
    alpha_error = Function(V_alpha)
    # iteration loop
    while err_alpha>tol and iter<maxiter:
        # solve elastic problem
        print('Solution for displacement')
        solver_u.solve()

        print('Solution for phase field')

        # solve phase field problem
        solver_alpha_tao.solve(DamageProblem(), alpha.vector(), lb.vector(), ub.vector())# test error
        alpha_error.vector()[:] = alpha.vector() - alpha_0.vector()
        err_alpha = np.linalg.norm(alpha_error.vector().get_local(), ord = np.Inf) 
        # update iteration
        print("Iteration:  %2d, Error: %2.8g, alpha_max: %.8g" %(iter, err_alpha, alpha.vector().max()))
        alpha_0.assign(alpha)
        iter=iter+1
    print("Iteration:  %2d, Error: %2.8g, alpha_max: %.8g" %(iter-1, err_alpha, alpha.vector().max()))
    return (err_alpha, iter)
    
savedir = "results/"                           # directory to export files
if os.path.isdir(savedir):
    shutil.rmtree(savedir)
file_alpha = File(savedir+"/alpha.pvd")        # define file name for phase field files
file_u = File(savedir+"/u.pvd")                # define file name for displacement field files

# initialization of vectors to store force and displacement
forces = np.zeros((num_steps+1, 2))

def postprocessing():
    forces[n+1] = np.array([-u(225.,103.)[1],-assemble(sigma(u,alpha)[1,1]*thickness*ds(1))])
    # Dump solution to file
    file_alpha << (alpha,n)                            # Phase field
    file_u << (u,n)                                    # Displacement field
    np.savetxt(savedir+'/forces.txt', forces)          # record force displacement data
        
# Execution of the loading steps
for n in range(num_steps):
    if n > num_of_large_load_step-1:                # To switch from large steps to small steps
        u_R.disp_A = total_disp/(num_of_large_load_step+47)*num_of_large_load_step
        u_R.disp_app = -0.94/1410
        u_R.B = num_of_large_load_step
    u_R.n = n
    # solve alternate minimization
    alternate_minimization(u,alpha,maxiter=20000)                   # call solver function

    postprocessing()                                                # call postprocessing function
    print("\nEnd of timestep %d with load %g"%(n, u(225.,103.)[1])) # print completion of load step in terminal
    print("-----------------------------------------")

    lb.vector()[:] = alpha.vector()                               # updating the lower bound to account for the irreversibility

# Print time is taken to complete the simulation 
    
comp_end = time.time()
print(f"Runtime of the program is {comp_end - comp_start} sec")






