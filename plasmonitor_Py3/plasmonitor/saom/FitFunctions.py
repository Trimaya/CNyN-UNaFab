# -*- coding: utf-8 -*-
from pylab import *
import numpy
from matplotlib import *


# def Lorentziana(Picos2i,Xmin,Xmax):
#    x=[k for k in arange(Xmin,Xmax,abs(Xmax-Xmin)/1200.0)]
#    y=[k for k in arange(Xmin,Xmax,abs(Xmax-Xmin)/1200.0)]
#    gamma=Picos2i[3]
#    X0=Picos2i[0]
#    for i in range(0,len(x)):
#        y[i]=(gamma**2/(((x[i]-X0)**2)+gamma**2))
#    return [x,y]
#
# def Lorentziana(Picos2i,Xmin,Xmax):
#    x=[k for k in arange(Xmin,Xmax,abs(Xmax-Xmin)/1200.0)]
#    y=[k for k in arange(Xmin,Xmax,abs(Xmax-Xmin)/1200.0)]
#    gamma=Picos2i[3]
#    X0=Picos2i[0]
#    for i in range(0,len(x)):
#        y[i]=(gamma**2/(((x[i]-X0)**2)+gamma**2))
#    return [x,y]


def Picos(wlen, intensidad, p_crit, ruido):
    # Funcion que detecta picos derivando punto a punto.
    # Inputs: wlen: vector con longitudes de onda
    #        intensidad: vector con las intensidades
    #        dispersion: numero minimo de puntos en que la intensidad ebe ser creciente. Criterio para definir un pico
    #        ruido: intensidad minima para ser considerado un pico
    # Output: Vector con las longitudes de onda e intensidades de los centros de los picos

    #    # DETECTAR PICOS

    peaks_wlen = []       # longitud de onda de los picos
    peaks_intens = []    # intensidades de los picos
    peaks_index = []    # numero de pixel donde se encuentra el pico
    peaks_fwhm = []

    derivada = diff(intensidad)

    for i in range(1, (len(wlen)-3)):
        # if (derivada[i] > 0 and derivada[i+1] < 0 ):
        if (derivada[i] > 0 and derivada[i+1] < 0 and derivada[i+2] < 0)\
                or (derivada[i] > 0 and derivada[i-1] > 0 and derivada[i+1] < 0):
            max_local = intensidad[i+1]

            if (max_local > ruido and (max_local-intensidad[i+2]) > ruido/4) \
               and (max_local > ruido and (max_local-intensidad[i]) > ruido/4):
                peaks_wlen.append(wlen[i+1])

                peaks_intens.append(intensidad[i+1])
                peaks_index.append(i+1)

    # CÁLCULO DE ANCHO DE LINEA,
 # A ojo se observa que la altura media de cada pico ocurre a dos pixeles del centro del pico.
 # Como guess inicial para el ajuste consideremos que el half width at the half maximum esta a dos pixeles del centro

    for i in range(0, len(peaks_index)):

        fwhm = 2 * (wlen[peaks_index[i]]-wlen[peaks_index[i]-2])
        peaks_fwhm.append(fwhm)

    return peaks_index, peaks_wlen, peaks_intens, peaks_fwhm
#
#
    # CONSTRUCCION DE PRIMERAS GAUSSIANAS, ANTES DEL AJUSTE.


def Gaussians(x, peaks_param):
    #  y = y0*exp(-2(x-x0)^2/w^2;  y0 = A/[w*sqrt(pi/2)];  w = fwhm/sqrt(ln4)

    y = []
    n = len(peaks_param) // 3
    for i in range(0, n):
        w = peaks_param[i+2*n]/sqrt(log(4))
        y0 = peaks_param[i+n]
        x0 = peaks_param[i]
        y_i = y0*exp(-2*(x-x0)**2/w**2)
        y.append(y_i)

        # plot(x,y_i,'-.')
        # show()

    y_sum = sum(y, axis=0)  # suma todas las gaussianas
    #    plot (x,y_sum, 'g-')
    return y, y_sum


def One_Gaussian(x, x0, y0, w):
    # Inputs:
    #x = wlen; w = width = fwhm/sqrt(log(4));
    # y0 = intensidad del pico = Area / (w*sqrt(pi2)); x0 = centro del pico
    #x0 = 357.37537159839275
    y = y0*exp(-2*(x-x0)**2/w**2)
    return y


def Parametros(x0):
    return x0


def N_Gaussians(x, *peaks_param):
    # INPUTS:
    # x: variable independiente
    # peaks_param: vector con los parametros a ajustar:
    # peaks_param = (peaks_wlen, peaks_intens, peaks fwhm)
    #p_wlen = [357.37537159839275]
    #p_wlen = [357.37,358.23]
    #p_width = [0.3,0.87,0.3]
    #w = 0.87/sqrt(log(4))
    y = 0
    #n = len(peaks_param)/3
    # for i in range(0,n):
    n = len(peaks_param)/3
    for i in range(0, n):
        w = peaks_param[i+2*n]/sqrt(log(4))
        #w = p_width[i]/sqrt(log(4))
        y0 = peaks_param[i+n]
        x0 = peaks_param[i]
        #x0 = p_wlen[i]
        y += One_Gaussian(x, x0, y0, w)

        #w = peaks_param[i+2*n]/sqrt(log(4))
        #y0 = peaks_param[i+n]
        #x0 = peaks_param[i]
        ##x0 = p_wlen[i]
        ##w = p_width[i]/sqrt(log(4))
        #y += One_Gaussian(x,x0,y0,w)
#        y.append(y_i)
    return y


def N_Gaussians_Wcte(x, *peaks_param):
    # INPUTS:
    # x: variable independiente
    # peaks_param: vector con los parametros a ajustar:
    # peaks_param = (peaks_wlen, peaks_intens, peaks fwhm)
    #p_wlen = [357.37537159839275]
    #p_wlen = [357.37,358.23]
    #p_width = [0.3,0.87,0.3]
    w = 1.0
    y = 0
    #n = len(peaks_param)/3
    # for i in range(0,n):
    n = len(peaks_param)/3
    for i in range(0, n):
        #w = peaks_param[i+2*n]/sqrt(log(4))
        #w = p_width[i]/sqrt(log(4))
        y0 = peaks_param[i+n]
        x0 = peaks_param[i]
        #x0 = p_wlen[i]
        y += One_Gaussian(x, x0, y0, w)

        #w = peaks_param[i+2*n]/sqrt(log(4))
        #y0 = peaks_param[i+n]
        #x0 = peaks_param[i]
        ##x0 = p_wlen[i]
        ##w = p_width[i]/sqrt(log(4))
        #y += One_Gaussian(x,x0,y0,w)
#        y.append(y_i)
    return y


def Areas(x, y):

    area = []
    for i in range(0, len(y)):
        intensidad = array(y[0][i])
        a_i = trapz(intensidad, x)
        area.append(a_i)

    return area

# def Ajuste(f_peaks,wlen,intens):
#    f_peaks

    # puntos = 2 #numero de pixeles (de subida y/o bajada) para que se considere un pico.
    #            # Hasta ahora solo funciona de esta forma ??
    # diferencial = numpy.diff(intensidad)  # obtiene la derivada punto a punto
    #tup_diferencial = tuple(diferencial)
    #
    #peaks_wlen = []
    #peaks_intensidad = []
    # for i in range(puntos,(len(diferencial)-1)):
    #    while diferencial[i] > 0 and diferencial[i+1] < 0 and intensidad[i+1] > ruido:
    #        peak = []
    #
    #        for j in range(i-puntos+1,i):
    #            peak.append(diferencial[j]>0 and diferencial[j+puntos+1]<0)
    #            if peak[j-i+puntos-1] == False:
    #                option1 = diferencial[j] <0 and diferencial[j+puntos+1]<0
    #                option2 = diferencial[j] >0 and diferencial[j+puntos+1]>0
    #                if option1 == True or option2 == True:
    #                    peak[j-i+puntos-1] = True
    #                else:
    #                     peak[j-i+puntos-1] = False
    #            else:
    #                continue
    #
    #            #print peak
    #
    #        if False not in peak:
    #
    #            peaks_wlen.append(wlen[i+1])
    #            peaks_intensidad.append(intensidad[i+1])
    #        break
    #
    #    while diferencial[i+1] < 0:    #hombro por la derecha. Encuentra un maximo local
    #        if diferencial[i-1] < diferencial[i] < diferencial[i+1] and diferencial[i+1]> diferencial[i+puntos+1]:
    #            peaks_wlen.append(wlen[i+1])
    #            peaks_intensidad.append(intensidad[i+1])
    #        break
    #    while diferencial[i+1] > 0:   # hombro por la izquierda. Encuentra un minimo local
    #        if diferencial[i-1] > diferencial[i] > diferencial[i+1] and diferencial[i+1]< diferencial[i+puntos+1]:
    #            peaks_wlen.append(wlen[i+1])
    #            peaks_intensidad.append(intensidad[i+1])
    #        break
    #
    #
    #
    # return peaks_wlen, peaks_intensidad, tup_diferencial
    #
    #


# def Lo(Picos2i,x0):
# aquí entra Picos2i de la forma [longitud de onda, intensidad, número de pico, gamma]
#    valor=(Picos2i[1]*Picos2i[3]**2/(((x0-Picos2i[0])**2)+Picos2i[3]**2))
#    return valor
#
# def LorentzRapido(B,LongMint,LongMaxt,dispersion,altura):
# [wave length, high, element number, gamma]
#    for i in range(1,len(B)):
#        if LongMint<B[1][0]:
#            LongMin=1
#        if LongMaxt>B[len(B)-1][0]:
#            LongMax=len(B)-1
#        if B[i][0]<LongMint:
#            LongMin=i+1
#        if B[i][0]<LongMaxt:
#            LongMax=i
#    # DETECTAR PICOS POR DECAIMIENTO
#    i=1;
#    up=1;
#    maxi=0;
#    elemento=0;
#    Picos2=[]
#    for longwave in range(LongMin,LongMax-dispersion):
#        if B[longwave+dispersion][1]>B[longwave][1]:   # up=1 si la curva 'subirá en el for siguiente
#            up=1
#        for i in range(longwave+1,longwave+dispersion+1):    # Revisar este +1
#            if B[longwave][1]>B[i][1] and up==1:    # Si la curva estaba subiendo, pero a partir de este punto solo baja
#                maxi=1                               #  entonces está en un máximo y maxi=1
#            else:
#                maxi=0                               # Si seguirá subiendo, entonces no es un máximo y maxi=0
#                break
#        if (maxi==1) and (B[longwave][1]>altura): # && (diferencia > promedio) Si es un máximo y está arriba de la 'línea de ruido', entonces guardamos su posición, altura y el número de lista en nuestros datos originales
#            Picos2.append([B[longwave][0],B[longwave][1],longwave])  # Va agregando los datos a la lista Picos2. La funcion append es para crear nuevos elementos en la lista
#            up=0
#            maxi=0
#            elemento=elemento+1
#
#     # CÁLCULO DE GAMMA, AJUSTE Y GRÁFICA DE LORENTZIANAS
#    for x in range(0,elemento):
#        AlturaTeo=Picos2[x][1]/2.0     # Calcula la altura a la mitad del pico
#        # ESCANEO A LA DERECHA
#        y=2
#        aproxR=abs(AlturaTeo-B[Picos2[x][2]+1][1])
#        gammaR=abs(Picos2[x][0]-B[Picos2[x][2]+1][0])
#        while ((Picos2[x][2]+y)<=(len(B[:])-1)) & (x!=elemento-1):
#            if (B[Picos2[x][2]+y][0]<Picos2[x+1][0]) & (B[Picos2[x][2]+y][1]>=AlturaTeo):
#                if abs(AlturaTeo-B[Picos2[x][2]+y][1])<aproxR:
#                    aproxR=abs(AlturaTeo-B[Picos2[x][2]+y][1])
#                    gammaR=abs(Picos2[x][0]-B[Picos2[x][2]+y][0])
#            else:
#                break
#            y=y+1
#
#        # ESCANEO A LA IZQUIERDA     # Lo mismo pero a la izquierda
#        y=2
#        aproxL=abs(AlturaTeo-B[Picos2[x][2]-1][1])
#        gammaL=abs(Picos2[x][0]-B[Picos2[x][2]-1][0])
#        while ((Picos2[x][2]-y)>=0) & (x!=0):
#            if (B[Picos2[x][2]-y][0]>Picos2[x-1][0]) & (B[Picos2[x][2]-y][1]>=AlturaTeo):
#                if abs(AlturaTeo-B[Picos2[x][2]-y][1])<aproxR:
#                    aproxL=abs(AlturaTeo-B[Picos2[x][2]-y][1])
#                    gammaL=abs(Picos2[x][0]-B[Picos2[x][2]-y][0])
#            else:
#                break
#            y=y+1
#
#        if aproxR<aproxL:
#            gamma=gammaR
#        else:
#            gamma=gammaL
#        Picos2[x].append(gamma)
#        Picos2[x][2]=x
#    return Picos2
#
# def GraficarDatos(B,LongMint,LongMaxt):
#    for i in range(1,len(B)):
#        if LongMint<B[1][0]:
#            LongMin=1
#        if LongMaxt>B[len(B)-1][0]:
#            LongMax=len(B)-1
#        if B[i][0]<LongMint:
#            LongMin=i+1
#        if B[i][0]<LongMaxt:
#            LongMax=i
#    # GRAFICAR DATOS ORGINALES
#    x=[B[i][0] for i in range(LongMin,LongMax+1)]
#    y=[B[i][1] for i in range(LongMin,LongMax+1)]
#    plot(x,y,'g o')
#    show()
#    hold(True)
#
# def GraficarAjustes(Picos2,Xmin,Xmax):
# GRAFICAR LORENTZIANA DEL PICO 'x'
#    for i in range(0,len(Picos2)):
#        hold(True)  # Se grafican las lorentzianas por separado
#        [xLorentz,yLorentz]=Lorentziana(Picos2[i],Xmin,Xmax)
#        hyLorentz=[Picos2[i][1]*l for l in yLorentz]
#        plot(xLorentz,hyLorentz,'k')
#        show()
#
# def LorentzRapido2(B,LongMint,LongMaxt,dispersion,altura):
# [wave length, high, element number, gamma]
#    for i in range(1,len(B)):
#        if LongMint<B[1][0]:
#            LongMin=1
#        if LongMaxt>B[len(B)-1][0]:
#            LongMax=len(B)-1
#        if B[i][0]<LongMint:
#            LongMin=i+1
#        if B[i][0]<LongMaxt:
#            LongMax=i
#    # DETECTAR PICOS POR DECAIMIENTO
#    i=1;
#    up=1;
#    maxi=0;
#    elemento=0;
#    Picos2=[]
#    for longwave in range(LongMin,LongMax-dispersion):
#        if B[longwave+dispersion][1]>B[longwave][1]:   # up=1 si la curva 'subirá en el for siguiente
#            up=1
#        for i in range(longwave+1,longwave+dispersion+1):    # Revisar este +1
#            if B[longwave][1]>B[i][1] and up==1:    # Si la curva estaba subiendo, pero a partir de este punto solo baja
#                maxi=1                               #  entonces está en un máximo y maxi=1
#            else:
#                maxi=0                               # Si seguirá subiendo, entonces no es un máximo y maxi=0
#                break
#        if (maxi==1) and (B[longwave][1]>altura): # && (diferencia > promedio) Si es un máximo y está arriba de la 'línea de ruido', entonces guardamos su posición, altura y el número de lista en nuestros datos originales
#            Picos2.append([B[longwave][0],B[longwave][1],longwave])  # Va agregando los datos a la lista Picos2. La funcion append es para crear nuevos elementos en la lista
#            up=0
#            maxi=0
#            elemento=elemento+1
#
#     # CÁLCULO DE GAMMA, AJUSTE Y GRÁFICA DE LORENTZIANAS
#    for x in range(0,elemento):
#        mini1=B[Picos2[x][2]+1][1]
#        mini2=B[Picos2[x][2]-1][1]
#        if mini1<mini2:
#            xn=B[Picos2[x][2]+1][0]
#            gamma=abs(B[Picos2[x][2]][0]-xn)/sqrt((B[Picos2[x][2]][1]/B[Picos2[x][2]+1][1])-1)
#        else:
#            xn=B[Picos2[x][2]-1][0]
#            gamma=abs(B[Picos2[x][2]][0]-xn)/sqrt((B[Picos2[x][2]][1]/B[Picos2[x][2]-1][1])-1)
#        Picos2[x].append(0.9*gamma)
#    return Picos2


# if __name__ == '__main__':
#    from pylab import *        # Estas lineas permiten correr el codigo por si mismo.
#    import numpy              # lo que esta abajo no se ejecuta cuando se importa en el main
#
#    print("Testing module.")
#    data = arange(10)
#    print "Data: {0}".format(data)
#    print "Square = {0}".format(square(data))
#    print "Cube = {0}".format(cube(data))
#    print(" ")
#    print("functions.py... ok!")
