import customtkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import api
  
### SYSTEM SETTINGS
tk.set_appearance_mode("System") 
tk.set_default_color_theme("blue")  


class App(tk.CTk):      # inicilização da app
    
    def __init__(self, fg_color: str | None = None, **kwargs): 
        super().__init__(fg_color, **kwargs)

        ### APP FRAME
        self.geometry("980x780")     # size
        self.title("DBS Medtronic graphic displayer")
        self.configure(background="#c75d55")

        self.search = Image.open("search-icon-png-9993.png")
        self.search_image = tk.CTkImage(self.search, size=(12,12))

        self.patient_frame = tk.CTkFrame(self,width=700, fg_color="#DEDEDE")
        self.patient_frame.pack(pady=10, padx=30, fill="both", expand=False)

        self.subpatient_frame = tk.CTkFrame(master=self.patient_frame, fg_color="#DEDEDE")
        self.subpatient_frame.grid(row=0, column=0, sticky="n")

        self.patient_frame.rowconfigure(0, weight=1)
        self.patient_frame.columnconfigure(0, weight=1)


        self.insert_report = tk.CTkLabel(master=self.subpatient_frame, text = 'Choose the patient report you want to analyse: ', font=("Arial", 13))
        self.insert_report.grid(row=0, column=0, padx=5, sticky="ew")

        self.data = tk.StringVar() 
        self.data = api.load_report("1")
        print(self.data["PatientInformation"]["Final"]["PatientFirstName"])
        self.data_structure = "Most Recent in Session"

        self.var = tk.StringVar(value="Select a report")
        self.var.trace("w", self.on_option_changed)       
        self.report = tk.CTkOptionMenu(self.subpatient_frame, variable=self.var, text_color="grey", width=380, height=20, fg_color="#ECECEC", button_color="#c75d55", button_hover_color="grey", dropdown_hover_color="#ECECEC", values=api.reportlist())
        self.report.grid(row=0, column=1, pady=10, sticky="ew")

        self.search_report = tk.CTkButton(master=self.subpatient_frame, image=self.search_image, compound="left", text="",width=10, height=20, hover=True, hover_color="grey", fg_color="#c75d55", command=self.createText) 
        self.search_report.grid(row=0, column=2, padx=3, pady=5, sticky="ew")

        self.display_patient = tk.CTkFrame(master=self.patient_frame, width=40, height=100, fg_color="#DEDEDE") 
        self.display_patient.grid(row=1, column=0, columnspan=3, padx=5, pady=3)
        
        
        self.data_frame = tk.CTkFrame(self, fg_color="#DEDEDE")
        self.data_frame.pack(pady=10, padx=30, fill="both", expand=True)

        self.brainSense = tk.CTkFrame(master=self.data_frame, width=200, fg_color="#DEDEDE")
        self.brainSense.grid(row=0, column=0, sticky="n")

        self.chose_data = tk.CTkFrame(master=self.data_frame, fg_color="#DEDEDE")
        self.chose_data.grid(row=0, column=1, sticky="n", padx=10)

        self.display_data = tk.CTkFrame(master=self.chose_data, fg_color="#ECECEC") 

        self.data_frame.rowconfigure(0, weight=1)
        self.data_frame.columnconfigure(1, weight=1)

        self.insert_data = tk.CTkLabel(master=self.brainSense, text = 'Choose a BrainSense feature: ', font=("Arial", 13), fg_color="#DEDEDE")
        self.insert_data.grid(row=0, column=0, padx=6, pady = 2, sticky="ns") 

        self.BSsurvey = tk.CTkButton(master=self.brainSense, text="BrainSense Survey", width=180, font=("Arial", 12), hover=True, hover_color="grey", fg_color="#c75d55", command=self.createBSsurevy) 
        self.BSsurvey.grid(row=1,column=0, padx=5, pady = 2, sticky="nsw")

        self.BSsetup = tk.CTkButton(master=self.brainSense, text="BrainSense Setup", width=180, font=("Arial", 12), hover=True, hover_color="grey", fg_color="#c75d55", command=self.createBSsetup) 
        self.BSsetup.grid(row=2,column=0, padx=5, pady = 2, sticky="nsw")

        self.BSstreaming = tk.CTkButton(master=self.brainSense, text="BrainSense Streaming", width=180, font=("Arial", 12), hover=True, hover_color="grey", fg_color="#c75d55", command=self.createBSstreaming)
        self.BSstreaming.grid(row=3,column=0, padx=5, pady = 2, sticky="nsw")

        self.BStimeline = tk.CTkButton(master=self.brainSense, text="BrainSense Timeline", width=180, font=("Arial", 12), hover=True, hover_color="grey", fg_color="#c75d55", command=self.createBStimeline)
        self.BStimeline.grid(row=4,column=0, padx=5, pady = 2, sticky="nsw")

        self.BSevents = tk.CTkButton(master=self.brainSense, text="BrainSense Events", width=180, font=("Arial", 12), hover=True, hover_color="grey", fg_color="#c75d55", command=self.createBSevents)
        self.BSevents.grid(row=5,column=0, padx=5, pady = 2, sticky="nsw")        
 
  
    
    def on_option_changed(self, *args):

        self.selected_option = self.var.get()
        
        if self.selected_option[0]=="4":
            self.data = api.load_report(self.selected_option[0])[0]
            self.dataInd = api.load_report(self.selected_option[0])[1]
        else:
            self.data = api.load_report(self.selected_option[0])

        #self.createText(data)

        #self.on_data_changed(data)
        #self.createBSsurevy(data)
    

    def createText(self): 
        # PATIENT DATA

        # limpa os dados anteriores cada vez que se carrega no botão search
        for widget in self.display_patient.winfo_children():
            widget.destroy()

        textP = tk.CTkLabel(self.display_patient, text="Patient information",font=("Arial", 14, "bold"), width=300, anchor="center")
        textP.grid(row=0, column=0, padx=5)

        patient = api.patient_info(self.data)

        gender_str = "Gender: " + patient[3]
        gender = tk.CTkLabel(self.display_patient, text=gender_str, font=("Arial", 12), width=300, anchor="center")
        gender.grid(row=1, column=0)

        birth_str = "Date of birth: " + patient[4]
        birth = tk.CTkLabel(self.display_patient, text=birth_str, font=("Arial", 12), width=300, anchor="center")
        birth.grid(row=2, column=0)

        diag_str = "Diagnosis: " + patient[5]
        diag = tk.CTkLabel(self.display_patient, text=diag_str, font=("Arial", 12), width=300, anchor="center")
        diag.grid(row=3, column=0)


        textD = tk.CTkLabel(self.display_patient, text="Device information",font=("Arial", 14, "bold"), width=300, anchor="center")
        textD.grid(row=0, column=1, padx=5)

        device = api.device_info(self.data)

        neuro_str = "Neurostimulator type: " + device[0]
        neuro = tk.CTkLabel(self.display_patient, text=neuro_str, font=("Arial", 12), width=300, anchor="center")
        neuro.grid(row=1, column=1)

        model_str = "Neurostimulator model: " + device[1]
        model = tk.CTkLabel(self.display_patient, text=model_str, font=("Arial", 12), width=300, anchor="center")
        model.grid(row=2, column=1)

        impl_str = "Implant date: " + device[2]
        impl = tk.CTkLabel(self.display_patient, text=impl_str, font=("Arial", 12), width=300, anchor="center")
        impl.grid(row=3, column=1)

    
    

    def createBSsurevy(self):
        
        # limpa os dados anteriores cada vez que se carrega no botão search
        for widget in self.chose_data.winfo_children():
            widget.destroy()
        
        self.BSsurvey.configure(font=('Arial', 14,'bold'), fg_color="#B3443B")
        self.BSsetup.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSstreaming.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BStimeline.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSevents.configure(font=('Arial', 12), fg_color="#c75d55")

        self.textBS = tk.CTkLabel(self.chose_data, text="BrainSense Survey",font=("Arial", 14, "bold"), text_color="#c75d55", width=300)
        self.textBS.grid(row=0, column=0, columnspan=2, sticky="n", padx=5)

        self.var_data = tk.StringVar(value="Select a data structure")    
        self.var_data.trace("w", self.on_data_changed)      
        self.datas = tk.CTkOptionMenu(self.chose_data, variable=self.var_data, text_color="grey", width=500, height=20, fg_color="#ECECEC", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=api.surveylist())
        self.datas.grid(row=1, column=0, sticky="ne", pady=1)

        self.search_report = tk.CTkButton(master=self.chose_data, image=self.search_image, compound="left", text="",width=10, height=20, hover=True, hover_color="grey", fg_color="#c75d55", command=self.createGraphic) 
        self.search_report.grid(row=1, column=1, padx=2, pady=1, sticky="nw")

    
    def createBSsetup(self):
        
        for widget in self.chose_data.winfo_children():
            widget.destroy()
        
        self.BSsurvey.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSsetup.configure(font=('Arial', 14,'bold'), fg_color="#B3443B")
        self.BSstreaming.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BStimeline.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSevents.configure(font=('Arial', 12), fg_color="#c75d55")

        self.textBS = tk.CTkLabel(self.chose_data, text="BrainSense Setup",font=("Arial", 14, "bold"), text_color="#c75d55", width=300)
        self.textBS.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5)

        self.var_data = tk.StringVar(value="Select a data structure")   
        self.var_data.trace("w", self.on_data_changed)       
        self.datas = tk.CTkOptionMenu(self.chose_data, variable=self.var_data, text_color="grey", width=500, height=20, fg_color="#ECECEC", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=api.setuplist())
        self.datas.grid(row=1, column=0, sticky="ne", pady=1)

        self.search_report = tk.CTkButton(master=self.chose_data, image=self.search_image, compound="left", text="",width=10, height=20, hover=True, hover_color="grey", fg_color="#c75d55", command=self.createGraphic) 
        self.search_report.grid(row=1, column=1, padx=2, pady=1, sticky="nw")  



    def createBSstreaming(self):

        for widget in self.chose_data.winfo_children():
            widget.destroy()

        self.BSsurvey.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSsetup.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSstreaming.configure(font=('Arial', 14,'bold'), fg_color="#B3443B")
        self.BStimeline.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSevents.configure(font=('Arial', 12), fg_color="#c75d55")

        self.textBS = tk.CTkLabel(self.chose_data, text="BrainSense Streaming",font=("Arial", 14, "bold"), text_color="#c75d55", width=300)
        self.textBS.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5)

        self.var_data = tk.StringVar(value="Select a data structure")   
        self.var_data.trace("w", self.on_data_changed)       
        self.datas = tk.CTkOptionMenu(self.chose_data, variable=self.var_data, text_color="grey", width=500, height=20, fg_color="#ECECEC", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=api.streaminglist())
        self.datas.grid(row=1, column=0, sticky="ne", pady=1)

        self.search_report = tk.CTkButton(master=self.chose_data, image=self.search_image, compound="left", text="",width=10, height=20, hover=True, hover_color="grey", fg_color="#c75d55", command=self.createGraphic) 
        self.search_report.grid(row=1, column=1, padx=2, pady=1, sticky="nw")  


    def createBStimeline(self):       

        for widget in self.chose_data.winfo_children():
            widget.destroy()

        self.BSsurvey.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSsetup.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSstreaming.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BStimeline.configure(font=('Arial', 14,'bold'), fg_color="#B3443B")
        self.BSevents.configure(font=('Arial', 12), fg_color="#c75d55")

        self.textBS = tk.CTkLabel(self.chose_data, text="BrainSense Timeline",font=("Arial", 14, "bold"), text_color="#c75d55", width=300)
        self.textBS.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5)

        self.var_data = tk.StringVar(value="Select a data structure")   
        self.var_data.trace("w", self.on_data_changed)       
        self.datas = tk.CTkOptionMenu(self.chose_data, variable=self.var_data, text_color="grey", width=500, height=20, fg_color="#ECECEC", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=api.timelinelist())
        self.datas.grid(row=1, column=0, sticky="ne", pady=1)

        self.search_report = tk.CTkButton(master=self.chose_data, image=self.search_image, compound="left", text="",width=10, height=20, hover=True, hover_color="grey", fg_color="#c75d55", command=self.createGraphic) 
        self.search_report.grid(row=1, column=1, padx=2, pady=1, sticky="nw")  

    
    def createBSevents(self):       

        for widget in self.chose_data.winfo_children():
            widget.destroy()

        self.BSsurvey.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSsetup.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSstreaming.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BStimeline.configure(font=('Arial', 12), fg_color="#c75d55")
        self.BSevents.configure(font=('Arial', 14,'bold'), fg_color="#B3443B")

        self.textBS = tk.CTkLabel(self.chose_data, text="BrainSense Events",font=("Arial", 14, "bold"), text_color="#c75d55", width=300)
        self.textBS.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5)

        self.var_data = tk.StringVar(value="Select a data structure")   
        self.var_data.trace("w", self.on_data_changed)       
        self.datas = tk.CTkOptionMenu(self.chose_data, variable=self.var_data, text_color="grey", width=500, height=20, fg_color="#ECECEC", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=api.eventslist())
        self.datas.grid(row=1, column=0, sticky="ne", pady=1)

        self.search_report = tk.CTkButton(master=self.chose_data, image=self.search_image, compound="left", text="",width=10, height=20, hover=True, hover_color="grey", fg_color="#c75d55", command=self.createGraphic) 
        self.search_report.grid(row=1, column=1, padx=2, pady=1, sticky="nw")  



    def on_data_changed(self, *args):   
        selected_data = self.var_data.get()
        print("Selected data:", selected_data)
        self.data_structure = selected_data

        # self.createBSsetup(self.data,selected_data)
        # print(data["PatientInformation"]["Final"]["PatientFirstName"])

    def on_measure_changed(self, *args):   
        selected_measure = self.var_dataSt.get()
        print("Selected data:", selected_measure)
        self.measure = selected_measure

        self.createGraphic()

    
    def on_event_changed(self, *args):   
        selected_event = self.var_event.get()
        print("Selected data:", selected_event)
        self.event = selected_event

        self.createGraphic()

        
    def on_trend_changed(self, *args):   
        selected_trend = self.var_trend.get()
        print("Selected data:", selected_trend)
        self.trend = selected_trend

        self.createGraphic()


    def openNewWindow(self):
     
        # Toplevel object which will be treated as a new window
        self.newWindow = Toplevel(self)
    
        self.newWindow.title("Figure: " + self.data_structure)

        # sets the geometry of toplevel
        self.newWindow.geometry("1500x1000")
        
        def resizer(e):
            global new_byteW, new_resized_byteW, new_imageW 

            new_byteW = Image.open(self.graph)
            new_resized_byteW = new_byteW.resize((e.width,e.height), Image.ANTIALIAS)
            new_imageW = ImageTk.PhotoImage(new_resized_byteW)

            self.canvas_graphW.create_image(0,0, image = new_imageW, anchor="nw")


        print(self.newWindow.winfo_width())

        self.height=self.newWindow.winfo_screenheight()
        self.width=self.newWindow.winfo_screenwidth()

        self.byteW = Image.open(self.graph)

        self.imageW = ImageTk.PhotoImage(self.byteW)

        self.canvas_graphW = Canvas(master=self.newWindow)
        self.canvas_graphW.pack(fill="both", expand=True)

        self.canvas_graphW.create_image(0,0, image = self.imageW, anchor="nw")
        
        self.newWindow.bind('<Configure>', resizer)
    
        




    def createGraphic(self):    
        
        self.display_data = tk.CTkFrame(master=self.chose_data, fg_color="#ECECEC", width=700, height=400) #"#ECECEC")     
        self.display_data.grid(row=2, column=0, columnspan=2, pady=7, padx=10)
        
        #self.display_data.pack(fill="both", expand=False)

        for widget in self.display_data.winfo_children():
            widget.destroy()

        self.graph = "ana"
        self.graph_width = 700

        if self.data_structure=="LFP Montage (time domain)":
            
            try:
                self.apiInfo = api.plot_LfpMontageTimeDomain(self.data, self.selected_option[0])
                self.graph = self.apiInfo[1]
                
                self.text = self.apiInfo[0]
                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

            except:
                pass
        
        elif self.data_structure=="LFP Montage (frequency domain)":

            try:
                self.graph = api.plot_LfpMontage(self.data, self.selected_option[0])
                
                self.graph_text = tk.CTkLabel(master=self.display_data, anchor="nw", text="This graphic is obtained by applying an FFT algorithm to the Lfp Montage (time domain) data", font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

            except:
                pass
        
        elif self.data_structure=="Indefinite Streaming (time domain)":

            try:
                if self.selected_option[0]=="4":
                    self.apiInfo = api.plot_IndefiniteStreaming(self.dataInd)
                else:
                    self.apiInfo = api.plot_IndefiniteStreaming(self.data)
                
                self.graph = self.apiInfo[1]
                
                self.text = self.apiInfo[0]
                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

            except:
                pass
      
        elif self.data_structure=="Most Recent in Session":

            try:
                self.graph = api.plot_MostRecentInSession(self.data)
                
                self.graph_text = tk.CTkLabel(master=self.display_data, text="This graphic is obtained by applying an FFT algorithm to the Sense Chanel Tests data.", font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

            except:
                pass

        elif self.data_structure.startswith("Sense Channel"):
            try:
                self.apiInfo = api.plot_SenseChannel(self.data)
                self.text = self.apiInfo[0]

                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)
                
                if len(self.apiInfo)==3:
                    print("2 measurements") 

                    try:
                        self.var_dataSt = tk.StringVar(value=self.measure)   
                    except:    
                        self.var_dataSt = tk.StringVar(value="Select a measurement")   
                    
                    self.var_dataSt.trace("w", self.on_measure_changed)       
                    self.measures = tk.CTkOptionMenu(self.display_data, variable=self.var_dataSt, text_color="grey", width=480, height=20, fg_color="white", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=["First measurement","Second measurement"])
                    self.measures.pack(pady=8)  
                    
                    try:
                        if self.measure=="First measurement": 
                            self.graph = self.apiInfo[1]        
                        elif self.measure=="Second measurement":
                            self.graph = self.apiInfo [2]
                    except:
                        pass
                    
                else:
                    print("1 measurement")
                    self.graph = self.apiInfo[1]        

            except:
                pass

        elif self.data_structure=="Calibration Tests":

            try:
                self.apiInfo = api.plot_CalibrationTests(self.data)
                self.text = self.apiInfo[0]

                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)
                
                if len(self.apiInfo)==3:
                    print("2 measurements") 

                    try:
                        self.var_dataSt = tk.StringVar(value=self.measure)   
                    except:    
                        self.var_dataSt = tk.StringVar(value="Select a measurement")   
                    
                    self.var_dataSt.trace("w", self.on_measure_changed)       
                    self.measures = tk.CTkOptionMenu(self.display_data, variable=self.var_dataSt, text_color="grey", width=480, height=20, fg_color="white", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=["First measurement","Second measurement"])
                    self.measures.pack(pady=8)    
                    
                    try:
                        if self.measure=="First measurement": 
                            self.graph = self.apiInfo[1]        
                        elif self.measure=="Second measurement":
                            self.graph = self.apiInfo [2]
                    except:
                        pass
                    
                else:
                    print("1 measurement")
                    self.graph = self.apiInfo[1]        

            except:
                pass

        
        elif self.data_structure=="Brain Sense (time domain)":

            try:
                self.apiInfo = api.plot_BrainSenseTD(self.data)
                self.graph = self.apiInfo[1]
                
                self.text = self.apiInfo[0]
                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

            except:
                pass
        
        elif self.data_structure=="Brains Sense LFP":

            try:
                self.apiInfo = api.plot_BrainSenseLfp(self.data)
                self.graph = self.apiInfo[1]
                
                self.text = self.apiInfo[0]
                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

            except:
                pass

        elif self.data_structure=="LFP Trend Logs":

            try:
                self.apiInfo = api.plot_LfpTrendLogs(self.data)
                self.trend_list = self.apiInfo[-2]
                self.text = self.apiInfo[-1]

                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

                try:
                    self.var_trend = tk.StringVar(value=self.trend)   
                except:    
                    self.var_trend = tk.StringVar(value="Select a date")   
                
                self.var_trend.trace("w", self.on_trend_changed)     
                self.trends = tk.CTkOptionMenu(self.display_data, variable=self.var_trend, text_color="grey", width=480, height=20, fg_color="white", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=self.trend_list)
                self.trends.pack(pady=8)  
                
                try:
                    for i in self.trend_list:
                        if self.trend==i: 
                            index = self.trend_list.index(i)
                            print(index)
                            self.graph = self.apiInfo[index]        

                except:
                    pass

            except:
                pass
            
        
        elif self.data_structure=="LFP Frequency Snapshot Events":
        
            try:
                for widget in self.display_data.winfo_children():
                    widget.destroy()

                self.apiInfo = api.plot_LfpFrequencySnapshotEvents(self.data)
                self.event_list = self.apiInfo[-2]
                self.text = self.apiInfo[-1]

                self.graph_text = tk.CTkLabel(master=self.display_data, text=self.text, font=("Arial", 12), width=400)
                self.graph_text.pack(padx=5, pady=5)

                try:
                    self.var_event = tk.StringVar(value=self.event)   
                except:    
                    self.var_event = tk.StringVar(value="Select an event")   
                
                self.var_event.trace("w", self.on_event_changed)     
                self.events = tk.CTkOptionMenu(self.display_data, variable=self.var_event, text_color="grey", width=480, height=20, fg_color="white", button_color="#c75d55", button_hover_color="#c75d55", dropdown_hover_color="grey", values=self.event_list)
                self.events.pack(pady=8) 
                

                try:
                    for i in self.event_list:
                        if self.event==i: 
                            print("entrei")
                            print(self.event)
                            index = self.event_list.index(i)
                            print(index)
                            self.graph = self.apiInfo[index]  

                except:
                    pass

            except:
                pass
                self.errorgraphic = tk.CTkLabel(self.display_data, text="No data available for this patient.",font=("Arial", 12), text_color="black", width=300).pack()

        # def on_resize(event):
            # self.byte = Image.open(self.graph)
            # self.reziged_image = self.byte.resize((event.width,event.height), Image.ANTIALIAS)
            # self.image = ImageTk.PhotoImage(self.reziged_image)
            # self.image.configure(size=(event.width,event.height))
            #self.image.configure(width=event.width, height=event.height)# anchor = "cnter")

        try:
            
            self.byte = Image.open(self.graph)


            self.image = ImageTk.PhotoImage(self.byte)

            print(self.image.width())
            self.graph_width = self.image.width() + 40
 
            #self.graph_image = tk.CTkLabel(master=self.display_data, image = self.image, text="")#, anchor = "center")
            #self.graph_image.pack(pady=15, padx=7, fill="both", expand=True) #grid(row=0, column=0, padx=5)

            self.canvas_graph = Canvas(master=self.display_data, width=self.graph_width, height=1000)
            self.canvas_graph.pack(padx=10, fill="both", expand=True)

            self.canvas_graph.create_image(0,0, image = self.image, anchor="nw")

            #self.image_window = Button(master=self.display_data, text="+", command= self.openNewWindow) 
            self.image_window = tk.CTkButton(master=self.display_data, image=self.search_image, compound="right", text="+",width=10, height=15, fg_color="#c75d55", hover=True, hover_color="grey", command= self.openNewWindow) 
            
            self.button_image_window = self.canvas_graph.create_window(80, 20, 
                                       anchor = "center",
                                       window = self.image_window)


        except:
            #pass
            if self.graph=="ana":
                self.errorgraphic = tk.CTkLabel(self.display_data, text="",font=("Arial", 12), text_color="black", width=300).pack()
            else:
                for widget in self.display_data.winfo_children():
                    widget.destroy()
                self.errorgraphic = tk.CTkLabel(self.display_data, text="No data available for this patient.",font=("Arial", 12), text_color="black", width=300).pack()



    # def close(self):
    #     app.destroy()    
    

if __name__ == "__main__":
    app = App()
    ### RUN APP
    app.mainloop()

 