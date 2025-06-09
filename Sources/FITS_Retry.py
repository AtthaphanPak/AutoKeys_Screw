from win32com.client import Dispatch
from tkinter import messagebox
from datetime import datetime
import glob, os, shutil
import tkinter as tk
import pandas as pd
import configparser
import time

class CAutoFITs_Retry_Torque_Scanner():
    def __init__ (self):
        # Read parameters from config files
        config = configparser.ConfigParser()
        main_files = "C:\Auto-FITs-Scanner"
        if os.path.exists(main_files) is False:
            os.makedirs(main_files)
            os.makedirs(os.path.join(main_files,"Properties"))
        config.read(os.path.join(main_files ,"Properties\config.ini"))
        try:
            self.retry_path = config["DEFAULT"]["retry_path"]
            self.model = config["DEFAULT"]["model"]
            self.Query_parameters = config["DEFAULT"]["Query_parameters"]
            self.Query_operation = config["DEFAULT"]["Query_operation"]
        except Exception as error:
            print("Please check config.ini")
            print(error)
            quit()

    def Handshake(model, operation, serial):
        lib = Dispatch("FITSDLL.clsDB") 
        fn_initDB = lib.fn_initDB(f"{model}",f"{operation}","2.10","dbLuminar")
        if fn_initDB == str("True"):
            fn_handshake = lib.fn_handshake(f"{model}",f"{operation}","2.10",f"{serial}")
            print("fn_handshake:\t", fn_handshake)
            if fn_handshake == str("True"):
                return True
            else:
                return False
        else:
            print("fn_initDB:\t", fn_initDB)
            return False

    def Log(model, operation, parameters,values):
        list_parameters = {}
        lib = Dispatch("FITSDLL.clsDB")
        ## Define Shift 
        start_day_shift = datetime.strptime("07:00","%H:%M").time()
        end_day_shift = datetime.strptime("19:00","%H:%M").time()
        if start_day_shift <= datetime.now().time() <= end_day_shift:
            list_parameters["Shift"] = "DAY"
        else:
            list_parameters["Shift"] = "NIGHT"
        list_parameters["MC"] = os.environ['COMPUTERNAME']
        parameters = parameters + ";" + "Shift" + ";" + "MC"
        values =  values + ";" + list_parameters["Shift"] + ";" + list_parameters["MC"]
        fn_initDB = lib.fn_initDB(f"{model}",f"{operation}","2.10","dbLuminar")
        if fn_initDB == "True":
            # print("model:\t", model)
            # print("operation:\t", operation)
            # print("parameters:\t", parameters)
            # print("values:\t", values)
            fn_log = lib.fn_log(f"{model}",f"{operation}","2.10",f"{parameters}",f"{values}",";")
            if fn_log == "True":
                return True
            else:
                return False
        else:
            return False

    def Query(model, operation, serial, query_para, values):
        lib = Dispatch("FITSDLL.clsDB")
        query_array = []
        fn_initDB = lib.fn_initDB(f"{model}",f"{operation}","2.10","dbLuminar")
        if fn_initDB == str("True"):
            for param in query_para.split(';'):
                fn_query = lib.fn_query(f"{model}",f"{operation}","2.10",f"{serial}",f"{param}",";")
                query_values = fn_query.replace(";","")
                if query_values != "-":
                    query_array.append(query_values)
            query_result = ";".join(query_array)
            values = f"{values};{query_result}"
            return values
        else:
            print(f"fn_Query --> {serial} Fail")
            parameters = "FAIL"
            values = "FAIL"
            return parameters, values
        
    def ReadAll(self):
        allpaths = []
        pathfail = os.path.join(self.retry_path, "Fail_HandCheck_*.csv")
        if os.path.exists(self.retry_path):
            allpaths = glob.glob(pathfail)
        else:
            exit()
        if allpaths is None:
            print("None")
            exit()
            
        return allpaths       

    def FITS_Retry(self, allpaths):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        model = self.model
        Query_parameters = self.Query_parameters
        query_operation = self.Query_operation
        now = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        
        for path in allpaths:
            dataFrame = pd.read_csv(path)
            print(path)
            programname = dataFrame["Program Name"].to_string(index=False)
            if programname.lower() == "pcba":
                operation = "S200A"
            elif programname.lower() == "ploygon":
                operation = "S300A"
            elif programname.lower() == "latm":
                operation = "S400A"
                
            serial = dataFrame["SN Scanner"].to_string(index=False)
            parameters = ";".join(dataFrame.columns.tolist())
            values = ";".join(dataFrame.astype(str).values.tolist()[0])
            fn_Handshake = CAutoFITs_Retry_Torque_Scanner.Handshake(model, operation, serial)
            
            if fn_Handshake is True:
                values = CAutoFITs_Retry_Torque_Scanner.Query(model, query_operation, serial, Query_parameters, values)
                parameters = f"{parameters};{Query_parameters}"
                fn_log = CAutoFITs_Retry_Torque_Scanner.Log(model, operation, parameters, values)
                print(f"fn_Log --> {serial} {fn_log}")
                if fn_log == True:
                    os.rename(path, os.path.join(os.path.dirname(path), f"{serial}_{now}.csv"))
                    print(f"PUSH {serial} TO FITS DONE.")
                elif fn_log == False:   
                    messagebox.showerror('FITs Log Fail', f'Serial {serial}\n')
            elif fn_Handshake is False:
                    messagebox.showerror('FITs Handcheck Fail', f'Serial {serial}\n')


MainClass=CAutoFITs_Retry_Torque_Scanner()
allpaths = MainClass.ReadAll()
MainClass.FITS_Retry(allpaths)
time.sleep(10)