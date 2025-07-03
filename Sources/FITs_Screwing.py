# For BU INNOVIZ
from datetime import datetime
from tkinter import messagebox, simpledialog
import tkinter as tk
import pandas as pd
import glob, os, shutil
import configparser
import time

from fitsdll import fn_Handshake, fn_Log
from sqs_connect import send_fi_telegram

class CAutoFITs_Screw():
    def __init__ (self):
        # Read parameters from config files
        self.MC = os.environ["COMPUTERNAME"]
        config = configparser.ConfigParser()
        main_files = "C:\Projects\Autokeys_Screw"
        config.read(os.path.join(main_files ,"Properties\config.ini"))
        try:
            self.FITs = config["DEFAULT"].get("FITs", "")
            self.path = config["DEFAULT"].get("file_path", "")
            self.path_extend = config["DEFAULT"].get("path_extend", "")
            self.model = config[self.MC].get("model", "")
            self.operation = config[self.MC].get("operation", "")
            self.fixture = config[self.MC].get("fixture", "")
        except Exception as error:
            print("Please check config.ini")
            quit()

        self.serial = ""

    def findAllTorqueDatabaseFiles(self):
        allfiles = []
        source_filepath = os.path.join(self.path, self.path_extend)
        for file in glob.glob(source_filepath):
            # print(file)
            allfiles.append(file)
        return allfiles
    
    def move_folder(src, dst):
        if os.path.exists(dst):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            shutil.rmtree(src)
        else:
            shutil.move(src, dst)
            
    def check_pd_filter(input):
        if isinstance(input, pd.Series) and input.empty:
            return None
        elif pd.isna(input):
            return None
        else:
            return input    
            
    def openDatabaseFile(self, file):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        now = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        # Read file
        df = pd.read_csv(file)
        # print("PAth file:\t", file)
        self.serial = df["Product Id"][0]
        try:
            Operator = str(int(df["Operator"][df["Operator"].first_valid_index()]))
        except Exception as error:
            Operator = "519723"
        # print("EN:\t", Operator)
        station = df["Station"][0]

        status = df["Unique ID"].str.contains("Complete Process", case=False, na=False).any()
        if not status:
            print(f"File {file} is not complete yet")
            minedData = df_output
            current_path = file
            CompactPathName = "NG"
            return minedData, current_path, CompactPathName

        # For operation MB to Top cover
        if self.operation == "IN230":
            try:
                BN_Screw = df.loc[(df["Unique ID"] == "SCAN SERIAL MB") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                MB2TC_01 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.01")
                MB2TC_02 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.02")
                MB2TC_03 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.03")
                MB2TC_04 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.04")
                MB2TC_05 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.05")
                MB2TC_06 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.06")
                MB2TC_07 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.07")
                MB2TC_08 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.08")
                
                data = {
                    "EN": Operator,
                    "Operation": self.operation, 
                    "SN unit": self.serial,
                    "BN Screw": CAutoFITs_Screw.check_pd_filter(BN_Screw),
                    "Program Name": "Screwing MB to Top cover",
                    "Fixture jig": self.fixture,
                    "Torque_1": CAutoFITs_Screw.check_pd_filter(MB2TC_01["Actual Torque"]),
                    "Angle_1": CAutoFITs_Screw.check_pd_filter(MB2TC_01["Actual Angle"]),
                    "Result_1": CAutoFITs_Screw.check_pd_filter(MB2TC_01["Status"]),
                    "Torque_2": CAutoFITs_Screw.check_pd_filter(MB2TC_02["Actual Torque"]),
                    "Angle_2": CAutoFITs_Screw.check_pd_filter(MB2TC_02["Actual Angle"]),
                    "Result_2": CAutoFITs_Screw.check_pd_filter(MB2TC_02["Status"]),
                    "Torque_3": CAutoFITs_Screw.check_pd_filter(MB2TC_03["Actual Torque"]),
                    "Angle_3": CAutoFITs_Screw.check_pd_filter(MB2TC_03["Actual Angle"]),
                    "Result_3": CAutoFITs_Screw.check_pd_filter(MB2TC_03["Status"]),
                    "Torque_4": CAutoFITs_Screw.check_pd_filter(MB2TC_04["Actual Torque"]),
                    "Angle_4": CAutoFITs_Screw.check_pd_filter(MB2TC_04["Actual Angle"]),
                    "Result_4": CAutoFITs_Screw.check_pd_filter(MB2TC_04["Status"]),
                    "Torque_5": CAutoFITs_Screw.check_pd_filter(MB2TC_05["Actual Torque"]),
                    "Angle_5": CAutoFITs_Screw.check_pd_filter(MB2TC_05["Actual Angle"]),
                    "Result_5": CAutoFITs_Screw.check_pd_filter(MB2TC_05["Status"]),
                    "Torque_6": CAutoFITs_Screw.check_pd_filter(MB2TC_06["Actual Torque"]),
                    "Angle_6": CAutoFITs_Screw.check_pd_filter(MB2TC_06["Actual Angle"]),
                    "Result_6": CAutoFITs_Screw.check_pd_filter(MB2TC_06["Status"]),
                    "Torque_7": CAutoFITs_Screw.check_pd_filter(MB2TC_07["Actual Torque"]),
                    "Angle_7": CAutoFITs_Screw.check_pd_filter(MB2TC_07["Actual Angle"]),
                    "Result_7": CAutoFITs_Screw.check_pd_filter(MB2TC_07["Status"]),
                    "Torque_8": CAutoFITs_Screw.check_pd_filter(MB2TC_08["Actual Torque"]),
                    "Angle_8": CAutoFITs_Screw.check_pd_filter(MB2TC_08["Actual Angle"]),
                    "Result_8": CAutoFITs_Screw.check_pd_filter(MB2TC_08["Status"]),
                    "Result": "None"
                }
                # Convert the dictionary to a DataFrame
                df_output = pd.DataFrame([data])
                nan_positions = df_output.isna()
                if nan_positions.any().any():
                    
                    print(f"File {file} is not complete yet")
                    
                    minedData = df_output
                    current_path = file
                    CompactPathName = "NG"
                    return minedData, current_path, CompactPathName

                result_columns = ["Result_1", "Result_2", "Result_3", "Result_4", "Result_5", "Result_6", "Result_7", "Result_8"]
                convertstatus = True
            except Exception as error:
                
                print(f"{self.operation} file >> {file}")
                print(error)
                
                messagebox.showerror("Process Message", f"FAIL to Generate Compact log file: {file}") 
                convertstatus = False
            
        # For operation Detector to OB
        elif self.operation == "OB120":
            # print("operation:\t", operation)
            try:
                BN_Screw = df.loc[(df["Unique ID"] == "Screw Material") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                DB2OB_01 = df.loc[(df["Unique ID"] == "DB2OB.01") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                DB2OB_02 = df.loc[(df["Unique ID"] == "DB2OB.02") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                DB2OB_03 = df.loc[(df["Unique ID"] == "DB2OB.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()

                data = {
                    "EN": Operator,     
                    "Operation": self.operation, 
                    "SN OB": self.serial, 
                    "BN Screw": CAutoFITs_Screw.check_pd_filter(BN_Screw),
                    "Program Name": "Detector to OB",
                    "Fixture jig": self.fixture,
                    "Torque_1": CAutoFITs_Screw.check_pd_filter(DB2OB_01["Actual Torque"]),
                    "Angle_1": CAutoFITs_Screw.check_pd_filter(DB2OB_01["Actual Angle"]),
                    "Result_1": CAutoFITs_Screw.check_pd_filter(DB2OB_01["Status"]),
                    "Torque_2": CAutoFITs_Screw.check_pd_filter(DB2OB_02["Actual Torque"]),
                    "Angle_2": CAutoFITs_Screw.check_pd_filter(DB2OB_02["Actual Angle"]),
                    "Result_2": CAutoFITs_Screw.check_pd_filter(DB2OB_02["Status"]),
                    "Torque_3": CAutoFITs_Screw.check_pd_filter(DB2OB_03["Actual Torque"]),
                    "Angle_3": CAutoFITs_Screw.check_pd_filter(DB2OB_03["Actual Angle"]),
                    "Result_3": CAutoFITs_Screw.check_pd_filter(DB2OB_03["Status"]),
                    "Result": "None",
                }
                # Convert the dictionary to a DataFrame
                df_output = pd.DataFrame([data])
                nan_positions = df_output.isna()
                if nan_positions.any().any():
                    
                    print(f"File {file} is not complete yet")
                    
                    minedData = df_output
                    current_path = file
                    CompactPathName = "NG"
                    return minedData, current_path, CompactPathName
                
                result_columns = ["Result_1", "Result_2", "Result_3"]
                convertstatus = True
            except Exception as error:
                
                print(f"{self.operation} file >> {file}")
                print(error)
                
                messagebox.showerror("Process Message", f"FAIL to Generate Compact log file: {file}") 
                convertstatus = False

        # For operation Interface connector to Top  
        elif self.operation ==  "IN240":
            # print("operation:\t", operation)
            try:
                PBA_SN = df.loc[(df["Unique ID"] == "SCAN PCBA") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                BN_Screw = df.loc[(df["Unique ID"] == "SCAN SERIAL MB") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                IC2TC_01 = df.loc[(df["Unique ID"] == "IC2TC.01") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                IC2TC_02 = df.loc[(df["Unique ID"] == "IC2TC.02") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                IC2TC_03 = df.loc[(df["Unique ID"] == "IC2TC.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                IC2TC_03 = df.loc[(df["Unique ID"] == "IC2TC.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                IC2TC_04 = df.loc[(df["Unique ID"] == "IC2TC.04") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                IC2TC_05 = df.loc[(df["Unique ID"] == "IC2TC.05") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                IC2TC_06 = df.loc[(df["Unique ID"] == "IC2TC.06") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                
                data = {
                    "SN unit": self.serial,  
                    "EN": Operator, 
                    "Operation": self.operation, 
                    "Interface PBA SN": CAutoFITs_Screw.check_pd_filter(PBA_SN),
                    "BN Screw": CAutoFITs_Screw.check_pd_filter(BN_Screw),   
                    "Program Name": "Interface connector to Top",
                    "Fixture jig": self.fixture,
                    "Torque_1": CAutoFITs_Screw.check_pd_filter(IC2TC_01["Actual Torque"]),
                    "Angle_1": CAutoFITs_Screw.check_pd_filter(IC2TC_01["Actual Angle"]),
                    "Result_1": CAutoFITs_Screw.check_pd_filter(IC2TC_01["Status"]),
                    "Torque_2": CAutoFITs_Screw.check_pd_filter(IC2TC_02["Actual Torque"]),
                    "Angle_2": CAutoFITs_Screw.check_pd_filter(IC2TC_02["Actual Angle"]),
                    "Result_2": CAutoFITs_Screw.check_pd_filter(IC2TC_02["Status"]),
                    "Torque_3": CAutoFITs_Screw.check_pd_filter(IC2TC_03["Actual Torque"]),
                    "Angle_3": CAutoFITs_Screw.check_pd_filter(IC2TC_03["Actual Angle"]),
                    "Result_3": CAutoFITs_Screw.check_pd_filter(IC2TC_03["Status"]),
                    "Torque_4": CAutoFITs_Screw.check_pd_filter(IC2TC_04["Actual Torque"]),
                    "Angle_4": CAutoFITs_Screw.check_pd_filter(IC2TC_04["Actual Angle"]),
                    "Result_4": CAutoFITs_Screw.check_pd_filter(IC2TC_04["Status"]),
                    "Torque_5": CAutoFITs_Screw.check_pd_filter(IC2TC_05["Actual Torque"]),
                    "Angle_5": CAutoFITs_Screw.check_pd_filter(IC2TC_05["Actual Angle"]),
                    "Result_5": CAutoFITs_Screw.check_pd_filter(IC2TC_05["Status"]),
                    "Torque_6": CAutoFITs_Screw.check_pd_filter(IC2TC_06["Actual Torque"]),
                    "Angle_6": CAutoFITs_Screw.check_pd_filter(IC2TC_06["Actual Angle"]),
                    "Result_6": CAutoFITs_Screw.check_pd_filter(IC2TC_06["Status"]),
                    "Result": "None"
                }
                # Convert the dictionary to a DataFrame
                df_output = pd.DataFrame([data])
                nan_positions = df_output.isna()
                if nan_positions.any().any():
                    
                    print(f"File {file} is not complete yet")
                    
                    minedData = df_output
                    current_path = file
                    CompactPathName = "NG"
                    return minedData, current_path, CompactPathName
                
                result_columns = ["Result_1", "Result_2", "Result_3", "Result_4", "Result_5", "Result_6"]
                convertstatus = True
            except Exception as error:
                
                print(f"{self.operation} file >> {file}")
                print(error)
                
                messagebox.showerror("Process Message", f"FAIL to Generate Compact log file: {file}") 
                
                convertstatus = False

        elif self.operation == "IN700":
            # print("operation:\t", operation)
            try:
                Top_cover = df.loc[(df["Unique ID"] == "SCAN SERIAL MB") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                BN_Screw = df.loc[(df["Unique ID"] == "SCREW Material") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                MB2TC_01 = df.loc[(df["Unique ID"] == "MB2TC.01") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_02 = df.loc[(df["Unique ID"] == "MB2TC.02") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_03 = df.loc[(df["Unique ID"] == "MB2TC.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_03 = df.loc[(df["Unique ID"] == "MB2TC.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_04 = df.loc[(df["Unique ID"] == "MB2TC.04") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_05 = df.loc[(df["Unique ID"] == "MB2TC.05") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_06 = df.loc[(df["Unique ID"] == "MB2TC.06") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_07 = df.loc[(df["Unique ID"] == "MB2TC.07") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                MB2TC_08 = df.loc[(df["Unique ID"] == "MB2TC.08") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
                
                data = {
                    "SN unit": self.serial,  
                    "EN": Operator, 
                    "Operation": self.operation, 
                    "BN Top cover": CAutoFITs_Screw.check_pd_filter(Top_cover),
                    "BN Screw": CAutoFITs_Screw.check_pd_filter(BN_Screw),   
                    "Program Name": "Screwing Cover Screws Type1",
                    "Fixture jig": self.fixture,
                    "Torque_1": CAutoFITs_Screw.check_pd_filter(MB2TC_01["Actual Torque"]),
                    "Angle_1": CAutoFITs_Screw.check_pd_filter(MB2TC_01["Actual Angle"]),
                    "Result_1": CAutoFITs_Screw.check_pd_filter(MB2TC_01["Status"]),
                    "Torque_2": CAutoFITs_Screw.check_pd_filter(MB2TC_02["Actual Torque"]),
                    "Angle_2": CAutoFITs_Screw.check_pd_filter(MB2TC_02["Actual Angle"]),
                    "Result_2": CAutoFITs_Screw.check_pd_filter(MB2TC_02["Status"]),
                    "Torque_3": CAutoFITs_Screw.check_pd_filter(MB2TC_03["Actual Torque"]),
                    "Angle_3": CAutoFITs_Screw.check_pd_filter(MB2TC_03["Actual Angle"]),
                    "Result_3": CAutoFITs_Screw.check_pd_filter(MB2TC_03["Status"]),
                    "Torque_4": CAutoFITs_Screw.check_pd_filter(MB2TC_04["Actual Torque"]),
                    "Angle_4": CAutoFITs_Screw.check_pd_filter(MB2TC_04["Actual Angle"]),
                    "Result_4": CAutoFITs_Screw.check_pd_filter(MB2TC_04["Status"]),
                    "Torque_5": CAutoFITs_Screw.check_pd_filter(MB2TC_05["Actual Torque"]),
                    "Angle_5": CAutoFITs_Screw.check_pd_filter(MB2TC_05["Actual Angle"]),
                    "Result_5": CAutoFITs_Screw.check_pd_filter(MB2TC_05["Status"]),
                    "Torque_6": CAutoFITs_Screw.check_pd_filter(MB2TC_06["Actual Torque"]),
                    "Angle_6": CAutoFITs_Screw.check_pd_filter(MB2TC_06["Actual Angle"]),
                    "Result_6": CAutoFITs_Screw.check_pd_filter(MB2TC_06["Status"]),
                    "Torque_7": CAutoFITs_Screw.check_pd_filter(MB2TC_07["Actual Torque"]),
                    "Angle_7": CAutoFITs_Screw.check_pd_filter(MB2TC_07["Actual Angle"]),
                    "Result_7": CAutoFITs_Screw.check_pd_filter(MB2TC_07["Status"]),
                    "Torque_8": CAutoFITs_Screw.check_pd_filter(MB2TC_08["Actual Torque"]),
                    "Angle_8": CAutoFITs_Screw.check_pd_filter(MB2TC_08["Actual Angle"]),
                    "Result_8": CAutoFITs_Screw.check_pd_filter(MB2TC_08["Status"]),
                    "Result": "None"
                }

                # Convert the dictionary to a DataFrame
                df_output = pd.DataFrame([data])
                nan_positions = df_output.isna()
                if nan_positions.any().any():
                    
                    print(f"File {file} is not complete yet")
                    
                    minedData = df_output
                    current_path = file
                    CompactPathName = "NG"
                    return minedData, current_path, CompactPathName
                
                result_columns = ["Result_1", "Result_2", "Result_3", "Result_4", "Result_5", "Result_6", "Result_7", "Result_8"]
                convertstatus = True
            except Exception as error:
                
                print(f"{self.operation} file >> {file}")
                print(error)
                
                messagebox.showerror("Process Message", f"FAIL to Generate Compact log file: {file}") 
                
                convertstatus = False


        excelSavePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(file))),"Compact_Data")
        isExist = os.path.exists(excelSavePath)
        if isExist is False:
            os.makedirs(excelSavePath, exist_ok=True)

        DataLog = os.path.join(os.path.dirname(excelSavePath), "Raw_Data")
        os.makedirs(DataLog, exist_ok=True)
        
        achpath, ext = os.path.splitext(os.path.basename(file))
        # print("achpath:\t",achpath)
        datetimeformat = datetime.now().strftime("%Y%m%d%H%M%S")
        New_ach = os.path.join(os.path.dirname(file), f"{achpath}_{datetimeformat}{ext}")

        if convertstatus is True:      
            # Replace "OK" with "PASS" in the specified columns
            df_output[result_columns] = df_output[result_columns].replace("OK", "PASS").replace("NOK", "FAIL")
            df_output["Result"] = df_output[result_columns].apply(lambda x: "PASS" if all(x == "PASS") else "FAIL", axis=1)
            # print("Create Compact file Serial:", df_output["SN Scanner"][0])
            # saving the dataframe
            CompactPathName = os.path.join(excelSavePath ,f'{self.serial}_{now}.csv')
            df_output.to_csv(CompactPathName, header=True, index=False)
            # check folder name in RAW_DATA are already exist?

            FolderInRawData = os.path.join(DataLog, os.path.basename(os.path.dirname(file)))
            isExist = os.path.exists(FolderInRawData)
            try:
                os.rename(file, New_ach)
            except Exception as error:
                df_output = False 
                current_path = file
                return  df_output, current_path, CompactPathName
            
            if isExist is True:
                shutil.move(New_ach, os.path.join(DataLog, os.path.basename(os.path.dirname(New_ach))))
                current_path = os.path.join(FolderInRawData, os.path.basename(New_ach))
                if len(os.listdir(os.path.dirname(New_ach))) == 0: 
                    os.rmdir(os.path.dirname(New_ach)) 
            elif isExist is False: 
                os.makedirs(FolderInRawData, exist_ok=True)
                shutil.move(New_ach, FolderInRawData)
                current_path = os.path.join(FolderInRawData, os.path.basename(New_ach))
                if len(os.listdir(os.path.dirname(New_ach))) == 0: 
                    os.rmdir(os.path.dirname(New_ach)) 

        elif convertstatus is False:
            CompactPathName = False
            Corrupted_Files = os.path.join(DataLog, "Corrupted_Files")
            os.makedirs(Corrupted_Files, exist_ok=True)
            try:
                os.rename(file, New_ach)
            except Exception as error:
                df_output = False 
                current_path = file
                return  df_output, current_path, CompactPathName
            isExist = os.path.exists(os.path.join(Corrupted_Files, os.path.basename(os.path.dirname(New_ach))))
            if isExist is True:
                shutil.move(New_ach, os.path.join(Corrupted_Files, os.path.basename(os.path.dirname(New_ach))))
                current_path = os.path.join(os.path.join(Corrupted_Files, os.path.basename(os.path.dirname(New_ach))), os.path.basename(New_ach))
                if len(os.listdir(os.path.dirname(New_ach))) == 0:
                    os.rmdir(os.path.dirname(New_ach))
            elif isExist is False:
                os.makedirs(os.path.join(Corrupted_Files, os.path.basename(os.path.dirname(file))), exist_ok=True)
                shutil.move(New_ach, os.path.join(Corrupted_Files, os.path.basename(os.path.dirname(New_ach))))
                current_path = os.path.join(os.path.join(Corrupted_Files, os.path.basename(os.path.dirname(New_ach))), os.path.basename(New_ach))
                if len(os.listdir(os.path.dirname(New_ach))) == 0: 
                    os.rmdir(os.path.dirname(New_ach))
                     
            df_output = False
            
        return df_output, current_path, CompactPathName

    def UploadDataToFITs(self, dataFrame, current_path, CompactPathName):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        ## Create folder FITS_Log_Fail && FITS_Handcheck_Fail
        FITS_Log_Fail = os.path.join(os.path.dirname(os.path.dirname(current_path)), "FITS_Log_Fail")
        os.makedirs(FITS_Log_Fail, exist_ok=True)
        FITS_Handcheck_Fail = os.path.join(os.path.dirname(os.path.dirname(current_path)), "FITS_Handcheck_Fail")
        os.makedirs(FITS_Handcheck_Fail, exist_ok=True)
    
        model = self.model
        operation = self.operation
        serial = self.serial
        parameters = ";".join(dataFrame.columns.tolist())
        values = ";".join(dataFrame.values.tolist()[0])
        Handshake_status = fn_Handshake(model, operation, serial)
        
        if Handshake_status is True:
            fn_log = fn_Log(model, operation, parameters, values)
            if fn_log == True:
                print(f"{serial} has been uploaded TO FITS {operation}.")
            else:   
                print('FITs Log Fail:\t', f'{fn_log}')
                messagebox.showerror('FITs Log Fail', f'Serial {serial}\n{fn_log}')
                CAutoFITs_Screw.move_folder(os.path.dirname(current_path), os.path.join(FITS_Log_Fail, os.path.basename(os.path.dirname(current_path))))
        else:
                print('FITs Log Fail:\t', f'{Handshake_status}')
                messagebox.showerror('FITs Handcheck Fail', f'Serial {serial}\n{Handshake_status}')
                rename =  os.path.join(os.path.dirname(CompactPathName) ,"Fail_HandCheck_" + os.path.basename(CompactPathName))
                os.rename(CompactPathName, rename)
                CAutoFITs_Screw.move_folder(os.path.dirname(current_path), os.path.join(FITS_Handcheck_Fail, os.path.basename(os.path.dirname(current_path))))

    def get_last_valid_row(df, uid):
        ok_df = df.loc[
            (df["Unique ID"] == uid) &
            (df["Status"] == "OK") &
            (df["Value"] == "OK"),
            ["Actual Torque", "Actual Angle", "Status"]
            ]
        if not ok_df.empty:
            return ok_df.tail(1).squeeze()
        
        nok_df = df.loc[
            (df["Unique ID"] == uid) &
            (df["Status"] == "NOK") &
            (df["Value"] == "NOK"),
            ["Actual Torque", "Actual Angle", "Status"]
            ]
        if not nok_df.empty:
            return nok_df.tail(1).squeeze()
        
        return None
    def scan_serial_window(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        while True:
            main_serial = simpledialog.askstring("Scann Main Serial", "Please Scan Main Serial")
            if len(main_serial) == 12:
                status_handshake = fn_Handshake("*", self.operation) 
    def aggregateAllDataAndSaveToFile(self):
        filesFound = CAutoFITs_Screw.findAllTorqueDatabaseFiles(self)
        for file in filesFound:
            minedData, current_path, CompactPathName = CAutoFITs_Screw.openDatabaseFile(self, file)
            if minedData == False or CompactPathName == "NG":
                continue
            if self.FITs.upper() == "ENABLE":
                CAutoFITs_Screw.UploadDataToFITs(self,minedData, current_path, CompactPathName)

while True:
    print("START")
    minedData=CAutoFITs_Screw()
    minedData.aggregateAllDataAndSaveToFile()
    time_sec = 30
    now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    print(f"{now}\tSleep:\t{time_sec}\tsecond")
    time.sleep(time_sec)