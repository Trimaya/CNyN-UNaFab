# -*- coding: utf-8 -*-

# LIBRERÍAS
import FitFunctions
from pylab import *
#import saomlib
import spec_analysis_V12
import numpy
import scipy.signal
from scipy.optimize import curve_fit


#rootdir = 'D:\\TrabajosCNyN\\DatosEspectroscopicos_proc\\Avantes\\i5b\\'
rootdir = 'C:\\Users\\Itayee Sierra\\Desktop\\DatosEspectroscopicos_proc\\j36\\'


carpeta = 'UV_proc\\'
#carpeta = 'i3i_proc\\'

fname = '1704146U2_cat'
#fname = 'hc5_TiO2_17_W_cat_tcalib'


espectro = loadtxt(rootdir+carpeta+fname+'.dat')
wlen = espectro[:, 0]

intens_index = 600  # Numero de archivo a analizar

spec = 2

species = ['TiI', 'N2', 'N2plus', 'ArI', 'ArII']


regiones, peaks = spec_analysis_V12.Spectrometer(spec, species)


wlen_r = (regiones['TiI'], regiones['N2'],
          regiones['N2plus'], regiones['ArI'], regiones['ArII'])
#
wlen_peaks_r = (peaks['TiI'], peaks['N2'],
                peaks['N2plus'], peaks['ArI'], peaks['ArII'])


intensidad = espectro[:, intens_index]
intensidad_raw = espectro[:, intens_index]

if spec == 2:
    window = [1, 200]
elif spec == 3:
    window = [1560, 1590]


intensidad = spec_analysis_V12.baseline(intensidad_raw, window)


savefname = rootdir+carpeta + fname + '_espectro.dat'

all_peaks = (transpose(wlen), transpose(intensidad))
savetxt(savefname, all_peaks)


#### BASELINE ####
#base = numpy.mean(intensidad_raw[baseline[0]:baseline[1]])
#intensidad = intensidad_raw - base


#### RUIDO ####

# Se obtiene la desviacion estandar del promedio de una zona del espectro que con seguridad
# no contenga lineas espectrales.
# Ambos espectrometros muestran que los ultimos 40 pixeles no contienen lineas.

#ruido = numpy.std(intensidad[baseline[0]:baseline[1]])*3
#ruido = numpy.var(intensidades_rest[3600:3640])

#intensidad_smooth = scipy.signal.savgol_filter(intensidad, window_length = 5, polyorder=2)

#### AJUSTE DE MULTIPLES PICOS ####

peaks_c = []   # vector con los centros de los picos
err_c = []

peaks_I = []   # vector con las intensidades
err_I = []

peaks_w = []   # vector con los anchos
err_w = []

peaks_A = []   # vector con las áreas


for j in range(0, len(wlen_r)):
    for i in range(0, len(wlen_r[j])):
        width_peaks = []
        intens_peaks_r = []
        peaks_param = []

        # selecciona los indices correspondientes a cada rango
        l1 = where(wlen > wlen_r[j][i][0])[0][0]
        l2 = where(wlen < wlen_r[j][i][1])[-1][-1]  # de longitudes de onda
        index_r = arange(l1, l2, 1)

        #x = linspace(wlen_r[j][0]-3,wlen_r[j][1]+3,500)
        x = arange(wlen_r[j][i][0]-3, wlen_r[j][i][1]+3, 0.01)

        for k in range(0, len(wlen_peaks_r[j][i])):

            width_peaks.append(0.1)
            intens_peaks_r.append(max(intensidad[index_r]))

        peaks_param = concatenate((array(wlen_peaks_r[j][i]), array(
            intens_peaks_r), array(width_peaks)), axis=0)

        peaks_param = list(peaks_param)
        # print(peaks_param)

# Gaussianas iniciales obtenidas con los parametros iniciales
        first_gauss = FitFunctions.Gaussians(x, peaks_param)

# Ajuste de las N gaussianes
        try:
            popt, pcov = curve_fit(FitFunctions.N_Gaussians, wlen[index_r], intensidad[index_r],
                                   p0=peaks_param)
        except:
            popt = zeros(len(peaks_param))
            pcov = eye((len(peaks_param)))  # ,len(peaks_param)))
            wrong_fit = 'wrong fit in file ' + \
                ' at peak ' + str(peaks_param[0])
            # print wrong_fit
            pass

        try:
            err_fit = sqrt(np.diag(pcov))
        except:
            exc_err = 'invalid value in err_fit ' + \
                ' at peak ' + str(peaks_param[0])
            print(exc_err)
            pass

        fit_gauss = FitFunctions.Gaussians(x, popt)
# Cálculo de área bajo la curva
        area_fit = []
   # area_peaks = []
        for k in range(0, len(fit_gauss[0])):
            area_fit.append(trapz(fit_gauss[0][k], x))
    #     area_peaks.append(trapz(first_gauss[0][i],x))

# Recuperacion de parametros ajustados. Guardar informacion
        h = len(popt) // 3
        for k in range(0, h):
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


# Graficado de resultados
#
        # selecciona los indices correspondientes a cada rango
        h1 = where(wlen > wlen_r[j][i][0]-5)[0][0]
        h2 = where(wlen < wlen_r[j][i][1]+5)[-1][-1]  # de longitudes de onda
        index_h = arange(h1, h2, 1)
    # figure(k)

        plot(wlen[index_h], intensidad[index_h], 'k-o')
        plot(x, fit_gauss[1], 'g')
        for k in range(0, len(wlen_peaks_r[j][i])):
            plot(x, first_gauss[0][k], 'r')
            plot(x, fit_gauss[0][k], 'b')
        show()

#    ##
#
# Manda a cero los valores en los que no hay picos verdaderos. Ej. O I en Si3N4 y viceversa
#
# for n in range(0,len(peaks_c)):
#    if peaks_w[n] > 2:   # Si no hay pico real, la gaussiana ajustada sera muy ancha
#        peaks_c[n] = 0
#        peaks_A[n] = 0
#        peaks_I[n] = 0
#        peaks_w[n] = 0
#    #
#    #c = array(peaks_c)
#    #array(peaks_w)
#    #array(peaks_I)
#
#
#c = array(peaks_c)
#c_err = array(err_c)
#    #c.shape = (24,1)
#
#I = array(peaks_I)
#I_err = array(err_I)
#    #I.shape = (24,1)
#
#w = array(peaks_w)
#w_err = array(err_w)
#    #w.shape = (24,1)
#
#A = array(peaks_A)
#    #A_err = array(err_A)
#
