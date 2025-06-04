# -*- coding: utf-8 -*-
#####


from . import spec_analysis, FitFunctions
from matplotlib import *
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from pylab import *
from numpy import *


def do_data_analysis(datos_peaks, defined_peaks: dict, rootdir):

    Pnumber = len(datos_peaks) // 4  # Numero de picos

    spec = 2

    especies = list(defined_peaks.keys())

    regiones, peaks = spec_analysis.Spectrometer(spec, especies)

    picos, wlen, intens, width, area = spec_analysis.separa2(
        datos_peaks, Pnumber)

    #####Corrector de datos #######
    # Verificar el indice de picos, para determinar el indice de area a corregir

    datos = [wlen, intens, width, area]
    title_param = ['Center', 'Maxima', 'Width', 'Area']

    ########   G R A F I C A S ###############

    x_data = arange(len(wlen[0]))
    #
    for k in arange(0, len(datos)):

        for i in range(0, len(especies)):

            especie = especies[i]
            elemento = peaks[especie]
            y_data, picos_element = spec_analysis.elementos(
                elemento, datos[k], picos)

            lgd = picos_element
            tit = title_param[k]
            # for j in range(0, len(y_data)):
            #     figure(k)
            #     plt.plot(x_data, y_data[j][0], label=str(lgd[j]))
            #     plt.title(tit)
            #     plt.xlabel('File number')

            #     plt.legend()
            #     plt.show()

    index = 2
    ArII_C = area[index]
    ArII_C = spec_analysis.corrector(ArII_C)
    #
    for i in range(0, len(area[index])):
        area[index][i] = ArII_C[i]

    ###### Suavizado de datos ######
    Area_smooth = []

    for i in range(0, len(especies)):

        especie = especies[i]
        elemento = peaks[especie]
        datos = area
        window_size, poly_order = 9, 3
        y_data, picos_element = spec_analysis.elementos(
            elemento, datos, picos)
        lgd = picos_element

        for j in range(0, len(y_data)):

            y_smooth = savgol_filter(
                y_data[j][0], window_size, poly_order, mode='mirror')
            Area_smooth.append(y_smooth)

            # figure(k+1)
            # plt.plot(x_data, y_smooth, label=str(lgd[j]))
            # plt.title(tit)
            # plt.xlabel('File number')

            # plt.legend()
            # plt.show()

    ####### Cálculo de Cocientes ########

    Ratios_all = []
    Ratios_smooth = []
    RatiosName_all = []
    datos = area

    for i in range(0, len(especies)):

        especie1 = especies[i]
        elemento1 = peaks[especie1]
        for j in range(i, len(especies)):
            especie2 = especies[j]
            elemento2 = peaks[especie2]

            if especie1 == especie2:
                pass
            else:

                R, Cociente = spec_analysis.cocientes(
                    elemento1, elemento2, datos, x_data, picos)
                # print R
                Ratios_all.append(Cociente)

                for k in range(0, len(Cociente)):

                    C_smooth = savgol_filter(Cociente[k], window_size,
                                             poly_order, mode='mirror')
                    Rname = R[k]
                    print(Rname)

                    RatiosName_all.append(Rname)

                    Ratios_smooth.append(C_smooth)

                    #   Graficas Ratios

            #       lgd = R[k]
            #       tit = especie1 + 'Ratios'
            #       v = [0, max(x_data), 0, 100]
            #
            #
            #       figure(5+i)
            #       plt.plot(x_data,C_smooth, label = lgd)
            #       plt.title(tit)
            #       plt.xlabel('File number')
            #
            #       plt.legend()
            #       plt.axis(v)
            #       plt.show()

    # Ratios_smooth.insert(0,RatiosName_all)
    # Area_smooth.insert(0,picos)

    carpeta = 'UV_proc\\'

    fname = '1704146U2_cat_peaks'

    saveratios = rootdir + carpeta + fname + '_S-ratios'+'.dat'
    saveareas = rootdir + carpeta + fname + '_S-areas'+'.dat'

    savetxt(saveratios, transpose(Ratios_smooth))
    savetxt(saveareas, transpose(Area_smooth))

    savetxt(rootdir + carpeta + fname + '_Areas.dat', transpose(area))
