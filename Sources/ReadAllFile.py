import pandas as pd
import glob
import os

def check_pd_filter(input):
    if isinstance(input, pd.Series) and input.empty:
        return None
    elif pd.isna(input):
        return None
    else:
        return input 
    
if __name__ == "__main__":
    csv_filename = "Data_POLYGON_PV_S400A.csv"
    file_path = "D:\\Data Result\\New folder"
    path_extend = "**\\*.csv"
    
    allfiles = glob.glob("D:\\Data Result\\New folder\\**\\*.csv")
    for csvfile in allfiles:
        print(csvfile)
        df = pd.read_csv(csvfile)
        
        operation = "S400A"
        Product_Id = df["Product Id"].tail(1).squeeze()
        try:
            Operator = str(int(df["Operator"][df["Operator"].first_valid_index()]))
        except:
            Operator = "519723"
            
        Scan_sub_1 = df.loc[(df["Description"] == "Scan sub 1") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
        BC1_01 = df.loc[(df["Unique ID"] == "BC1.01") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC1_02 = df.loc[(df["Unique ID"] == "BC1.02") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC1_03 = df.loc[(df["Unique ID"] == "BC1.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC1_03 = df.loc[(df["Unique ID"] == "BC1.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC1_04 = df.loc[(df["Unique ID"] == "BC1.04") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        Scan_sub_2 = df.loc[(df["Description"] == "Scan sub 2") & (df["Status"] == "OK"), "Value"].tail(1).squeeze()
        BC2_01 = df.loc[(df["Unique ID"] == "BC2.01") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC2_02 = df.loc[(df["Unique ID"] == "BC2.02") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC2_03 = df.loc[(df["Unique ID"] == "BC2.03") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC2_04 = df.loc[(df["Unique ID"] == "BC2.04") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()
        BC2_05 = df.loc[(df["Unique ID"] == "BC2.05") & (df["Status"] == "OK") & (df["Value"] == "OK"), ["Actual Torque", "Actual Angle", "Status"]].tail(1).squeeze()

        data = {
            "SN Scanner": Product_Id,  
            "EN": Operator, 
            "Operation": operation,      
            "Program Name": " S400 old and LATM",
            "SN Fold Mirror": check_pd_filter(Scan_sub_1),
            "PeakTorque #1": check_pd_filter(BC1_01["Actual Torque"]),
            "TotalAngle #1": check_pd_filter(BC1_01["Actual Angle"]),
            "Result #1": check_pd_filter(BC1_01["Status"]),
            "PeakTorque #2": check_pd_filter(BC1_02["Actual Torque"]),
            "TotalAngle #2": check_pd_filter(BC1_02["Actual Angle"]),
            "Result #2": check_pd_filter(BC1_02["Status"]),
            "PeakTorque #3": check_pd_filter(BC1_03["Actual Torque"]),
            "TotalAngle #3": check_pd_filter(BC1_03["Actual Angle"]),
            "Result #3": check_pd_filter(BC1_03["Status"]),
            "PeakTorque #4": check_pd_filter(BC1_04["Actual Torque"]),
            "TotalAngle #4": check_pd_filter(BC1_04["Actual Angle"]),
            "Result #4": check_pd_filter(BC1_04["Status"]),
            "SN LATM": check_pd_filter(Scan_sub_2),
            "PeakTorque #5": check_pd_filter(BC2_01["Actual Torque"]),
            "TotalAngle #5": check_pd_filter(BC2_01["Actual Angle"]),
            "Result #5": check_pd_filter(BC2_01["Status"]),
            "PeakTorque #6": check_pd_filter(BC2_02["Actual Torque"]),
            "TotalAngle #6": check_pd_filter(BC2_02["Actual Angle"]),
            "Result #6": check_pd_filter(BC2_02["Status"]),
            "PeakTorque #7": check_pd_filter(BC2_03["Actual Torque"]),
            "TotalAngle #7": check_pd_filter(BC2_03["Actual Angle"]),
            "Result #7": check_pd_filter(BC2_03["Status"]),
            "PeakTorque #8": check_pd_filter(BC2_04["Actual Torque"]),
            "TotalAngle #8": check_pd_filter(BC2_04["Actual Angle"]),
            "Result #8": check_pd_filter(BC2_04["Status"]),
            "PeakTorque #9": check_pd_filter(BC2_05["Actual Torque"]),
            "TotalAngle #9": check_pd_filter(BC2_05["Actual Angle"]),
            "Result #9": check_pd_filter(BC2_05["Status"]),
            "Result": "None"
        }
        # Convert the dictionary to a DataFrame
        df_output = pd.DataFrame([data])
        result_columns = ["Result #1", "Result #2", "Result #3", "Result #4", "Result #5", "Result #6", "Result #7", "Result #8", "Result #9"]
        df_output[result_columns] = df_output[result_columns].replace("OK", "PASS")
        df_output["Result"] = df_output[result_columns].apply(lambda x: "PASS" if all(x == "PASS") else "FAIL", axis=1)
        
        if os.path.exists(csv_filename):
            df_output.to_csv(csv_filename, mode="a", header=False,index=False)
        else:
            df_output.to_csv(csv_filename, mode="w", header=True, index=False)
    
    print("Complete Record All Data")    
        