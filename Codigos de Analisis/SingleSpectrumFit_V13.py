#Python_3
# -*- coding: utf-8 -*-
##LIBRERÍAS##
import FitFunctions as Fit
from matplotlib.pylab import *
import spec_analysis_V13 as dic
import numpy as np
from scipy.optimize import curve_fit
#############################################################################################
#Datos Iniciales
#############################################################################################
#Direccion del archivo txt
#rootdir = 'C:\\Users\\Maui\\Documents\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\AnalisisLimpieza\\j6j\\'
#rootdir = 'C:\\Users\\Maui\\Documents\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\Si&W\\kb5\\'
#rootdir = 'C:\\Users\\Maui\Documents\\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\TiN\\90W_20%\\jb7\\'
rootdir = r'G:\.shortcut-targets-by-id\1Yo0DnMNtDsUYI8mAj-M23-B9YD1leayY\Plasmonitor\DatosEspectroscopicos\LB3'
#rootdir = r'F:\DatosEspectroscopicos_proc\Wencel\2021-09\L9K'

folder = r'\UV_proc'
#folder = 'VIS_proc\'
#folder = 'har_proc\'

fname = r'\1704146U2_cat'  #Espectrometro UV
#fname = '1704147U2_cat'  #Espectrometro VIS
#fname= 'har_TiO2_01_W_cat_tcalib' #Thorlabs
#fname = '1906286U2_cat'  #Espectrometro UV_ NewSpectrometer
#fname = '1906287U2_cat'
###############################################################################################
spec = 2   # 2 =  Espect UV; 3 = Espect. VIS
intens_index = 2750  #Numero de archivo a analizar
print(rootdir+folder+fname+'.dat')
espectro = np.loadtxt(rootdir+folder+fname+'.dat')
wlen = espectro[:,0]

#Spectral lines set:

#species = ['TiI','ArII','ArI','N2','N2plus']
species = ['TiI','TiII','ArII','ArI','N2','N2plus'] #Analisis Pulsada
#species = ['SiI','ArII','ArI','N2','N2plus','OI']
#species = ['SiI','N2plus']
#species = ['TiI','ArII','ArI']

################################################################################################
regiones, peaks = dic.Spectrometer(spec,species)

#wlen_r = (regiones['TiI'],regiones['ArII'], regiones['ArI'],regiones['N2'],regiones['N2plus'])#, regiones['N2plus'])
wlen_r = (regiones['TiI'],regiones['TiII'],regiones['ArII'], regiones['ArI'],regiones['N2'],regiones['N2plus'])# Analisis Pulsada
#wlen_r = (regiones['SiI'],regiones['ArII'], regiones['ArI'],regiones['N2'],regiones['N2plus'],regiones['OI'])#, regiones['N2plus'])
#wlen_r = (regiones['SiI'],regiones['N2plus'])
#wlen_r = (regiones['TiI'],regiones['ArII'], regiones['ArI'])

#wlen_peaks_r = (peaks['TiI'],peaks['ArII'], peaks['ArI'],peaks['N2'],peaks['N2plus'])#, peaks['N2plus'])
wlen_peaks_r = (peaks['TiI'],peaks['TiII'],peaks['ArII'], peaks['ArI'],peaks['N2'],peaks['N2plus'])# Analisis Pulsada
#wlen_peaks_r = (peaks['SiI'],peaks['ArII'], peaks['ArI'],peaks['N2'],peaks['N2plus'],peaks['OI'])
#wlen_peaks_r = (peaks['SiI'],peaks['N2plus'])
#wlen_peaks_r = (peaks['TiI'],peaks['ArII'], peaks['ArI'])

#####################################################################################################
intensidad = espectro[:,intens_index]
intensidad_raw = espectro[:,intens_index]
if spec == 2:
    window = [1,200]
elif spec == 3:
    window = [1897,1922]
elif  spec ==1:
    window = [3515,3630]
intensidad = dic.baseline(intensidad_raw,window)
if fname == r'\1906286U2_cat.dat':
    calib_data = dic.calibraUV(wlen,intensidad)
    intensidad = calib_data[1]
    wlen = calib_data[0]
    print(calib_data)    
if fname == r'\1906287U2_cat.dat':
   calib_data = dic.calibraVIS(wlen,intensidad)
   intensidad = calib_data[1]
   wlen = calib_data[0]
   print(calib_data)
    
savefname = rootdir+folder+fname + '_intensidad.dat'
all_peaks = (transpose(wlen),transpose(intensidad))
savetxt(savefname,all_peaks)


#### BASELINE #####################################################################################
#base = np.mean(intensidad_raw[baseline[0]:baseline[1]])
#intensidad = intensidad_raw - base
#### RUIDO ##########################################################################################
# Se obtiene la desviacion estandar del promedio de una zona del espectro que con seguridad 
# no contenga lineas espectrales.
# Ambos espectrometros muestran que los ultimos 40 pixeles no contienen lineas.
#ruido = np.std(intensidad[baseline[0]:baseline[1]])*3
    #ruido = np.var(intensidades_rest[3600:3640])
    #intensidad_smooth = scipy.signal.savgol_filter(intensidad, window_length = 5, polyorder=2)
#### AJUSTE DE MULTIPLES PICOS ########################################################################
peaks_c = []   # vector con los centros de los picos
err_c = []
peaks_I = []   # vector con las intensidades
err_I = []
peaks_w = []   # vector con los anchos
err_w = []
peaks_A = []   # vector con las áreas
for j in range(0,len(wlen_r)):
	for i in range(0,len(wlen_r[j])):
		width_peaks = []
		intens_peaks_r=[]
		peaks_param = []
		l1 = np.where(wlen > wlen_r[j][i][0])[0][0]   # selecciona los indices correspondientes a cada rango
		l2 = np.where(wlen < wlen_r[j][i][1])[-1][-1] # de longitudes de onda
		index_r = np.arange(l1,l2,1)
		x = np.arange(wlen_r[j][i][0]-3,wlen_r[j][i][1]+3,0.01)
		for k in range(0,len(wlen_peaks_r[j][i])):
			width_peaks.append(0.1) 
			intens_peaks_r.append(np.max(intensidad[index_r]))
		peaks_param = np.concatenate((np.array(wlen_peaks_r[j][i]),np.array(intens_peaks_r),np.array(width_peaks)), axis =0)
		peaks_param = list(peaks_param)
#Gaussianas iniciales obtenidas con los parametros iniciales    
		first_gauss = Fit.Gaussians(x, peaks_param)
#Ajuste de las N gaussianes
		try:
			popt, pcov = curve_fit(Fit.N_Gaussians, wlen[index_r],intensidad[index_r], p0 = peaks_param)
		except:
			popt = np.zeros(len(peaks_param))
			pcov = np.eye((len(peaks_param)))#,len(peaks_param)))
			wrong_fit = 'wrong fit in file ' +  ' at peak ' + str(peaks_param[0])
			pass   
		try:                
			err_fit = np.sqrt(np.diag(pcov))
		except:
			exc_err = 'invalid value in err_fit '+  ' at peak ' + str(peaks_param[0])
			print(exc_err)
			pass
		#print(popt)
		fit_gauss = Fit.Gaussians(x,popt)
#Cálculo de área bajo la curva############################################################################
		area_fit = []
		#area_peaks = []
		for k in range(0,len(fit_gauss[0])):
			area_fit.append(np.trapz(fit_gauss[0][k],x))        
	#Recuperacion de parametros ajustados. Guardar informacion
		h = int(len(popt)/3)
		for k in range(0,h):                       
			peaks_c.append(popt[k])      # Centro del pico
			err_c.append(err_fit[k])
		#
			peaks_I.append(popt[k+h])    # Intensidad
			err_I.append(err_fit[k+h])
		#
			peaks_w.append(popt[k+2*h])  # Ancho del pico
			err_w.append(err_fit[k+2*h])
		#
			peaks_A.append(area_fit[k])  # Area del pico
##Graficado de resultados##########################################################################
#        
		h1 = np.where(wlen > wlen_r[j][i][0]-5)[0][0]   # selecciona los indices correspondientes a cada rango
		h2 = np.where(wlen < wlen_r[j][i][1]+5)[-1][-1] # de longitudes de onda
		index_h = np.arange(h1,h2,1)   
	#figure(k)
		plot(wlen[index_h],intensidad[index_h],'k-o')
		plot(x,fit_gauss[1],'g')
		for k in range(0,len(wlen_peaks_r[j][i])):
			plot(x,first_gauss[0][k],'r')
			plot(x,fit_gauss[0][k],'b')
		show()
        
#    ##
#    
## Manda a cero los valores en los que no hay picos verdaderos. Ej. O I en Si3N4 y viceversa
#
#for n in range(0,len(peaks_c)):
#    if peaks_w[n] > 2:   # Si no hay pico real, la gaussiana ajustada sera muy ancha
#        peaks_c[n] = 0
#        peaks_A[n] = 0
#        peaks_I[n] = 0
#        peaks_w[n] = 0
#    #    
#    #c = np.array(peaks_c)
#    #np.array(peaks_w)
#    #np.array(peaks_I)
#    
#    
#c = array(peaks_c)
#c_err = array(err_c)
#    #c.shape = (24,1)
#    
#I = np.array(peaks_I)
#I_err = np.array(err_I)
#    #I.shape = (24,1)
#    
#w = np.array(peaks_w)
#w_err = np.array(err_w)
#    #w.shape = (24,1)
#    
#A = np.array(peaks_A)
#    #A_err = np.array(err_A)
# 