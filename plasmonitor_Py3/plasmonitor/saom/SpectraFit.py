# -*- coding: utf-8 -*-

# LIBRERÍAS

from pylab import *
import numpy
import scipy.signal
from scipy.optimize import curve_fit
from . import FitFunctions, spec_analysis


def get_spectra_fit(espectro, defined_peaks: dict):

    wlen = espectro[:, 0]

    intens_index = arange(1, shape(espectro)[1])

    spec = 2

    # species = ['TiI', 'N2', 'N2plus', 'ArI', 'ArII']
    species = list(defined_peaks.keys())

    regiones, peaks = spec_analysis.Spectrometer(spec, species)

    wlen_r = [regiones[especie] for especie in species]

    wlen_peaks_r = [peaks[especie] for especie in species]

    peak_number = []
    wlen_column = []

    for i in arange(0, len(wlen_peaks_r)):
        for j in arange(0, len(wlen_peaks_r[i])):
            peak_index = len(wlen_peaks_r[i][j])
            # print peak_index
            peak_number.append(peak_index)
            peak_column = wlen_peaks_r[i][j]

            for h in arange(0, len(wlen_peaks_r[i][j])):
                wlen_column.append(peak_column[h])

    peak_number = sum(peak_number, axis=0)

    all_peaks = zeros((4*peak_number, len(intens_index)+1))
    all_err = zeros((3*peak_number, len(intens_index)+1))

    for k in intens_index:

        print(k)

        intensidad = espectro[:, k]
        intensidad_raw = espectro[:, k]

        if spec == 2:
            window = [1, 200]
        elif spec == 3:
            window = [1560, 1590]

        intensidad = spec_analysis.baseline(intensidad_raw, window)

    #### RUIDO ####

    # Se obtiene la desviacion estandar del promedio de una zona del espectro que con seguridad
    # no contenga lineas espectrales.
    # Ambos espectrometros muestran que los ultimos 40 pixeles no contienen lineas.

        #ruido = numpy.std(intensidad[xi_baseline:xf_baseline])*3

    #### AJUSTE DE MULTIPLES PICOS ####

        peaks_c = []   # vector con los centros de los picos
        err_c = []

        peaks_I = []   # vector con las intensidades
        err_I = []

        peaks_w = []   # vector con los anchos
        err_w = []

        peaks_A = []   # vector con las áreas

    # Secuencia de ajuste de cada pico para cada espectro
    #
        for j in range(0, len(wlen_r)):
            for i in range(0, len(wlen_r[j])):
                width_peaks = []
                intens_peaks_r = []
                peaks_param = []

                # selecciona los indices correspondientes a cada rango
                l1 = where(wlen > wlen_r[j][i][0])[0][0]
                # de longitudes de onda
                l2 = where(wlen < wlen_r[j][i][1])[-1][-1]
                index_r = arange(l1, l2, 1)

                x = linspace(wlen_r[j][i][0]-3, wlen_r[j][i][1]+3, 500)

                for n in range(0, len(wlen_peaks_r[j][i])):

                    width_peaks.append(0.2)
                    intens_peaks_r.append(max(intensidad[index_r]))

    # Parametros iniciales, obtenidos mediante el espectro

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
                        str(k) + ' at peak ' + str(peaks_param[0])
                    print(wrong_fit)
                    pass

            # print popt
                try:
                    err_fit = sqrt(np.diag(pcov))
                except:
                    exc_err = 'invalid value in err_fit ' + \
                        str(k) + ' at peak ' + str(peaks_param[0])
                    print(exc_err)
                    pass

    # Gaussianas ajustadas obtenidas con los parametros ajustados

                fit_gauss = FitFunctions.Gaussians(x, popt)

    # Cálculo de área bajo la curva
                area_fit = []

                for i in range(0, len(fit_gauss[0])):
                    area_fit.append(trapz(fit_gauss[0][i], x))

    # Recuperacion de parametros ajustados. Guardar informacion
                h = len(popt) // 3
                for i in range(0, h):
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

        for n in range(0, len(peaks_c)):
            # Si no hay pico real o no lo ajusta correctamente,
            if peaks_w[n] > 2 or peaks_I[n] < 0:
                # la gaussiana ajustada sera muy ancha
                peaks_c[n] = 0
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

        all_peaks[:, k] = hstack((c, I, w, A))
        all_err[:, k] = hstack((c_err, I_err, w_err))

    first_column = array(wlen_column*4)

    all_peaks[:, 0] = first_column

    return all_peaks, all_err
