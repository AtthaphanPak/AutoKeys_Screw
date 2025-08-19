# For BU INNOVIZ
from datetime import datetime
import pandas as pd
import glob, os, shutil
import configparser
import time
import tempfile

from fitsdll import fn_Log
from sqs_connect import send_fi_telegram, Check_result_telegram
from window import scan_serial, message_popup

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
            self.sub = config[self.MC].get("sub", "").split(",")
        except Exception as error:
            print("Please check config.ini")
            quit()

        self.bin_folder = os.path.join(os.path.dirname(self.path), "bin")
        os.makedirs(self.bin_folder, exist_ok=True)
        self.serial = ""
        self.sub_sn = []

    def findTorqueDataFiles(self):
        pattren = os.path.join(self.path, "*", f"{self.serial}_*.csv")
        files = glob.glob(pattren)
        if not files:
            print("File not found")
            return None
        file = max(files, key=os.path.getatime)
        return file
    
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
        now = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        # Read file
        df = pd.read_csv(file)
        # print("PAth file:\t", file)
        try:
            Operator = str(int(df["Operator"][df["Operator"].first_valid_index()]))
        except Exception as error:
            Operator = "524161"
        # print("EN:\t", Operator)

        status = df["Unique ID"].str.contains("Complete Process", case=False, na=False).any()
        if not status:
            print(f"File {file} is not complete yet")
            minedData = None
            current_path = file
            CompactPathName = "NG"
            return minedData, current_path, CompactPathName

        # For operation MB to Top cover
        if self.operation == "IN230":
            try:
                # BN_Screw = df.loc[(df["Unique ID"] == "SCAN SERIAL MB") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                # BN_Screw = sub_sn[0]
                MB2TC_01 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.01")
                MB2TC_02 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.02")
                MB2TC_03 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.03")
                MB2TC_04 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.04")
                MB2TC_05 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.05")
                MB2TC_06 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.06")
                MB2TC_07 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.07")
                MB2TC_08 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.08")
                
                data = {
                    "EN": str(Operator),
                    "Operation": str(self.operation), 
                    "SN": str(self.serial),
                    "BN Screw": str(self.sub_sn[0]),
                    "Main board SN": str(self.sub_sn[1]),
                    "Program Name": "Screwing MB to Top cover",
                    "Fixture jig": str(self.fixture),
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
                
                message_popup(3, "Process Message", f"FAIL to Generate Compact log file: {file}") 
                convertstatus = False
            
        # For operation Detector to OB
        elif self.operation == "OB120":
            # print("operation:\t", operation)
            try:
                # BN_Screw = df.loc[(df["Unique ID"] == "Screw Material") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                DB2OB_01 = CAutoFITs_Screw.get_last_valid_row(df, "DB2OB.01")
                DB2OB_02 = CAutoFITs_Screw.get_last_valid_row(df, "DB2OB.02")
                DB2OB_03 = CAutoFITs_Screw.get_last_valid_row(df, "DB2OB.03")

                data = {
                    "EN": str(Operator),     
                    "Operation": str(self.operation), 
                    "SN": str(self.serial), 
                    "BN Screw": str(self.sub_sn[0]),
                    "Program Name": "Detector to OB",
                    "Fixture jig": str(self.fixture),
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
                
                message_popup(3, "Process Message", f"FAIL to Generate Compact log file: {file}") 
                convertstatus = False

        # For operation Interface connector to Top  
        elif self.operation ==  "IN240":
            # print("operation:\t", operation)
            try:
                # PBA_SN = df.loc[(df["Unique ID"] == "SCAN PCBA") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                # BN_Screw = df.loc[(df["Unique ID"] == "SCAN SERIAL MB") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                IC2TC_01 = CAutoFITs_Screw.get_last_valid_row(df, "IC2TC.01")
                IC2TC_02 = CAutoFITs_Screw.get_last_valid_row(df, "IC2TC.02")
                IC2TC_03 = CAutoFITs_Screw.get_last_valid_row(df, "IC2TC.03")
                IC2TC_04 = CAutoFITs_Screw.get_last_valid_row(df, "IC2TC.04")
                IC2TC_05 = CAutoFITs_Screw.get_last_valid_row(df, "IC2TC.05")
                IC2TC_06 = CAutoFITs_Screw.get_last_valid_row(df, "IC2TC.06")
                
                data = { 
                    "EN": str(Operator), 
                    "Operation": str(self.operation), 
                    "SN": str(self.serial), 
                    "Interface PBA SN": str(self.sub_sn[1]),
                    "BN Screw": str(self.sub_sn[0]),
                    "Program Name": "Interface connector to Top",
                    "Fixture jig": str(self.fixture),
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
                
                message_popup(3, "Process Message", f"FAIL to Generate Compact log file: {file}") 
                
                convertstatus = False

        elif self.operation == "IN700":
            # print("operation:\t", operation)
            try:
                # Top_cover = df.loc[(df["Unique ID"] == "SCAN SERIAL MB") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                # BN_Screw = df.loc[(df["Unique ID"] == "SCREW Material") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
                MB2TC_01 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.01")
                MB2TC_02 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.02")
                MB2TC_03 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.03")
                MB2TC_04 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.04")
                MB2TC_05 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.05")
                MB2TC_06 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.06")
                MB2TC_07 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.07")
                MB2TC_08 = CAutoFITs_Screw.get_last_valid_row(df, "MB2TC.08")
                
                data = {  
                    "EN": str(Operator), 
                    "Operation": str(self.operation), 
                    "SN": str(self.serial),
                    "BN Top cover": str(self.sub_sn[1]),
                    "BN Screw": str(self.sub_sn[0]),   
                    "Program Name": "Screwing Cover Screws Type1",
                    "Fixture jig": str(self.fixture),
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
                # print(df_output)
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
                
                message_popup(3, "Process Message", f"FAIL to Generate Compact log file: {file}") 
                
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
            while True:
                try:
                    os.rename(file, New_ach)
                    break
                except PermissionError as p:
                    print("PermissionError")
                    print(p)
                    continue
                except Exception as error:
                    print("Exception")
                    print(error)
                    df_output = pd.DataFrame() 
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
            while True:
                try:
                    os.rename(file, New_ach)
                    break
                except PermissionError as p:
                    print(p)
                    continue
                except Exception as error:
                    print(error)
                    df_output = pd.DataFrame() 
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
                     
            df_output = pd.DataFrame() 
            
        return df_output, current_path, CompactPathName

    def UploadDataToFITs(self, dataFrame, current_path, CompactPathName):
        ## Create folder FITS_Log_Fail && FITS_Handcheck_Fail
        FITS_Log_Fail = os.path.join(os.path.dirname(os.path.dirname(current_path)), "FITS_Log_Fail")
        os.makedirs(FITS_Log_Fail, exist_ok=True)
        FITS_Handcheck_Fail = os.path.join(os.path.dirname(os.path.dirname(current_path)), "FITS_Handcheck_Fail")
        os.makedirs(FITS_Handcheck_Fail, exist_ok=True)
    
        model = self.model
        operation = self.operation
        serial = self.serial
        # print(dataFrame.columns.tolist())
        # print(dataFrame.values.tolist()[0])
        parameters = ";".join(dataFrame.columns.tolist())
        values = ";".join(dataFrame.values.tolist()[0])
        
        fn_log = fn_Log(model, operation, parameters, values)
        if fn_log == True:
            message_popup(1, "FITs Log", f"{serial} has been uploaded TO FITS {operation}.")
        else:   
            print('FITs Log Fail:\t', f'{fn_log}')
            message_popup(3, 'FITs Log Fail', f'Serial {serial}\n{fn_log}')
            CAutoFITs_Screw.move_folder(os.path.dirname(current_path), os.path.join(FITS_Log_Fail, os.path.basename(os.path.dirname(current_path))))

    def get_last_valid_row(df, uid):
        ok_df = df.loc[
            (df["Unique ID"] == uid) &
            (df["Status"] == "OK") &
            (df["Value"].isin(["OK", "manualOK"])),
            ["Actual Torque", "Actual Angle", "Status"]
            ]
        if not ok_df.empty:
            return ok_df.tail(1).squeeze().astype(str)
        
        nok_df = df.loc[
            (df["Unique ID"] == uid) &
            (df["Status"] == "NOK") &
            (df["Value"].isin(["NOK", "manualNOK"])),
            ["Actual Torque", "Actual Angle", "Status"]
            ]
        if not nok_df.empty:
            return nok_df.tail(1).squeeze().astype(str)
        
        return None
    
    def check_process_done(self):
        pattren = os.path.join(self.path, "*", f"{self.serial}_*.csv")
        files = glob.glob(pattren)
        if not files:
            print("File not found")
            return None
        file = max(files, key=os.path.getatime)
        temp_path =os.path.join(tempfile.gettempdir(), "log_temp.csv")

        try:
            shutil.copy2(file, temp_path)
            df = pd.read_csv(file)

            if "Unique ID" in df.columns:
                if df["Unique ID"].astype(str).str.contains("Complete Process").any():
                    print(f"Process finished file -> {file}")
                    return file
                else:
                    print(f"Wait process finish file -> {file}")
                    return None
            else:
                raise ValueError("Missing 'Unique ID' column.")
            
        except PermissionError:
            return None
        except Exception as e:
            message_popup(3, "Read csv Error", f"Error file\n{file}\n{e}")
            return None
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e:
                    print(e)

    def clearlog(self):
        self.serial = ""
        self.sub_sn = []
        for item in os.listdir(self.path):
            source_path = os.path.join(self.path, item)
            basename = os.path.basename(source_path) + datetime.now().strftime("%Y-%m-%d %H_%M_%S")
            new_source_path = os.path.join(os.path.dirname(source_path), basename)
            os.rename(source_path, new_source_path)
            destination_path = os.path.join(self.bin_folder, item)
            shutil.move(new_source_path, destination_path)

    def aggregateAllDataAndSaveToFile(self):
        while True:
            self.clearlog()
            serials = scan_serial(self.FITs, self.model, self.operation, self.sub)
            print("main_serial\t", serials["main"])
            if serials["main"] == "quit":
                print("User quit Program")
                quit()
            
            self.serial = serials["main"]
            
            # --- Sub Serial ---
            print("sub_serial\t" ,serials["subs"])
                            
            self.sub_sn = serials["subs"]
            
            callback = send_fi_telegram(self.serial)
            if callback == False:
                message_popup(3, "SQS Connect error", "Can't connect SQS Software, Please contract engineer")
                quit()

            Check_result_telegram(self.serial)

            for i in range(3):
                file = self.findTorqueDataFiles()
                if file:
                    break
                else:
                    print("retry find log {i}")
                    message_popup(3, "File not found", "Please, Check log file in SQS Log folder")
                    continue
                
            minedData, current_path, CompactPathName = self.openDatabaseFile(file)
            # print(minedData) 
            # print(CompactPathName)
            if minedData == None or CompactPathName == "NG":
                print(minedData)
                continue
            if self.FITs.upper() == "ENABLE":
                self.UploadDataToFITs(minedData, current_path, CompactPathName)
                print(f"{self.serial} Finished")

if __name__  == "__main__":
    while True:
        print("START")
        minedData=CAutoFITs_Screw()
        minedData.aggregateAllDataAndSaveToFile()