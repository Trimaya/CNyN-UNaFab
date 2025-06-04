# -*- coding: utf-8 -*-(
### Codigo para el analisis de datos arrojados por los ajustes gaussianos a la
### las líneas de emisión


from  pylab import *
#import saomlib
import numpy
 


def Spectrometer(spec,especies):
#seleccionar pixeles para calculo de baseline, espectrometro y especies a analizar
#INPUTS. base: (px_in,px_fin)
#        spec: 1 = thorlabs, 2= avantesUV, 3 = avantesVISspecies
#        especies:  tupla de las especies a analizar

    #global thorlabs
    #global avantesVIS
    #global avantesUV    

   

####### THORLABS SPECTROMETER   #######
    if spec == 1: #Colocar en el diccionario los picos que corresponden 
                         # a cada especie así como los límites inferior y superior 
                         # de la region que lo contiene 

        regiones = {'ArI': [[696.25,698], [702.9,704.3]],
                    'ArII': [[461.1,462.7]],  # Contiene lineas de ArII visibles en Si_W
                    'N2': [[380.2,381.7]],
                    'N2plus': [[391.2,392.4]],
                    'OI': [[777.4,778.6]],
                    'TiI':[[465.35,470.0], [503.6,505.8]],
                    'AlI':[[395.9,396.8],[397.7,398.7]],
                    'AgI':[[546.8,547.5]],
                    'SiI':[[390.2,391.6]],
                    'WI':[]
               
                       }
        
        
        peaks = {'ArI': [[697.2],[703.7]], # longitudes de onda de los picos
                'ArII': [[461.8]],  #[ArII-460.96],[ArII-386.8nm],[ArI,ArII-517.6,ArI]
                'N2': [[381]],
                'N2plus': [[391.99]],
                'OI': [[778]],
                'TiI':[[466.4,467.4,468.9], [504.7]],
                'AlI':[[396.5],[398.2]],
                'AgI':[[547.2]],
                'SiI':[[391.1]],
                'WI':[]
                }
                
        #baseline = (3600, 3640)
        
        wlen_r = []
        for i in range (0,len(especies)):
            
            wlen_r.append(regiones[especies[i]]) 
            #print(wlen_r)
                
#####  AVANTES UV, NOMBRE DE ARCHIVOS: 1704146U2 ######              
    elif spec == 2:     #AVANTES UV
                        #Colocar en el diccionario los picos que corresponden 
                         # a cada especie así como los límites inferior y superior 
                         # de la region que lo contiene. Consultar archivo de identificacion de lineas correspondiente
        
        regiones = {'ArI': [[425.4,426.2],[450.5,451.2]],
                    'ArII': [[426.1,426.8],[427.4,428.0],[454.1,454.7]],  
                    'N2': [[315.5,316.5],[336.8,337.5],[357.4,357.9],[380.1,380.7]],
                    'N2plus': [[390.8,391.9]],
                    'OI': [],   #No hay lineas de oxigeno en esta region
                    'TiI':[],
                    'AlI':[[256.44,257.86],[256.44,257.86],[307.94,308.49]],
                    'AgI':[],
                    'SiI':[[243.1,243.9],[251,252.2],[287.7,288.6]],     
                    }
        
        peaks = {'ArI': [[425.8],[450.9]],
                'ArII': [[426.5],[427.6],[454.3]], #[1], Picos 1 y 3 de Ar I, pico 2 de Ar II
                'N2': [[315.9],[337.1],[357.6],[380.3]],
                'N2plus': [[391.3]],
                'OI': [],
                'TiI':[],
                'AlI':[[256.9],[257.6],[308.2]],
                'AgI':[],
                'SiI':[],     
                }
                
        #baseline = (0,28) #pixeles en los que se toma la linea base

#####  AVANTES VIS, NOMBRE DE ARCHIVOS: 1704147U2 ######  
    elif spec == 3:      #Colocar en el diccionario los picos que corresponden 
                         # a cada especie así como los límites inferior y superior 
                         # de la region que lo contiene. Consultar archivo de identificacion de lineas correspondiente
        
        regiones = {'ArI': [[590.4,592.4],[641.1,642.8],[686.1,688.3],[702.2,703.9],[706.2,707.3],[794.0,795.2],[825.6,826.9]],
                    'ArII': [[460.3,462.1],[465.2,467.0],[475.8,477.5]],  
                    'N2': [],
                    'N2plus': [[470.5,471.9]],
                    'OI': [[776.3,777.5],[843.3,845.1]],
                    'TiI':[[465.2,469.2]],
                    'AlI':[],
                    'AgI':[],
                    'SiI':[],
                    'WI':[]     
                    }
        
        
        peaks = {'ArI': [[591.3],[641.7],[687.2],[702.9],[706.6],[794.7],[826.1]],
                'ArII': [[461.2],[466.1],[476.7]], 
                'N2': [],
                'N2plus': [[470.9]],
                'OI': [[777.2],[844.2]],
                'TiI':[[465.8,466.9,468.4],[844.2]],
                'AlI':[],
                'AgI':[],
                'SiI':[],
                'WI':[]     
                }
                
        #baseline = (0,28) #pixeles en los que se toma la linea base   
        
    else:
        print("choose a valid spectrometer")
        
    #return baseline, regiones, peaks     
    return regiones, peaks  

def baseline(intensidad_raw,window):
    
    
    base = numpy.mean(intensidad_raw[window[0]:window[1]])
    intensidad = intensidad_raw - base
    print("baseline = ", base)
    
    return intensidad




# separa parametros de ajuste de la matriz de datos
def separa(rootdir,fname,peaks):
    
    fname = rootdir + fname
    data = loadtxt(fname, dtype = float)
    fil_col = shape(data)
    
    picos = zeros(peaks)  #Longitudes de onda de interes
    wlen = zeros((peaks,fil_col[1]-1))
    intensidad = zeros((peaks,fil_col[1]-1))
    width = zeros((peaks,fil_col[1]-1))
    areas = zeros((peaks,fil_col[1]-1))
         
    for i in range(0,peaks):
        picos[i] = round(data[i][0],1)
        wlen[i] = data[i][1:] 
        intensidad[i] = data[i+peaks][1:]
        width[i] = data[i+2*peaks][1:]
        areas[i] = data[i+3*peaks][1:]
        
    return picos, wlen, intensidad, width, areas

def separa2(data,peaks):
    
    fil_col = shape(data)
    
    picos = zeros(peaks)  #Longitudes de onda de interes
    wlen = zeros((peaks,fil_col[1]-1))
    intensidad = zeros((peaks,fil_col[1]-1))
    width = zeros((peaks,fil_col[1]-1))
    areas = zeros((peaks,fil_col[1]-1))
         
    for i in range(0,peaks):
        picos[i] = round(data[i][0],1)
        wlen[i] = data[i][1:] 
        intensidad[i] = data[i+peaks][1:]
        width[i] = data[i+2*peaks][1:]
        areas[i] = data[i+3*peaks][1:]
        
    return picos, wlen, intensidad, width, areas


def elementos(elemento,datos,picos):
    
            
    #elemento = peaks[especie]
    sep_datos = []
    elemento_wlen = []
    for j in range(0,len(elemento)):
        for i in range(0,len(elemento[j])):
            a = find(picos == elemento[j][i])
            #print a
            elemento_wlen.append(picos[a])
            
            sep_datos.append(datos[a])
            
            
    return sep_datos, elemento_wlen
            


    
### Eliminar puntos donde area == 0  debido a un mal ajuste de las lineas.
### Util para lineas muy debiles supuestamente siempre visibles (e.g. Ar II)
def corrector(T):
    #fil_col = shape(T)
    #print fil_col
    
    T1 = T
    T_corr = T

    #for i in range(0,fil_col[0]):
    #    for j in range(0,fil_col[1]):
    for k in range(1,len(T)):
        #print k
        if T1[k] == 0:
            #print T1
                #T_corr[i][j] = (T1[i][j-1] + T1[i][j+1])/2
            T_corr[k] = T1[k-1]
            
        
    return T_corr
                
            

     
def cocientes(especie1,especie2,datos,r,picos):
# INPUTS: especie1, especie2. Strings con el nombre de las especies cuyo cociente se quiera calcular
#       r: rango de indices en el que se efectuara el cociente 
#    datos: matriz con todas las áreas. La función corre elementos para obtener las areas de cada especie 
#    picos: vector con todos los picos para poder correr elementos.

    
    T1, picos1 = elementos(especie1,datos,picos)
    #print T1
    T2, picos2 = elementos(especie2,datos,picos)
    #print T2
    
    C = zeros((len(T1)*len(T2),len(r)))
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
            
            
            
            



