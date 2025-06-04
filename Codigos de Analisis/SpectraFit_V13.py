#Python_3
# LIBRERÍAS
import FitFunctions as Fit
from pylab import *
import spec_analysis_V13 as dic
import numpy as np
import scipy.signal as ss
from scipy.optimize import curve_fit
##############################################################################
#rootdir = 'C:\\Users\\Maui\\Documents\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\AnalisisLimpieza\\j6j\\'
#rootdir = 'C:\\Users\\Maui\\Documents\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\Si&W\\kb5\\'
#rootdir = 'C:\\Users\\Maui\Documents\\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\TiN\\90W_20%\\jb7\\'
#rootdir = r'F:\DatosEspectroscopicos_proc\Pulsada\2021-10\LAI-2'
rootdir = r'G:\.shortcut-targets-by-id\1Yo0DnMNtDsUYI8mAj-M23-B9YD1leayY\Plasmonitor\DatosEspectroscopicos\LB3'
#rootdir = r'E:\L96\Sputter'


folder = r'\UV_proc'
#folder = 'VIS_proc\'
#folder = 'har_proc\'

fname = r'\1704146U2_cat'  #Espectrometro UV
#fname = '1704147U2_cat'  #Espectrometro VIS
#fname= 'har_TiO2_01_W_cat_tcalib' #Thorlabs
#fname = '1906286U2_cat'  #Espectrometro UV_ NewSpectrometer
#fname = '1906287U2_cat'

spec = 2   # 2 =  Espect UV; 3 = Espect. VIS

print (rootdir+fname)
espectro = np.loadtxt(rootdir+folder+fname+'.dat')
#################################################################################
intens_index = arange(1,shape(espectro)[1])

#Spectral lines set:

#species = ['TiI','ArII','ArI','N2','N2plus']
#species = ['TiI','TiII','ArII','ArI','N2','N2plus'] #Analisis Pulsada
#species = ['SiI','ArII','ArI','N2','N2plus','OI']
species = ['SiI','N2plus']
#species = ['TiI','ArII','ArI']


regiones, peaks = dic.Spectrometer(spec,species)


#wlen_r = (regiones['TiI'],regiones['ArII'], regiones['ArI'],regiones['N2'],regiones['N2plus'])#, regiones['N2plus'])
#wlen_r = (regiones['TiI'],regiones['TiII'],regiones['ArII'], regiones['ArI'],regiones['N2'],regiones['N2plus'])# Analisis Pulsada
#wlen_r = (regiones['SiI'],regiones['ArII'], regiones['ArI'],regiones['N2'],regiones['N2plus'],regiones['OI'])#, regiones['N2plus'])
wlen_r = (regiones['SiI'],regiones['N2plus'])
#wlen_r = (regiones['TiI'],regiones['ArII'], regiones['ArI'])

#wlen_peaks_r = (peaks['TiI'],peaks['ArII'], peaks['ArI'],peaks['N2'],peaks['N2plus'])#, peaks['N2plus'])
#wlen_peaks_r = (peaks['TiI'],peaks['TiII'],peaks['ArII'], peaks['ArI'],peaks['N2'],peaks['N2plus'])# Analisis Pulsada
#wlen_peaks_r = (peaks['SiI'],peaks['ArII'], peaks['ArI'],peaks['N2'],peaks['N2plus'],peaks['OI'])
wlen_peaks_r = (peaks['SiI'],peaks['N2plus'])
#wlen_peaks_r = (peaks['TiI'],peaks['ArII'], peaks['ArI'])

peak_number = []
wlen_column = []
#peak_region = len(wlen_peaks_r)
####################################################################################
for i in arange(0,len(wlen_peaks_r)):
	for j in arange(0,len(wlen_peaks_r[i])):
		peak_index = len(wlen_peaks_r[i][j])
		#print peak_index
		peak_number.append(peak_index)
		peak_column = wlen_peaks_r[i][j]
		for h in arange(0,len(wlen_peaks_r[i][j])):
			wlen_column.append(peak_column[h])
peak_number = np.sum(peak_number, axis = 0)

all_peaks = np.zeros((4*peak_number, len(intens_index)+1))
all_err = np.zeros((3*peak_number, len(intens_index)+1))

#### RUIDO ####

# Se obtiene la desviacion estandar del promedio de una zona del espectro que con seguridad
# no contenga lineas espectrales.
# Ambos espectrometros muestran que los ultimos 40 pixeles no contienen lineas.

for k in intens_index:
	print(k)
	wlen = espectro[:,0]
	# intensidad = espectro[:,k]
	intensidad_raw = espectro[:,k]
	if spec == 2:
		window = [1,200]
	elif spec == 3:
		window = [1897,1922]
	elif  spec ==1:
		window = [3515,3630]
	intensidad = dic.baseline(intensidad_raw,window)
	if fname == '1906286U2_cat':
		calib_data = dic.calibraUV(wlen,intensidad)
		#print(calib_data)
		intensidad = calib_data[1]
		wlen = calib_data[0]
		# print(calib_data)
	if fname == '1906287U2_cat':
		calib_data = dic.calibraVIS(wlen,intensidad)
		#print(calib_data)
		intensidad = calib_data[1]
		wlen = calib_data[0]
		#print(calib_data)
	#ruido = np.std(intensidad[xi_baseline:xf_baseline])*3
#### AJUSTE DE MULTIPLES PICOS ####
	peaks_c = []   # vector con los centros de los picos
	err_c = []
	peaks_I = []   # vector con las intensidades
	err_I = []
	peaks_w = []   # vector con los anchos
	err_w = []
	peaks_A = []   # vector con las áreas
# Secuencia de ajuste de cada pico para cada espectro
	for j in range(0,len(wlen_r)):
		for i in range(0,len(wlen_r[j])):
			width_peaks = []
			intens_peaks_r=[]
			peaks_param = []
			l1 = where(wlen > wlen_r[j][i][0])[0][0]   # selecciona los indices correspondientes a cada rango
			l2 = where(wlen < wlen_r[j][i][1])[-1][-1] # de longitudes de onda
			index_r = np.arange(l1,l2,1)
			x = np.linspace(wlen_r[j][i][0]-3,wlen_r[j][i][1]+3,500)
			for n in range(0,len(wlen_peaks_r[j][i])):
				width_peaks.append(0.2)
				intens_peaks_r.append(max(intensidad[index_r]))
#Parametros iniciales, obtenidos mediante el espectro
			peaks_param = concatenate((array(wlen_peaks_r[j][i]),array(intens_peaks_r),array(width_peaks)), axis =0)
			peaks_param = list(peaks_param)
			#print(peaks_param)
#Gaussianas iniciales obtenidas con los parametros iniciales
			first_gauss = Fit.Gaussians(x, peaks_param)
#Ajuste de las N gaussianes
			try:
				popt, pcov = curve_fit(Fit.N_Gaussians, wlen[index_r],intensidad[index_r],p0 = peaks_param)
			except:
				popt = np.zeros(len(peaks_param))
				pcov = np.eye((len(peaks_param)))#,len(peaks_param)))
				wrong_fit = 'wrong fit in file ' + str(k) + ' at peak ' + str(peaks_param[0])
				print(wrong_fit)
				pass
			try:
				err_fit = np.sqrt(np.diag(pcov))
			except:
				exc_err = 'invalid value in err_fit '+ str(k) + ' at peak ' + str(peaks_param[0])
				print(exc_err)
				pass
#Gaussianas ajustadas obtenidas con los parametros ajustados
			fit_gauss = Fit.Gaussians(x,popt)
#Cálculo de área bajo la curva
			area_fit = []
			for i in range(0,len(fit_gauss[0])):
				area_fit.append(trapz(fit_gauss[0][i],x))
# Recuperacion de parametros ajustados. Guardar informacion
			h = int(len(popt)/3)
			for i in range(0,h):
				peaks_c.append(popt[i])      # Centro del pico
				err_c.append(err_fit[i])
			#
				peaks_I.append(popt[i+h])    # Intensidad
				err_I.append(err_fit[i+h])
			#
				peaks_w.append(abs(popt[i+2*h]))  # Ancho del pico
				err_w.append(err_fit[i+2*h])
			#
				peaks_A.append(area_fit[i])  # Area del pico
# Manda a cero los valores en los que no hay picos verdaderos. Ej. O I en Si3N4 y viceversa
	for n in range(0,len(peaks_c)):
		if peaks_w[n] > 5 or peaks_I[n] < 0 :   # Si no hay pico real o no lo ajusta correctamente,
			peaks_c[n] = 0                      # la gaussiana ajustada sera muy ancha
			peaks_A[n] = 0
			peaks_I[n] = 0
			peaks_w[n] = 0
	c = array(peaks_c)
	c_err = array(err_c)
	I = array(peaks_I)
	I_err = array(err_I)
	w = array(peaks_w)
	w_err = array(err_w)
	A = array(peaks_A)
	all_peaks[:,k] = np.hstack((c,I,w,A))
	all_err[:,k]  = np.hstack((c_err,I_err,w_err))
######################################################################################
first_column = array(wlen_column*4)
all_peaks[:,0] = first_column
savefname = rootdir + folder + fname + '_peaks.dat'
saveferr = rootdir+ folder+fname + '_peaks_err.dat'
savetxt(savefname,all_peaks)
savetxt(saveferr,all_err)
##
