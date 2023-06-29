import json

from flask import Flask, make_response
import io
# import base64
# import seaborn as sns

import numpy as np      # manipulação numérica
import pandas as pd     # análise e manipulação de dados (https://pandas.pydata.org/docs/#)
from datetime import date, datetime

import matplotlib.pyplot as plt     # visualização de plots


def reportlist():
    reports=["1 - ID:8967","2 - ID:19014090", "3 - ID:9229411", "4 - ID:19748456"]
    return reports

def load_report(rep):
    
    while True:
        if rep=='1':
            with open("c:/Users/analu/OneDrive/Documents/UNI - 3º ANO - 2º SEMESTRE/PROJETO/registos BrainSense/Registos BrainSense 20Feb2023/1. Susete Goncalves/Report_Json_Session_Report_20230220T120426.json") as file:
                data = json.load(file)
            return data
        elif rep=='2':
            with open("c:/Users/analu/OneDrive/Documents/UNI - 3º ANO - 2º SEMESTRE/PROJETO/registos BrainSense/Registos BrainSense 20Feb2023/2. Antonio Castanheira/Report_Json_Session_Report_20230220T120150.json") as file:
                data = json.load(file)
            return data
        elif rep=='3':
            with open("c:/Users/analu/OneDrive/Documents/UNI - 3º ANO - 2º SEMESTRE/PROJETO/registos BrainSense/Registos BrainSense 20Feb2023/3. Adriana Nascimento/Report_Json_Session_Report_20230220T115950.json") as file:
                data = json.load(file)
            return data
        elif rep=='4':
            with open("c:/Users/analu/OneDrive/Documents/UNI - 3º ANO - 2º SEMESTRE/PROJETO/registos BrainSense/Registos BrainSense 13Abr2023/Report_Json_Session_Report_20230413T122752.json") as file:
                data = json.load(file)
            with open ("c:/Users/analu/OneDrive/Documents/UNI - 3º ANO - 2º SEMESTRE/PROJETO/registos BrainSense/Registos BrainSense 13Abr2023/Indefinite Streaming - crise de ausencia -  Report_Json_Session_Report_20230413T123902.json") as file:
                dataInd = json.load(file)
            return data,dataInd



app = Flask(__name__) 


@app.route('/', methods=['GET'])
def links():

    pi = '/patient'; di = '/DeviceInformation'; mris = '/MostRecentInSession'; sc = '/SenseChannel'; ct = '/CalibrationTests'; lmtd = '/LfpMontageTimeDomain'; lm = '/LfpMontage'
    inds = '/IndefiniteStreaming'; bstd = '/BrainSenseTimeDomain'; bs = '/BrainSenseLfp'; es = '/EventSummary'; lfse = '/LfpFrequencySnapshotEvents'

    link = f"To access the different data structures available enter the following directories in the browser:\n- Patient information: {pi}\n- Device information: {di}\n- BrainSense Survey: LFP Montage time domain ({lmtd}) and LFP Montage frequency domain ({lm})\n- BrainSense SetUp: Most Recent In Session ({mris}), Sense Channel tests ({sc}) and Calibration tests ({ct})"
    link_ = f"- BrainSense Survey Recording: Indefinite Streaming ({inds})\n- BrainSense Streaming: Brain Sense time domain ({bstd}) and Brains Sense LFP ({bs})\n- BrainSense Timeline: LFP Trend Logs ()\n- BrainSense Events: LFP Frequency Snapshots ({lfse})"
    return make_response(link+link_)
    

@app.route('/patient', methods=['GET'])
def patient_info(data):

    if "PatientInformation" in data and "Final" in data["PatientInformation"]:
        firstname = data["PatientInformation"]["Final"]["PatientFirstName"]
        lastname = data["PatientInformation"]["Final"]["PatientLastName"]
        patientID = data["PatientInformation"]["Final"]["PatientId"]
        gender = data["PatientInformation"]["Final"]["PatientGender"][17:].lower()
        birth = data["PatientInformation"]["Final"]["PatientDateOfBirth"][0:10].replace("-","/")
        diagnosis = data["PatientInformation"]["Final"]["Diagnosis"][17:]
        #patient = f"{firstname} {lastname} (patient ID: {patientID})"
        patient = [firstname,lastname,patientID,gender,birth,diagnosis]

        #return make_response(patient)
        return patient

    else:
        # return make_response("The file is anonymized.")
        return "The file is anonymized."


@app.route('/DeviceInformation', methods=['GET'])
def device_info(data):

    if "DeviceInformation" in data:
        implante_date = data['DeviceInformation']['Final']['ImplantDate'][0:10].replace("-", "/")
        #MeasureDate = datetime.strptime(MeasureDate, '%Y-%m-%d %H:%M:%S').date()
        stimulator = data['DeviceInformation']['Initial']['Neurostimulator']
        stimulator_model = data['DeviceInformation']['Initial']['NeurostimulatorModel']
        #device = f"The device was implanted in"
        device = [stimulator,stimulator_model, implante_date]

        return device
        #return make_response(device)
    else:
        # return make_response("The file is anonymized.")
        return "There are no specifications on the device."
    

### -------------------------------------------------------------------------------------------------------------------------------------

def setuplist():
    data=["Most Recent in Session","Sense Channel", "Calibration Tests"]
    return data


# MostRecentInSession belong to BrainSense Setup 
@app.route('/MostRecentInSession', methods=['GET'])
def plot_MostRecentInSession(data):

    if ("MostRecentInSessionSignalCheck" in data) & (len(data["MostRecentInSessionSignalCheck"])>0):
        fig, axs = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True, figsize=(10, 5), constrained_layout=True)
        fig.suptitle("MostRecentInSessionSignalCheck", fontsize=15, fontweight='bold')

        for i,ax in enumerate(axs.flatten()):
            
            plt.subplot(1,3,(i+1))

            x_left = data["MostRecentInSessionSignalCheck"][i]["SignalFrequencies"]
            y_left = data["MostRecentInSessionSignalCheck"][i]["SignalPsdValues"]

            if i==0:
                ax.plot(x_left, y_left, color='red', label='Left ANT')
            else:
                ax.plot(x_left, y_left, color='red')


            for j in x_left:
                if j>7:
                    index_left = x_left.index(j)
                    break

            x_left_interval = x_left[index_left:]
            y_left_interval = y_left[index_left:]

            max_left_index_int = np.argmax(y_left_interval)

            peak_x_left = x_left_interval[max_left_index_int]
            peak_y_left = y_left_interval[max_left_index_int]

            ax.scatter(peak_x_left,peak_y_left, marker="o", color="red")

            ax.text(0.95, 0.95, f'Left peak: {peak_x_left} Hz', transform=ax.transAxes,
                    fontsize=7, color="red", verticalalignment='top', horizontalalignment='right')

            x_right = data["MostRecentInSessionSignalCheck"][i+3]["SignalFrequencies"]
            y_right = data["MostRecentInSessionSignalCheck"][i+3]["SignalPsdValues"]

            if i==0:
                ax.plot(x_right, y_right, color='darkred', label='Right ANT')
            else:
                ax.plot(x_right, y_right, color='darkred')

            for k in x_right:
                if k>7:
                    index_right = x_right.index(k)
                    break

            x_right_interval = x_right[index_right:]
            y_right_interval = y_right[index_right:]

            max_right_index_int = np.argmax(y_right_interval)

            peak_x_right = x_right_interval[max_right_index_int]
            peak_y_right = y_right_interval[max_right_index_int]

            ax.scatter(peak_x_right,peak_y_right, marker="o", color="darkred")

            ax.text(0.95, 0.90, f'Right peak: {peak_x_right} Hz', transform=ax.transAxes,
                    fontsize=7, color="darkred", verticalalignment='top', horizontalalignment='right')
        
            plt.ylim(0,2.0)
            plt.title(data["MostRecentInSessionSignalCheck"][i]["Channel"][18:-5], fontsize=7)

        fig.legend()
        fig.supxlabel('Frequency (Hz)', fontsize=9)
        fig.supylabel('Power (dB/Hz)', fontsize=9)

        fig.tight_layout(pad=1.5, w_pad=2.0) 

        # Encode plot as PNG image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # return send_file(img, mimetype='image/png')
        return img

    
    else:
        # return make_response('No Most Recent in Session Signal Check performed')
        return 'No Most Recent in Session Signal Check performed'
    

# Sense Channel Tests belong to BrainSense Setup 
@app.route('/SenseChannel', methods=['GET'])
def plot_SenseChannel(data):

    if ("SenseChannelTests" in data): # & (len(data["SenseChannelTests"])>0):

        cycle = 1
        if len(data["CalibrationTests"])>=7:   # no relatório 3 são feitos 2  sense chaannel tests
            cycle = 2

        senseChannel_time = data["SenseChannelTests"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
        senseChannel_rec = len(data["SenseChannelTests"][0]["TimeDomainData"]) / data["SenseChannelTests"][0]["SampleRateInHz"]     # Calculate the length of the recording
        
        if cycle == 1:
            SCTests = f"One BrainSense Sense Channels Test was performed in the therapy section at {senseChannel_time} during {senseChannel_rec} seconds."
        elif cycle==2:
            senseChannel_time2 = data["SenseChannelTests"][6]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
            senseChannel_rec2 = len(data["SenseChannelTests"][6]["TimeDomainData"]) / data["SenseChannelTests"][6]["SampleRateInHz"]     # Calculate the length of the recording

            SCTests = f"Two BrainSense Sense Channels Tests were performed in the therapy section at {senseChannel_time} during {senseChannel_rec} seconds \n and at {senseChannel_time2} during {senseChannel_rec2} seconds."

        senseCH = [SCTests]

        for i in range(cycle):        
            fig, axs = plt.subplots(1, 3, figsize=(10, 6), constrained_layout=True)
            fig.suptitle("SenseChannelTests", fontsize=15, fontweight='bold')

            for i in range(3):
                
                plt.subplot(1,3,(i+1))
                plt.plot(data["SenseChannelTests"][i]["TimeDomainData"], color='red')
                plt.plot(data["SenseChannelTests"][i+3]["TimeDomainData"], color='darkred')

                plt.title(data["SenseChannelTests"][i]["Channel"][0:-5], fontsize=9)
                ## estes limites aproximam estes gráficos aos do Use Cases (pág 5)
                plt.ylim(-50,50)

            fig.legend(['Left ANT','Right ANT'])
            fig.supxlabel('Time', fontsize=9)
            fig.supylabel('LFP Magnitude (uVp)', fontsize=9)
            fig.tight_layout(w_pad=1.5)

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            senseCH.append(img)


        return senseCH
    
    else:
        # return make_response('No Sense Channel Tests performed')
        return 'No Sense Channel Tests performed'

# Calibration Tests also belong to BrainSense Setup 
@app.route('/CalibrationTests', methods=['GET'])
def plot_CalibrationTests(data):

    if ("CalibrationTests" in data): # & (len(data["CalibrationTests"])>0):
        
        cycle = 1
        if len(data["CalibrationTests"])>4:   # no relatório 3 são feitos 2  calibration tests
            cycle = 2


        calibrationTests_time = data["CalibrationTests"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
        calibrationTests_rec = len(data["CalibrationTests"][0]["TimeDomainData"]) / data["CalibrationTests"][0]["SampleRateInHz"]     # Calculate the length of the recording 

        if cycle == 1:
            calibrationTests = f"One BrainSense Setup Calibration Test was performed in the therapy section at {calibrationTests_time} during {calibrationTests_rec} seconds."
        elif cycle==2:
            calibrationTests_time2 = data["SenseChannelTests"][6]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
            calibrationTests_rec2 = len(data["SenseChannelTests"][6]["TimeDomainData"]) / data["SenseChannelTests"][6]["SampleRateInHz"]     # Calculate the length of the recording

            calibrationTests = f"Two BrainSense Setup Calibration Test were performed in the therapy section at {calibrationTests_time} during {calibrationTests_rec} seconds \n and at {calibrationTests_time2} during {calibrationTests_rec2} seconds."

        calib = [calibrationTests]

        for i in range(cycle):        
            fig, axs = plt.subplots(1, 2, constrained_layout=True)
            fig.suptitle("CalibrationTests", fontsize=15, fontweight='bold')

            for i in range(0,3,2):
                
                subplot = [1,"erro",2]
                plt.subplot(1,2,subplot[i])
                plt.plot(data["SenseChannelTests"][i]["TimeDomainData"], color='red')
                plt.plot(data["SenseChannelTests"][i+3]["TimeDomainData"], color='darkred')

                plt.title(data["SenseChannelTests"][i]["Channel"][0:-5], fontsize=9)
                ## estes limites aproximam estes gráficos aos do Use Cases (pág 5)
                plt.xlim(0,1000)
                plt.ylim(-60,60)

            fig.legend(['Left ANT','Right ANT'])
            fig.supxlabel('Time', fontsize=9)
            fig.supylabel('LFP Magnitude (uVp)', fontsize=9)
            fig.tight_layout(w_pad=1.5)


        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        calib.append(img)

        
        # return send_file(img, mimetype='image/png') #, make_response(senseChannel_time)
        return calib
    
    else:
        # return make_response('No Calibration Tests performed')
        return 'No Calibration Tests performed'


### -------------------------------------------------------------------------------------------------------------------------------------

def surveylist():
    data=["LFP Montage (time domain)","LFP Montage (frequency domain)", "Indefinite Streaming (time domain)"]
    return data


# LFP Montage (time domain) belongs to BrainSense Survey
@app.route('/LfpMontageTimeDomain', methods=['GET'])
def plot_LfpMontageTimeDomain(data,lead):

    if ("LfpMontageTimeDomain" in data):  #(len(data["LfpMontageTimeDomain"])>0):
        if (len(data["LfpMontageTimeDomain"])>0):

            if lead=="2":
                nrows=5; ncols=3; figx=11; figy=10; rang=15
            else:
                nrows=2; ncols=3; figx=10; figy=8; rang=6
        
            fig, axs = plt.subplots(nrows, ncols, sharex=True, sharey=True, figsize=(figx, figy), constrained_layout=True)    # Constrained layout attempts to resize subplots in a figure so that there are no overlaps between axes objects and labels on the axes.

            fig.suptitle("LFP Montage (time domain)", fontsize=15, fontweight='bold')   

            for i in range(rang):
                
                plt.subplot(nrows,ncols,(i+1))
                plt.plot(data["LfpMontageTimeDomain"][i]["TimeDomainData"], color='red')
                plt.plot(data["LfpMontageTimeDomain"][i+rang]["TimeDomainData"], color='darkred')
                
                #plt.ylim(0,1.5)
                plt.title(data["LfpMontageTimeDomain"][i]["Channel"], fontsize=7)

            fig.legend(['Left ANT','Right ANT'])
            fig.supxlabel('Time', fontsize=9)
            fig.supylabel('LFP Magnitude (uVp)', fontsize=9)

            fig.tight_layout(pad=1.5)

            LfpMontageTD_itime = data["LfpMontageTimeDomain"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
            LfpMontageTD_ftime = data["LfpMontageTimeDomain"][-1]["FirstPacketDateTime"][0:19].replace("T", " ") 
            LfpMontageTD_rec = len(data["LfpMontageTimeDomain"][0]["TimeDomainData"]) / data["LfpMontageTimeDomain"][0]["SampleRateInHz"]   # Calculate the length of the recording
            LfpMontageTD_ = f"BrainSense Survey LFP measurement performed between {LfpMontageTD_itime} and {LfpMontageTD_ftime}, during {LfpMontageTD_rec} seconds."        
            
            LfpMontageTD = [LfpMontageTD_]

            # Encode plot as PNG image
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            LfpMontageTD.append(img)

            # return send_file(img, mimetype='image/png') #, make_response(senseChannel_time)
            return LfpMontageTD
        
        else:
        # return make_response('No Lfp Montage Time Domain measurement performed')
            return 'No Lfp Montage Time Domain measurement performed'
    else:
        # return make_response('No Lfp Montage Time Domain measurement performed')
        return 'No Lfp Montage Time Domain measurement performed'
    
    

# LFP Montage (frequency domain) belongs to BrainSense Survey
@app.route('/LfpMontage', methods=['GET'])
def plot_LfpMontage(data,lead):

    if "LFPMontage" in data: #| (len(data["LFPMontage"])>0):
        if len(data["LFPMontage"])>0:

            if lead=="2":
                nrows=5; ncols=3; rang=15
            else:
                nrows=2; ncols=3; rang=6

            fig, axs = plt.subplots(nrows, ncols, sharex=True, sharey=True, figsize=(12, 8), constrained_layout=True)    # Constrained layout attempts to resize subplots in a figure so that there are no overlaps between axes objects and labels on the axes.

            fig.suptitle("LFP Montage", fontsize=15, fontweight='bold')   

            for i,ax in enumerate(axs.flatten()):
                
                plt.subplot(nrows,ncols,(i+1))

                x_left = data["LFPMontage"][i]["LFPFrequency"]
                y_left = data["LFPMontage"][i]["LFPMagnitude"]

                if i==0:
                    ax.plot(x_left, y_left, color='red', label='Left ANT')
                else:
                    ax.plot(x_left, y_left, color='red')

                for j in x_left:
                    if j>7:
                        index_left = x_left.index(j)
                        break

                x_left_interval = x_left[index_left:]
                y_left_interval = y_left[index_left:]

                max_left_index_int = np.argmax(y_left_interval)

                peak_x_left = x_left_interval[max_left_index_int]
                peak_y_left = y_left_interval[max_left_index_int]

                ax.scatter(peak_x_left ,peak_y_left, marker="o", color="red")

                ax.text(0.95, 0.95, f'Left peak: {peak_x_left} Hz', transform=ax.transAxes,
                        fontsize=7, color="red", verticalalignment='top', horizontalalignment='right')

                x_right = data["LFPMontage"][i+rang]["LFPFrequency"]
                y_right = data["LFPMontage"][i+rang]["LFPMagnitude"]

                if i==0:
                    ax.plot(x_right, y_right, color='darkred', label='Right ANT')
                else:
                    ax.plot(x_right, y_right, color='darkred')

                for k in x_right:
                    if k>7:
                        index_right = x_right.index(k)
                        break

                x_right_interval = x_right[index_right:]
                y_right_interval = y_right[index_right:]

                max_right_index_int = np.argmax(y_right_interval)

                peak_x_right = x_right_interval[max_right_index_int]
                peak_y_right = y_right_interval[max_right_index_int]

                ax.scatter(peak_x_right,peak_y_right, marker="o", color="darkred")

                ax.text(0.95, 0.90, f'Right peak: {peak_x_right} Hz', transform=ax.transAxes,
            fontsize=7, color="darkred", verticalalignment='top', horizontalalignment='right')
                
                plt.ylim(0,1.5)
                plt.title(data["LFPMontage"][i]["SensingElectrodes"][26:], fontsize=7)


            fig.legend()
            fig.supxlabel('LFP Frequency (Hz)', fontsize=9)
            fig.supylabel('LFP Magnitude (uVp)', fontsize=9)

            fig.tight_layout(pad=1.5)  

            # Encode plot as PNG image
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # return send_file(img, mimetype='image/png') #, make_response(senseChannel_time)
            return img
        
        else:
            # return make_response('No Lfp Montage measurement performed')
            return 'No Lfp Montage measurement performed'
        
    else:
        # return make_response('No Lfp Montage measurement performed')
        return 'No Lfp Montage measurement performed'


# Indefinite Streaming (time domain) belongs to BrainSense Survey Recording
@app.route('/IndefiniteStreaming', methods=['GET'])
def plot_IndefiniteStreaming(data):

    if ("IndefiniteStreaming" in data): # & (len(data["IndefiniteStreaming"])>0):
        
        fig, axs = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True, figsize=(10, 6), constrained_layout=True)    # Constrained layout attempts to resize subplots in a figure so that there are no overlaps between axes objects and labels on the axes.

        fig.suptitle("Indefinite Streaming", fontsize=15, fontweight='bold')   

        for i in range(3):
            
            plt.subplot(1,3,(i+1))
            plt.plot(data["IndefiniteStreaming"][i]["TimeDomainData"], color='red')
            plt.plot(data["IndefiniteStreaming"][i+3]["TimeDomainData"], color='darkred')
            
            plt.title(data["IndefiniteStreaming"][i]["Channel"][0:-5], fontsize=7)


        fig.legend(['Left ANT','Right ANT'])
        fig.supxlabel('Time', fontsize=9)
        fig.supylabel('LFP Magnitude (uVp)', fontsize=9)

        fig.tight_layout(pad=1.5)

        indefiniteStreaming_time = data["IndefiniteStreaming"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
        indefiniteStreaming_rec = len(data["IndefiniteStreaming"][0]["TimeDomainData"]) / data["IndefiniteStreaming"][0]["SampleRateInHz"]     # Calculate the length of the recording 
        indefiniteStreaming_ = f"BrainSense Survey Indefinite Streaming performed at {indefiniteStreaming_time} during {indefiniteStreaming_rec} seconds."
        
        indefiniteStreaming = [indefiniteStreaming_]

        # Encode plot as PNG image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        indefiniteStreaming.append(img)

        # return send_file(img, mimetype='image/png') #, make_response(senseChannel_time)
        return indefiniteStreaming
    
    else:
        # return make_response('No Indefinite Streaming measurement performed')
        return 'No Indefinite Streaming measurement performed'


### -------------------------------------------------------------------------------------------------------------------------------------

def streaminglist():
    data=["Brain Sense (time domain)","Brains Sense LFP"]
    return data


# Brain Sense (time domain) belongs to BrainSense Streaming 
@app.route('/BrainSenseTimeDomain', methods=['GET'])
def plot_BrainSenseTD(data):

    if "BrainSenseTimeDomain" in data:
        if len(data["BrainSenseTimeDomain"])>0:

            plt.suptitle("Brain Sense", fontsize=15, fontweight='bold')   

            plt.plot(data["BrainSenseTimeDomain"][0]["TimeDomainData"], color='red')
            plt.plot(data["BrainSenseTimeDomain"][1]["TimeDomainData"], color='darkred')
            
                #plt.ylim(0,1.5)
            plt.title(data["BrainSenseTimeDomain"][0]["Channel"][0:-5], fontsize=7)

            plt.legend(['Left ANT','Right ANT'])
            plt.xlabel('Time', fontsize=9)
            plt.ylabel('LFP Magnitude (uVp)', fontsize=9)

            plt.tight_layout(pad=1.5)
            fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(8, 6), constrained_layout=True)    # Constrained layout attempts to resize subplots in a figure so that there are no overlaps between axes objects and labels on the axes.

            fig.suptitle("Brain Sense (time domain)", fontsize=15, fontweight='bold')   

            for i in range(2):
                
                plt.subplot(1,2,(i+1))
                plt.plot(data["BrainSenseTimeDomain"][i]["TimeDomainData"], color='red')
                
                #plt.ylim(0,1.5)
                plt.title(data["BrainSenseTimeDomain"][i]["Channel"], fontsize=7)


            fig.supxlabel('Time', fontsize=9)
            fig.supylabel('LFP Magnitude (uVp)', fontsize=9)

            fig.tight_layout(pad=1.5)

            brainSenseTD_time = data["BrainSenseTimeDomain"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
            brainSenseTD_rec = len(data["BrainSenseTimeDomain"][0]["TimeDomainData"]) / data["BrainSenseTimeDomain"][0]["SampleRateInHz"]     # Calculate the length of the recording 
            brainSenseTD_ = f"BrainSense Streaming Brain Sense Time Domain performed at {brainSenseTD_time} during {brainSenseTD_rec} seconds."
            
            brainSenseTD = [brainSenseTD_]

            # Encode plot as PNG image
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            brainSenseTD.append(img)
            # return send_file(img, mimetype='image/png') #, make_response(senseChannel_time)
            return brainSenseTD
        
        else:
            # return make_response('No Brain Sense Time Domain measurement performed')
            return 'No Brain Sense Time Domain measurement performed'

    else:
        # return make_response('No Brain Sense Time Domain measurement performed')
        return 'No Brain Sense Time Domain measurement performed'



# Brains Sense LFP (power? domain) belongs to BrainSense Streaming
@app.route('/BrainSenseLfp', methods=['GET'])
def plot_BrainSenseLfp(data):

    if "BrainSenseLfp" in data:
        if len(data["BrainSenseLfp"])>0:
            y_dataLFP_R = []; y_datamA_R = []; y_dataLFP_L = []; y_datamA_L = []

            for i in data["BrainSenseLfp"][0]["LfpData"]:
                y_dataLFP_R.append(i["Right"]["LFP"])
                y_dataLFP_L.append(i["Left"]["LFP"])
                y_datamA_R.append(i["Right"]["mA"])
                y_datamA_L.append(i["Left"]["mA"])

            fig, (ax1,ax2) = plt.subplots(1,2, sharex=True, sharey=True, figsize=(10, 6))
            fig.suptitle("Brain Sense LFP", fontsize=15, fontweight='bold')   
            fig.supxlabel('Time', fontsize=9)

            color = 'tab:red'
            ax1.set_title('Brain Sense LFP Left')
            ax1.set_ylabel('LFP Frequency (Hz)', fontsize=9, color=color)
            ax1.plot(y_dataLFP_L, color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax3 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'tab:blue'
            ax3.set_ylabel('STIM Amplitude (mA)', color=color)  # we already handled the x-label with ax1
            ax3.plot(y_datamA_L, color=color)
            ax3.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()

            color = 'tab:red'
            ax2.set_title('Brain Sense LFP Right')
            ax2.set_ylabel('LFP Frequency (Hz)', fontsize=9, color=color)
            ax2.plot(y_dataLFP_R, color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            ax4 = ax2.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'tab:blue'
            ax4.set_ylabel('STIM Amplitude (mA)', color=color)  # we already handled the x-label with ax1
            ax4.plot(y_datamA_R, color=color)
            ax4.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()

            brainSense_time = data["BrainSenseLfp"][0]["FirstPacketDateTime"][0:19].replace("T", " ")        # Select datetime
            brainSense_ = f"BrainSense Streaming Brain Sense Time Domain performed at {brainSense_time}."
            
            brainSense = [brainSense_]
            # Encode plot as PNG image
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            brainSense.append(img)

            # return send_file(img, mimetype='image/png') #, make_response(senseChannel_time)
            return brainSense
        
        else:
            # return make_response('No Brain Sense LFP measurement performed')
            return 'No Brain Sense LFP measurement performed'
    
    else:
        # return make_response('No Brain Sense LFP measurement performed')
        return 'No Brain Sense LFP measurement performed'


### -------------------------------------------------------------------------------------------------------------------------------------

def timelinelist():
    data=["LFP Trend Logs"]
    return data


# Event Summary (not a graphic) belongs to BrainSense Timeline/Events
@app.route('/EventSummary', methods=['GET'])
def plot_EventSummary(data):

    if "EventSummary" in data:
        if len(data["EventSummary"])>0:

            eventSummary_start = data["EventSummary"]["SessionStartDate"][0:19].replace("T", " ")        # Select the start of the session
            eventSummary_end = data["EventSummary"]["SessionEndDate"][0:19].replace("T", " ")            # Select the end of the session
            eventSummary_dateStart = date(int(eventSummary_start[0:4]), int(eventSummary_start[5:7]), int(eventSummary_start[8:10]))
            eventSummary_dateEnd = date(int(eventSummary_end[0:4]), int(eventSummary_end[5:7]), int(eventSummary_end[8:10]))
            eventSummary_delta = eventSummary_dateEnd - eventSummary_dateStart
            eventSummary_days = eventSummary_delta.days
            eventSummary = f"EventSummary for timeline started at {eventSummary_start} and ended at {eventSummary_end} (Total of {eventSummary_days} days)"

            return make_response(eventSummary)
        
        else:
            return make_response('No Event Summary available.')
    
    else:
        return make_response('No Event Summary available.')
    
# LFP Trend Logs () belongs to BrainSense Timeline
@app.route('/LfpTrendLogs', methods=['GET'])
def plot_LfpTrendLogs(data):

    if "DiagnosticData" in data and "LFPTrendLogs" in data["DiagnosticData"]:
        if len(data["DiagnosticData"]["LFPTrendLogs"])>0:
            
            trend = []
            date_set = []

            plt.clf()

            for date in data["DiagnosticData"]["LFPTrendLogs"]["HemisphereLocationDef.Left"]:
                y_dataLFP_R = []; y_datamA_R = []; y_dataLFP_L = []; y_datamA_L = []

                date_set.append(date[:10])

                for i in range (0,len(data["DiagnosticData"]["LFPTrendLogs"]["HemisphereLocationDef.Left"][date])):
                    y_dataLFP_R.append(data["DiagnosticData"]["LFPTrendLogs"]["HemisphereLocationDef.Right"][date][i]["LFP"])
                    y_dataLFP_L.append(data["DiagnosticData"]["LFPTrendLogs"]["HemisphereLocationDef.Left"][date][i]["LFP"])
                    y_datamA_R.append(data["DiagnosticData"]["LFPTrendLogs"]["HemisphereLocationDef.Right"][date][i]["AmplitudeInMilliAmps"])
                    y_datamA_L.append(data["DiagnosticData"]["LFPTrendLogs"]["HemisphereLocationDef.Left"][date][i]["AmplitudeInMilliAmps"])

                fig, (ax1,ax2) = plt.subplots(1,2, sharex=True, sharey=True, figsize=(10, 6))
                fig.suptitle("LFP Trend Logs", fontsize=15, fontweight='bold')   
                fig.supxlabel('Time', fontsize=9)

                color = 'tab:red'
                ax1.set_title('LFP Trend Logs Left')
                ax1.set_ylabel('LFP Frequency (Hz)', fontsize=9, color=color)
                # ax1.plot(y_dataLFP_L, color=color)
                ax1.scatter(range(len(y_dataLFP_L)), y_dataLFP_L, marker='s', color=color)
                ax1.tick_params(axis='y', labelcolor=color)

                ax3 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

                color = 'tab:blue'
                ax3.set_ylabel('STIM Amplitude (mA)', color=color)  # we already handled the x-label with ax1
                ax3.plot(y_datamA_L, color=color)
                ax3.tick_params(axis='y', labelcolor=color)

                fig.tight_layout()

                color = 'tab:red'
                ax2.set_title('LFP Trend Logs Right')
                ax2.set_ylabel('LFP Frequency (Hz)', fontsize=9, color=color)
                # ax2.plot(y_dataLFP_R, color=color)
                ax2.scatter(range(len(y_dataLFP_R)), y_dataLFP_R, marker='s', color=color)
                ax2.tick_params(axis='y', labelcolor=color)

                ax4 = ax2.twinx()  # instantiate a second axes that shares the same x-axis

                color = 'tab:blue'
                ax4.set_ylabel('STIM Amplitude (mA)', color=color)  # we already handled the x-label with ax1
                ax4.plot(y_datamA_R, color=color)
                ax4.tick_params(axis='y', labelcolor=color)

                fig.tight_layout()
                
                # Encode plot as PNG image
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)

                trend.append(img)

                plt.clf()

            
            trend.append(date_set)

            LFPTrendLogs = f"The data was recorded for {len(date_set)} days."

            trend.append(LFPTrendLogs)

            return trend
        
        else:
            return 'No LFP Trend Logs available.'
    
    else:
        return 'No LFP Trend Logs available.'
    

### -------------------------------------------------------------------------------------------------------------------------------------

def eventslist():
    data=["LFP Frequency Snapshot Events"]
    return data


# LFP Frequency Snapshot Events (not a graphic) belongs to BrainSense Timeline/Events
@app.route('/LfpFrequencySnapshotEvents', methods=['GET'])
def plot_LfpFrequencySnapshotEvents(data):

    if "DiagnosticData" in data and "LfpFrequencySnapshotEvents" in data["DiagnosticData"]:

        events=[]
        event_names = []

        plt.clf()

        for i in range(len(data["DiagnosticData"]["LfpFrequencySnapshotEvents"])):
    
            if "LfpFrequencySnapshotEvents" in data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]:
                # fig, axs = plt.subplots(1, 2, constrained_layout=True)
                # fig.suptitle(data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["EventName"], fontsize=15, fontweight='bold')
                plt.title(data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["EventName"], fontsize=15, fontweight='bold')
                event_names.append(data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["EventName"])

                plt.plot(data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["LfpFrequencySnapshotEvents"]["HemisphereLocationDef.Left"]["Frequency"],data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["LfpFrequencySnapshotEvents"]["HemisphereLocationDef.Left"]["FFTBinData"], color='red')
                plt.plot(data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["LfpFrequencySnapshotEvents"]["HemisphereLocationDef.Right"]["Frequency"],data["DiagnosticData"]["LfpFrequencySnapshotEvents"][i]["LfpFrequencySnapshotEvents"]["HemisphereLocationDef.Right"]["FFTBinData"], color='darkred')
                plt.legend(['Left ANT','Right ANT'])
                plt.xlabel('Frquency (Hz)',fontsize=7)
                plt.ylabel('FFTBinData (uVp)',fontsize=7)

                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)

                events.append(img)

                plt.clf()

        events.append(event_names)

        n_events = len(data["DiagnosticData"]["LfpFrequencySnapshotEvents"])        # gives the number of events registered by the patient
        LfpFrequencySnapshotEvents = f"There were {n_events} events registered by the patient, from which {len(event_names)} were recorded by the device. "

        events.append(LfpFrequencySnapshotEvents)

        return events
    
    else:
        return 'No events registered by patient.'



if __name__ == '__main__':
    # cria o endereço http://localhost:5000
    app.run(port=5000,host='localhost',debug=True)




