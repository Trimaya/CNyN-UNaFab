###Codigo en Python 3 para el ajuste de una gaussiana en lineas espectrales##
##Librerias##
import numpy as np
################################################################################
def Picos(wlen,intensidad,p_crit,ruido): ##Encontrar picos
	#Picos 
	peaks_wlen=[]
	peaks_intens=[]
	peaks_index=[]
	peaks_fwhm=[]
	
	derivdad=np.diff(intensidad)
	
	for i in range(1,(len(wlen)-3)):
		if (derivada[i] > 0 and derivada[i+1] < 0 and derivada[i+2] < 0)\
        or (derivada[i] > 0 and derivada[i-1] > 0 and derivada[i+1] < 0): 
			max_local = intensidad[i+1]
			if (max_local> ruido and (max_local-intensidad[i+2]) > ruido/4) \
			and (max_local> ruido and (max_local-intensidad[i]) > ruido/4):
				peaks_wlen.append(wlen[i+1])    
				peaks_intens.append(intensidad[i+1])
				peaks_index.append(i+1)
	
	## CÁLCULO DE ANCHO DE LINEA## 
		# A ojo se observa que la altura media de cada pico ocurre a dos pixeles del centro del pico.
		# Como guess inicial para el ajuste consideremos que el half width at the half maximum esta a dos pixeles del centro   
	for i in range(0,len(peaks_index)):    
		fwhm = 2 * (wlen[peaks_index[i]]-wlen[peaks_index[i]-2])
		peaks_fwhm.append(fwhm)
	
	return  peaks_index, peaks_wlen, peaks_intens, peaks_fwhm
################################################################################
def One_Gaussian(x,x0,y0,w):
	y = y0*np.exp(-2*(x-x0)**2/w**2)        
	return y 
################################################################################
def Gaussians(x,peaks_param): ##Suma de Gaussianas para mejor ajuste
	y = []
	n = int(len(peaks_param)/3)
	for i in range(0,n):
		w = peaks_param[i+2*n]/np.sqrt(np.log(4))
		y0 = peaks_param[i+n]
		x0 = peaks_param[i]
		y_i = y0*np.exp(-2*(x-x0)**2/w**2)
		y.append(y_i)
	y_sum = np.sum(y,axis=0)   #suma todas las gaussianas  
	return y, y_sum
################################################################################
def N_Gaussians(x,*peaks_param):
    #INPUTS:
    # x: variable independiente
    # peaks_param: vector con los parametros a ajustar:=(peaks_wlen, peaks_intens, peaks fwhm)
	y = 0
	n = int(len(peaks_param)/3)
	for i in range(0,n):
		w = peaks_param[i+2*n]/np.sqrt(np.log(4))
		y0 = peaks_param[i+n]
		x0 = peaks_param[i]
		y += One_Gaussian(x,x0,y0,w)
	return y
##################################################################################
def N_Gaussians_Wcte(x,*peaks_param): #Ajuste base
    #INPUTS:
    # x: variable independiente
    # peaks_param: vector con los parametros a ajustar:=(peaks_wlen, peaks_intens, peaks fwhm)
	w = 1.0
	y = 0
	n = int(len(peaks_param)/3)
	for i in range(0,int(n)):
		y0 = peaks_param[i+n]
		x0 = peaks_param[i]
		y += One_Gaussian(x,x0,y0,w)
	return y
####################################################################################
def Areas(x,y):
	area = []
	for i in range(0,len(y)):
		intensidad = array(y[0][i])
		a_i = np.trapz(intensidad,x)
		area.append(a_i)
	return area