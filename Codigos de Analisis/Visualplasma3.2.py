##################################### SAOM-LAB #################################################
######## This code allows selecting different parts of the spectral line's areas  ##############
######### This code calculates the average and standard deviation from the selected data #######
############ V3.2 calculates the averge in a window of time of n items #########################
############  collected by Avantes or Labwiew, Uses Python 3.x.x  RRL ##########################
################################################################################################


import numpy as np
import pandas as pd
from matplotlib.widgets import SpanSelector
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
import matplotlib.pyplot as plt

## This rutine is used to read the raw data ##
## Enter the directory where the file is located ##
#rootcd = r'C:\Users\Maui\Documents\TrabajosCNyN\DatosEspectroscopicos_proc\Avantes\Si&W\kb5\UV_proc'
#rootcd = r'F:\DatosEspectroscopicos_proc\Pulsada\2021-10\LAI-2\UV_proc'
#rootcd = r'E:\DatosEspectroscopicos_proc\Pulsada\2021-04\l46\VIS_proc'
rootcd = r'E:\DatosEspectroscopicos_proc\Wencel\2021-10\LB3\UV_proc'
#rootcd = r'E:\L96\Sputter\UV_proc'
#rootcd = r'E:\DatosEspectroscopicos_proc\Wencel\2021-09\L93\VIS_proc'

diagonal = '\\'
## Enter the file name with the extension (.txt or .dat) ##
## Enter the file name with its type (.txt or .dat) ##
file = r'1704146U2_cat_peaks_Areas.dat'
#file = r'1704147U2_cat_peaks_Areas.dat'

#file = r'1906287U2_cat_peaks_Areas.dat'

c_dir = rootcd+diagonal+file
print(c_dir)
## True if you want to average the raw data, otherwise False ##
mean_all_data = True
average_number = 5 # set the size of the window, for example (5)--0 1 2 3 4, will choose the center 2
                    # and will average the data and save the value, then 1 2 3 4 5, 3 will be selected and so on...


        ######### Label the species in the same order that are in spec_analysis.py ########

#Species VIS:
#ArI: 'ArI_426','ArI_560','ArI_703','ArI_826'
#ArII: 'ArII_404','ArII_461'

#species_VIS = ['TiI_466','TiI_467','TiI_468', 'ArII_460','ArI_451', 'ArI_703','ArI_826','OI_778']
#species_VIS = ['ArII_460','ArI_826']
#species_VIS = ['ArII_404','ArII_461','ArI_426','ArI_560','ArI_703','ArI_826']

#Species UV:
#TiI =['TiI_260','TiI_260.5','TiI_318','TiI_319','TiI_365','TiI_391','TiI_399']
#TiII= ['TiII_316','TiII_316.8','TiII_332.9']
#ArII_UV = ['ArII_404','ArII_454','ArII_459','ArII_461']
#ArI_UV = ['ArI_426','ArI_450']
#N2 = ['N2_315','N2_357','N2_380']
#N2plus = ['N2+_358','N2+_391','N2+_427']

#species_UV = ['SiI_250','SiI_288','ArI_451','N2_315', 'N2_336','N2_357','N2_380','N2plus_358']
species_UV = ['SiI_250','SiI_288','N2plus_391']
#species_UV = ['TiI_260','TiI_260.5','TiI_318','TiI_319','TiI_365','TiI_391','TiI_399','TiII_316','TiII_316.8','TiII_332.9',
           #  'ArII_404','ArII_454','ArII_459','ArII_461','ArI_426','ArI_450','N2_315','N2_357','N2_380','N2+_358','N2+_391','N2+_427'] #Analisis Pulsada

if 'DATOSESPECTROSCOPICOS' in c_dir.upper(): ## This reading routine is used for the gaussian fit from the spec_analysis data ##
    print ('Spec_analysis data (Gaussian method)')
    ## Read the data from spec analysis using the white space delimiter ##
    framedata = pd.read_csv(c_dir, delim_whitespace= True, header= None)

    ## Read the TIme data located in the same folder and set it to zero ##
    if 'VIS' in c_dir.upper():
        print('ViS data')

        species = species_VIS

        if 'MEDICIONES' in  c_dir.upper():
        ## The time extracted form the data name will be used ##
            t_uv = pd.read_csv(rootcd+diagonal+'VISTime.dat', delim_whitespace = True, header = None)
            t_uv = t_uv.abs()
            using_time = True ## We declare that we are going  to use time for the analysis ##
            print ('Using collected time')
        else:
            using_time = False


    elif 'UV'in c_dir.upper():
        print('UV data')
        ## Label the species in the same order that are in the spec_analysis ##
        species = species_UV
        if 'MEDICIONES' in  c_dir.upper():
            t_uv = pd.read_csv(rootcd+diagonal+'UVTime.dat', delim_whitespace = True, header = None)
            t_uv = t_uv.abs()
            using_time = True
            print ('Using collected time')
        else:
            using_time = False


    if using_time == True:
        # print (t_uv)
        t_uv.columns = ['Time'] ## Index  the column as Time ##
        t_exp = t_uv.copy()
        t_exp .columns = ['Time_exp'] ## Add the computer time at the end ##
        t_exp['Time_exp'] = t_exp['Time_exp'].apply(lambda x: x/10000)
        entero = t_uv['Time'].min() ## Use the min data
        print ('Min time used: '+ str(entero))
        # print (t_uv)
        t_uv['Time'] = t_uv['Time'].apply(lambda x: x - entero) ## Set the zero
        # print (t_uv)
        t_uv['Time'] = t_uv['Time'].apply(lambda x: x/10000) ## Divide the numbers in order to use Hours and decimals ##

        ## Label the species in the same order that are in the spec_analysis ##
        framedata.columns = (species)
        framedata.insert (0, 'Time', t_uv) ## Set the column Time in the data frame in the first columns ##
        framedata = framedata.sort_values (by = 'Time')
        framedata ['Time_exp']= t_exp ## Add time exp at the end ##

        maindata = framedata.copy()
        maindata = maindata.drop(['Time_exp'],axis =1)



    else:
        print ('Using file number as time')
        framedata.columns = (species)

        ## Declare the number of data for the X axis ##
        filenumber =  framedata.shape[0]

        xfile = np.arange (filenumber)## Make the vector of file number ##
        ## Add the file number to the Data frame ##
        framedata.insert(loc=0, column='Time', value=xfile)
        maindata = framedata.copy()

else:
    print ('Labwiew data (integral method)')
    framedata = pd.read_csv(c_dir, sep="\t", header= None) ## Read the TXT data.

    species = framedata.iloc[0].values.flatten().tolist() ## Make the first row from the data frame as a list ##

    species[0] = 'Time' ## Name the first data from the list as time ##
    Time = species[0]

    species.pop(0) ## Delete the first item ##

    ## This rutine allows to catch every three index from the list ##
    species = species[::3] ## Conserve in steps of 3 ##

    lines = list(species) ## Save it in a new list ##

    lines.insert (0,Time)

    lines.pop(-1)
    maindata = framedata.iloc[:,::3].copy() ## Select the Areas from the data frame ##
    print(maindata.shape)
    maindata.columns = (lines) ## Index the columns of the areas


    entero = maindata['Time'].min() ## Get the min value of time

    maindata['Time'] = maindata['Time'].apply(lambda x: x - entero) ## Set time to ZERO for the analysis ##

## Averaging data in a window of items ##

def mean_data(a):
    print ("Areas averaged")
    # maindata.columns += "_ave"
    newmaindata = maindata.iloc[:,1:].rolling (a,center= True).mean()
    maindata.iloc[:,1:] = newmaindata
    maindata.fillna(0)
    # newmaindata = maindata.rolling (a,center= True).mean()
    # print (newmaindata)

    print (maindata)


if mean_all_data== True:
    mean_data(average_number)
    title_fig = 'Averaged areas'
else:

    print ("Raw areas")
    title_fig = 'Raw_Areas'
    print (maindata)






## Plotting ##
fig = plt.figure(figsize=(9, 7))
# plt.title(title_fig)
## First Plot, Divide the figure into a 2x1 grid, and give me the first section ##

## All the spectral lines will be ploted as function of time or file number ##
ax = fig.add_subplot(211)


maindata.plot(x=0, ax=ax)

## Create the legend for the plot ##

plt.legend(title=title_fig, loc='upper left', bbox_to_anchor=(1.02, 1.05))
# plt.legend(title=title_fig, loc='upper right', bbox_to_anchor=(0, 1.0), borderaxespad=0)
# plt.legend(title=title_fig, loc='upper right' )
fig.subplots_adjust(right = 0.8)

## Second plot ##

ax2 = fig.add_subplot(212)
maindata.plot(x=0, ax=ax2, legend=False )

####### Button's section #####


def submit(text): ## Enter the text of the min value
    global xminbox
    xminbox = eval(text)

    print (xminbox)


def submit2(text): ## Enter the text of the max value
    global xmaxbox
    xmaxbox = eval(text)

    print (xmaxbox)


def Boxselection (xminbox, xmaxbox):
    print ('The data has been selected')
    ax2.clear()
    maindata_selected = maindata.loc[(maindata['Time'] >= xminbox) & (maindata['Time'] <= xmaxbox)]

    maindata_selected.plot(x=0, ax=ax2, legend=False )


    fig.canvas.draw_idle() ## Redraw the graph ##

    ## Calculate Mean and STD, you can apply any function to...  ##
    maindata_selected1=maindata_selected.drop(['Time'],axis =1)
    meandata = maindata_selected1.mean().copy()

    std_data = maindata_selected1.std().copy()

    analysis_frame = [meandata,std_data]
    analysis_complete = pd.concat(analysis_frame, axis =1)
    analysis_complete.columns =['Mean', 'STD']

    # print (maindata_selected)
    print ('Data mean and std')
    print (analysis_complete)

    ## Origin format, just  to paste ##
    origin = pd.DataFrame(analysis_complete.values.reshape(1,-1))
    print ('origin_format and selected data has been exported to txt')
    print (origin)
    ## Save the selected data ##
    maindata_selected.to_csv('Selected_data.txt', header=True, index=None, sep=' ', mode='w')
    origin.to_csv('origin_format.txt', header=None, index=None, sep=' ', mode='w')

def calling (event):


    Boxselection(xminbox, xmaxbox)

    ## Save the complete data ##
maindata.to_csv('Complete_data.txt', header=True, index=None, sep=' ', mode='w')

axbox1 = plt.axes([0.1, 0.02, 0.1, 0.035]) ## Position of the box and dimensions [x,y,lenght, width]
text_box1 = TextBox(axbox1, 'Min', initial= '')
text_box1.on_submit(submit)

axbox2 = plt.axes([0.3, 0.02, 0.1, 0.035])
text_box2 = TextBox(axbox2, 'Max', initial= '')
text_box2.on_submit(submit2)

axbutton = plt.axes([0.7, 0.02, 0.2, 0.035])
button = Button(axbutton, 'Set')
button.on_clicked(calling)
# fig.tight_layout()
plt.show()
