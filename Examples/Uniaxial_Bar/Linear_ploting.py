# This code is generated by Dr. Manish Kumar with the collaboration of Dr. Enrico Salvati and Dr. Roberto Alessi.
# Contact email: Manish Kumar <mkumar2@me.iitr.ac.in>, Enrico Salvati <enrico.salvati@uniud.it>, Group website https://simed.uniud.it/
# This code produces the load vs displacement plot. The data is imported from the spreadsheets, and the plot is saved in .svg format.
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
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Import data from the spreadsheet
df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="E,F")                            # specify the columns
data = np.zeros((len(df)-4, 2))
sd1 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="Q,R")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd2 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AC,AD")                          # specify the columns
data = np.zeros((len(df)-4, 2))
sd3 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AO,AP")                          # specify the columns
data = np.zeros((len(df)-4, 2))
sd4 = df.values[4:, :]                                                                                        # specify the data

# Plotting
plt.figure(1)
plt.plot (sd1[:,0],sd1[:,1],color='k', linewidth=2.0, Marker='o', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_10_5')
plt.plot (sd2[:,0],sd2[:,1],color='k', linewidth=2.0, Marker='^', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_10_10')
plt.plot (sd3[:,0],sd3[:,1],color='k', linewidth=2.0, Marker='s', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_10_20')
plt.plot (sd4[:,0],sd4[:,1],color='k', linewidth=2.0, Marker='x', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_10_50')
plt.grid('on')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.title('b/h = 10')
plt.legend()
plt.xlim([0,0.121])
plt.ylim([0,3])
plt.xticks([0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.12])
plt.yticks([0., 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
plt.savefig('Linear_b_h_10.svg')
plt.show()

# Import data from the spreadsheet
df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="G,H")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd1 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="S,T")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd2 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AE,AF")                          # specify the columns 
data = np.zeros((len(df)-4, 2))
sd3 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AQ,AR")                          # specify the columns 
data = np.zeros((len(df)-4, 2))
sd4 = df.values[4:, :]                                                                                        # specify the data

# Plotting
plt.figure(1)
plt.plot (sd1[:,0],sd1[:,1],color='k', linewidth=2.0, Marker='o', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_20_5')
plt.plot (sd2[:,0],sd2[:,1],color='k', linewidth=2.0, Marker='^', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_20_10')
plt.plot (sd3[:,0],sd3[:,1],color='k', linewidth=2.0, Marker='s', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_20_20')
plt.plot (sd4[:,0],sd4[:,1],color='k', linewidth=2.0, Marker='x', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_20_50')
plt.grid('on')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.title('b/h = 20')
plt.legend()
plt.xlim([0,0.121])
plt.ylim([0,3])
plt.xticks([0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.12])
plt.yticks([0., 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
plt.savefig('Linear_b_h_20.svg')
plt.show()

# Import data from the spreadsheet
df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="I,J")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd1 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="U,V")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd2 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AG,AH")                          # specify the columns 
data = np.zeros((len(df)-4, 2))
sd3 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AS,AT")                          # specify the columns
data = np.zeros((len(df)-4, 2))
sd4 = df.values[4:, :]                                                                                        # specify the data

# Plotting
plt.figure(1)
plt.plot (sd1[:,0],sd1[:,1],color='k', linewidth=2.0, Marker='o', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_50_5')
plt.plot (sd2[:,0],sd2[:,1],color='k', linewidth=2.0, Marker='^', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_50_10')
plt.plot (sd3[:,0],sd3[:,1],color='k', linewidth=2.0, Marker='s', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_50_20')
plt.plot (sd4[:,0],sd4[:,1],color='k', linewidth=2.0, Marker='x', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_50_50')
plt.grid('on')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.title('b/h = 50')
plt.legend()
plt.xlim([0,0.121])
plt.ylim([0,3])
plt.xticks([0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.12])
plt.yticks([0., 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
plt.savefig('Linear_b_h_50.svg')
plt.show()

# Import data from the spreadsheet
df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="K,L")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd1 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="W,X")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd2 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AI,AJ")                          # specify the columns
data = np.zeros((len(df)-4, 2))
sd3 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AU,AV")                          # specify the columns 
data = np.zeros((len(df)-4, 2))
sd4 = df.values[4:, :]                                                                                        # specify the data

# Ploting
plt.figure(1)
plt.plot (sd1[:,0],sd1[:,1],color='k', linewidth=2.0, Marker='o', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_100_5')
plt.plot (sd2[:,0],sd2[:,1],color='k', linewidth=2.0, Marker='^', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_100_10')
plt.plot (sd3[:,0],sd3[:,1],color='k', linewidth=2.0, Marker='s', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_100_20')
plt.plot (sd4[:,0],sd4[:,1],color='k', linewidth=2.0, Marker='x', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_100_50')
plt.grid('on')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.title('b/h = 100')
plt.legend()
plt.xlim([0,0.121])
plt.ylim([0,3])
plt.xticks([0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.12])
plt.yticks([0., 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
plt.savefig('Linear_b_h_100.svg')
plt.show()

# Import data from the spreadsheet
df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="M,N")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd1 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="Y,Z")                            # specify the columns 
data = np.zeros((len(df)-4, 2))
sd2 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AK,AL")                          # specify the columns 
data = np.zeros((len(df)-4, 2))
sd3 = df.values[4:, :]                                                                                        # specify the data

df = pd.read_excel ('Linear_Load_disp.xlsx',sheet_name='Load_disp', usecols="AW,AX")                          # specify the columns 
data = np.zeros((len(df)-4, 2))
sd4 = df.values[4:, :]                                                                                        # specify the data

# Plotting
plt.figure(1)
plt.plot (sd1[:,0],sd1[:,1],color='k', linewidth=2.0, Marker='o', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_200_5')
plt.plot (sd2[:,0],sd2[:,1],color='k', linewidth=2.0, Marker='^', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_200_10')
plt.plot (sd3[:,0],sd3[:,1],color='k', linewidth=2.0, Marker='s', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_200_20')
plt.plot (sd4[:,0],sd4[:,1],color='k', linewidth=2.0, Marker='x', MarkerSize = 5., MarkerEdgeColor='k', MarkerFaceColor ='r', label='L_200_50')
plt.grid('on')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (N)')
plt.title('b/h = 200')
plt.legend()
plt.xlim([0,0.121])
plt.ylim([0,3])
plt.xticks([0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.12])
plt.yticks([0., 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
plt.savefig('Linear_b_h_200.svg')
plt.show()
