##Python_3
##Librerias##
import matplotlib as plt
import matplotlib.pylab as pylab
import numpy as np
################################################################################
def Spectrometer(spec,especies):
#seleccionar pixeles para calculo de baseline, espectrometro y especies a analizar
#INPUTS:
#	base: (px_in,px_fin)
#   spec: 1 = thorlabs, 2= avantesUV, 3 = avantesVISspecies
#   especies:  tupla de las especies a analizar
#		global thorlabs
#		global avantesVIS
#		global avantesUV

	##Thorlabs Spectrometer#####################################################
	if spec==1:
		#Regiones alrededor de los picos
		regiones = {'ArI': [[451.1,452.5], [702.7,704.3],[825.2,827.8]],
					'ArII': [[404.08,404.72]],  # Contiene lineas de ArII visibles en Si_W
					'N2': [[380.2,381.7]],
					'N2plus': [[391.2,392.4]],
					'OI': [[776.8,778.5]],
					'TiI':[[465.2,470.0]],
					'AlI':[[395.9,396.8],[397.7,398.7]],
					'AgI':[[546.8,547.5]],
					'SiI':[[390.2,391.6]],
					'WI':[]
					}
		# longitudes de onda de los picos
		peaks = {'ArI': [[451.8],[703.7],[826.8]], 
				'ArII': [[404.34]],  #[ArII-460.96],[ArII-386.8nm],[ArI,ArII-517.6,ArI]
				'N2': [[381]],
				'N2plus': [[391.99]],
				'OI': [[778]],
				'TiI':[[466.2,467.3,468.7]],
				'AlI':[[396.5],[398.2]],
				'AgI':[[547.2]],
				'SiI':[[391.1]],
				'WI':[]
				}
		wlen_r=[]
		for i in range(0,len(especies)):
			wlen_r.append(regiones[especies[i]])
	#####  AVANTES UV, NOMBRE DE ARCHIVOS: 1704146U2 ###### 
	elif spec==2:
		regiones = {'ArI': [[425.5,426.1],[450.5,451.2]], #Analisis Pulsada
                    #'ArI': [[450.5,451.2]],  
                    
                    'ArII': [[404,404.8],[454.1,454.6],[458.5,459.2],[460.5,461.3]], #Analisis Pulsada
                    #'ArII': [[404,404.8],[454.1,454.7],[460.5,461.3]],   
                   
                    'N2': [[315.5,316.5],[357.4,357.9],[380.1,380.7]], #Analisis Pulsada
                    #'N2': [[315.3,316.5],[380,381]],
                    
                    #'N2plus': [[357.9,358.8],[390.8,391.9],[427.4,428.0]],#Analisis Pulsada
                    'N2plus': [[390.8,391.9]],
                    
                    'OI': [],   #No hay lineas de oxigeno en esta region
                    
                    'TiI':[[259.5,260.9],[318,319.7],[364.9,365.7],[390.8,391.9],[398.4,399.4]],#Analisis Pulsada
                    #'TiI':[[318,320.5]],
                    
                    'TiII':[[316.8,317.5],[316.5,317.3],[332.6,333.2]],#Analisis Pulsada
                    
                    #'AlI':[[256.3,258.1]],
                    'AlI':[[256.4,257.9], [307.6,308.8]],
                    'AgI':[],
                    #'SiI':[[243.1,243.9],[250.3,251.1],[287.7,288.6],[390.2,390.9]],
                    'SiI':[[251,252.1],[287.7,288.6]],
                    'WI':[[254.8,255.5],[400.5,401.2],[429.0,429.6]]     
                    }
                    
		peaks = {'ArI': [[425.8],[450.9]], #Analisis Pulsada
                #'ArI': [[450.9]],   #La 425 está superpuesta con N2
                
                'ArII': [[404.3],[454.3],[458.9],[460.8]], #Analisis Pulsada
                #'ArII': [[404.3,405.3],[433.2],[454.3],[460.8]], 
                
                'N2': [[315.9],[357.6],[380.3]], #Analisis Pulsada
                #'N2': [[315.8],[380.3]],
                               
                #'N2plus': [[358.1],[391.3],[427.7]], #Analisis Pulsada
                'N2plus': [[391.3]],
                
                'OI': [],
                
                'TiI':[[260,260.5],[318.6,319.2],[365.3],[391.3],[398.9]],#Analisis Pulsada
                #'TiI':[[318.6,319.2,319.9]],#Ti 363.5,364.2,394.78,429.9.
                
                'TiII':[[316.2],[316.8],[332.9]],#Analisis Pulsada
                
                #'AlI':[[256.8,257.6]],
                'AlI':[[256.9,257.6], [308.2]],
                'AgI':[],
                #'SiI':[[243.5],[250.7],[288.1],[390.6]], 
                'SiI':[[251.6],[288.1]],
                'WI':[[255.2],[400.8],[429.3]]   #El 4o pico no es W    
                }
	#####  AVANTES VIS, NOMBRE DE ARCHIVOS: 1704147U2 ######
	elif spec == 3:        
		regiones = {#'ArI': [[590.4,592.4],[641.1,642.8],[686.7,688.3],[702.2,703.9],[706.2,707.3],[794.0,795.2],[825.6,826.9]],
				#'ArI':  [[702.1,703.8],[794.0,795.2],[825,827.4]],
				'ArI':  [[825,827.4]],
				'ArII': [[460.5,461.9]],  
				#'ArII': [[453.8,455.2],[475.8,477.5]],
				'N2': [], #Nitrogeno atomico
				#'N2': [[741.4,745.4]], #Nitrogeno atomico
				'N2plus': [],
				#'N2plus': [[470,471.9]],
				'OI': [[776.7,777.9],[843.3,845.1]],
				'TiI':[[550.6,552.7]],
				'AlI':[],
				'AgI':[],
				'SiI':[],
				'WI':[]     
				}     
		peaks = {#'ArI': [[591.3],[641.7],[687.2],[702.9],[706.6],[794.7],[826.1]], # Lineas para oxidos
				#'ArI': [[702.9],[794.6],[826.3]],# Lineas para nitruros
				'ArI': [[826.3]],
				'ArII': [[461.2]], 
				#'ArII': [[454.5],[476.7]], 
				'N2': [],
				# 'N2': [[742.4,743.5,744.3,745.0]],
				'N2plus': [],
				#'N2plus': [[470.9]],
				'OI': [[777.1],[844.2]],
				'TiI':[[551.5]],
				'AlI':[],
				'AgI':[],
				'SiI':[],
				'WI':[] 
				}
	else:
		print('choose a valid spectrometer')
	return regiones, peaks
##################################################################################
def baseline(intensidad_raw,window):
	base = np.mean(intensidad_raw[window[0]:window[1]])
	intensidad = intensidad_raw - base
	print('baseline = ', base)
	return intensidad
##################################################################################
def calibraUV(wlen,intensidad):
	nwlen = wlen
	print('Revisar direccion de la calibracion')
	factor = loadtxt('C:\\Users\\Maui\\Documents\\PYTHON\AnalisisEspectroscopia\\CalibracionUV_2019a2017_l3i.dat')
	nintensidad = intensidad*factor
	return (nwlen,nintensidad)
###################################################################################    
def calibraVIS(wlen,intensidad):
	nwlen = wlen #Ajuste entre las longitudes de onda de ambos espectrometros.
	print('Revisar en codigo direccion de la calibracion')
	factor = loadtxt('C:\\Users\\Maui\\Documents\\PYTHON\AnalisisEspectroscopia\\CalibracionVIS_AvantesNew.dat')
	nintensidad = intensidad*factor
	return (nwlen,nintensidad)
####################################################################################
def separa(rootdir,fname,peaks): # separa parametros de ajuste de la matriz de datos
	fname = rootdir + fname
	data = np.loadtxt(fname, dtype = float)
	fil_col = np.shape(data)    
	picos = np.zeros(peaks)  #Longitudes de onda de interes
	wlen = np.zeros((peaks,fil_col[1]-1))
	intensidad = np.zeros((peaks,fil_col[1]-1))
	width = np.zeros((peaks,fil_col[1]-1))
	areas = np.zeros((peaks,fil_col[1]-1))     
	for i in range(0,peaks):
		picos[i] = round(data[i][0],1)
		wlen[i] = data[i][1:] 
		intensidad[i] = data[i+peaks][1:]
		width[i] = data[i+2*peaks][1:]
		areas[i] = data[i+3*peaks][1:]       
	return picos, wlen, intensidad, width, areas
#####################################################################################
def elementos(elemento,datos,picos):
	sep_datos = []
	elemento_wlen = []
	for j in range(0,len(elemento)):
		for i in range(0,len(elemento[j])):
			a = find(picos == elemento[j][i])
			elemento_wlen.append(picos[a])
			sep_datos.append(datos[a])
	return sep_datos, elemento_wlen
######################################################################################    
def corrector(T):
### Eliminar puntos donde area == 0  debido a un mal ajuste de las lineas.
### Util para lineas muy debiles supuestamente siempre visibles (e.g. Ar II)
	T1 = T
	T_corr = T
	for k in range(1,len(T)):
		if T1[k] == 0:
			#T_corr[i][j] = (T1[i][j-1] + T1[i][j+1])/2
			T_corr[k] = T1[k-1]
	return T_corr
#######################################################################################     
def cocientes(especie1,especie2,datos,r,picos):
# INPUTS: especie1, especie2. Strings con el nombre de las especies cuyo cociente se quiera calcular
#       r: rango de indices en el que se efectuara el cociente 
#    	datos: matriz con todas las áreas. La función corre elementos para obtener las areas de cada especie 
#    	picos: vector con todos los picos para poder correr elementos.
	T1, picos1 = elementos(especie1,datos,picos)
	T2, picos2 = elementos(especie2,datos,picos)
	C = np.zeros(int(len(T1)*len(T2),len(r)))
	peaks_ratio = []
	count = 0        
	for i in range(len(T1)):        
		for j in range(len(T2)):
			C[count] =  T1[i][0][r] / T2[j][0][r]
			#where(C == inf, [0,])
			#where(C == nan, C = 0)
			#print C
			#i1 = where(T1[i][r] <0 )
			#T1[i][i1] = 0
			peaks_ratio.append(str(picos1[i])+'/'+str(picos2[j]))
			count +=1        
	return peaks_ratio, C