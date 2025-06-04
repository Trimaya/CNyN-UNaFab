#Python_3
# -*- coding: utf-8 -*-
#####Librerias
import spec_analysis_V13 as dic
from matplotlib import *
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.pylab import *
from numpy import *
import FitFunctions as Fit
###################################################################################################

#rootdir = 'C:\\Users\\Maui\\Documents\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\AnalisisLimpieza\\j6j\\'
#rootdir = 'C:\\Users\\Maui\\Documents\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\Si&W\\kb5\\'
#rootdir = 'C:\\Users\\Maui\Documents\\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\TiN\\90W_20%\\jb7\\'
#rootdir = r'F:\DatosEspectroscopicos_proc\Pulsada\2021-10\LAI-2'
rootdir = r'G:\.shortcut-targets-by-id\1Yo0DnMNtDsUYI8mAj-M23-B9YD1leayY\Plasmonitor\DatosEspectroscopicos\LB3'
#rootdir = r'E:\L96\Sputter'


folder = r'\UV_proc'
#folder = 'VIS_proc\'
#folder = 'har_proc\'

fname = r'\1704146U2_cat_peaks.dat'  #Espectrometro UV
#fname = r'\1704147U2_cat_peaks.dat'  #Espectrometro VIS
#fname= 'har_TiO2_01_W_cat_tcalib' #Thorlabs
#fname = '1906286U2_cat'  #Espectrometro UV_ NewSpectrometer
#fname = '1906287U2_cat'


spec = 2   # 2 =  Espect UV; 3 = Espect. VIS
root = rootdir+folder
datos_peaks = np.loadtxt(rootdir+folder+fname)
Pnumber = int(len(datos_peaks)/4) #Numero de picos
#################################################################################################

#species = ['TiI','ArII','ArI','N2','N2plus']
#species = ['TiI','TiII','ArII','ArI','N2','N2plus'] #Analisis Pulsada
#species = ['SiI','ArII','ArI','N2','N2plus','OI']
species = ['SiI','N2plus']
#species = ['TiI','ArII','ArI']

#################################################################################################
regiones, peaks = dic.Spectrometer(spec,species)
picos, wlen, intens, width, area = dic.separa(root,fname,Pnumber)

#####Corrector de datos #######
#Verificar el indice de picos, para determinar el indice de area a corregir
datos = [wlen, intens, width, area]
title_param = ['Center','Maxima','Width', 'Area']

print(picos)
########   G R A F I C A S ###############
# x_data = arange(len(wlen[0]))
# for k in arange(0,len(datos)):
    # for i in range(0,len(especies)):
        # especie = especies[i]
        # elemento = peaks[especie]
        # y_data, picos_element = spec_analysis_V13.elementos(elemento,datos[k],picos)
        # lgd = picos_element
        # tit = title_param[k]
        # for j in range(0,len(y_data)):
            # figure(k)
            # plt.plot(x_data,y_data[j][0], label = str(lgd[j]))
            # plt.title(tit)
            # plt.xlabel('File number')

            # plt.legend()
            # plt.show()
# index = 2
# ArII_C = area[index]
# ArII_C = spec_analysis_V13.corrector(ArII_C)
# for i in range(0,len(area[index])):
    # area[index][i] = ArII_C[i]
# Suavizado de datos ######
# Area_smooth = []
# for i in range(0,len(especies)):
    # especie = especies[i]
    # elemento = peaks[especie]
    # datos = area
    # window_size, poly_order = 9, 3
    # y_data, picos_element = spec_analysis_V13.elementos(elemento,datos,picos)
    # lgd = picos_element
	# for j in range(0, len(y_data)):


        # y_smooth = savgol_filter(y_data[j][0], window_size, poly_order, mode ='mirror')
        # Area_smooth.append(y_smooth)


        # figure(k+1)
        # plt.plot(x_data,y_smooth, label = str(lgd[j]))
        # plt.title(tit)
        # plt.xlabel('File number')

        # plt.legend()
        # plt.show()


##### Cálculo de Cocientes ########

# Ratios_all = []
# Ratios_smooth = []
# RatiosName_all = []
# datos = area

# for i in range(0,len(especies)):

    # especie1 = especies[i]
   # print especie1
    # elemento1 = peaks[especie1]
    # print elemento1
    # for j in range(i,len(especies)):
        # especie2 = especies[j]
       # print especie2
        # elemento2 = peaks[especie2]
       # print elemento2

        # if especie1 == especie2:
            # pass
        # else:

            # R, Cociente = spec_analysis_V13.cocientes(elemento1,elemento2,datos,x_data,picos)
           # print R




            # for k in range(0, len(Cociente)):


                # C_smooth = savgol_filter(Cociente[k], window_size,
                                         # poly_order, mode ='mirror')
                # Rname = R[k]
                # print Rname

                # RatiosName_all.append(Rname)

                # Ratios_smooth.append(C_smooth)
                # Ratios_all.append(Cociente[k])

                  # Graficas Ratios

               # lgd = R[k]
               # tit = especie1 + 'Ratios'
               # v = [0, max(x_data), 0, 100]


               # figure(5+i)
               # plt.plot(x_data,C_smooth, label = lgd)
               # plt.title(tit)
               # plt.xlabel('File number')

               # plt.legend()
               # plt.axis(v)
               # plt.show()



# Ratios_smooth.insert(0,RatiosName_all)
# Area_smooth.insert(0,picos)

sname = fname.rstrip('.dat')
# saveratios = rootdir + carpeta + sname  + '_S-ratios'+'.dat'
# saveareas = rootdir + carpeta + sname  + '_S-areas'+'.dat'
# #savenames = rootdir + carpeta + sname  + '_RatiosName'+'.dat'

# savetxt(saveratios,transpose(Ratios_smooth))
# savetxt(saveareas,transpose(Area_smooth))
#savetxt(savenames,transpose(RatiosName_all))

savetxt(root + sname+'_Areas.dat',transpose(area))
# savetxt(root + sname+'_Ratios.dat',Ratios_all)
