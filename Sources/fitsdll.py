from win32com.client import Dispatch 
from datetime import datetime
import glob
import re
import os

def Convert_Data(array_value):
    pack_value = ";".join(array_value)
    return pack_value

def fn_Handshake(model: str, operation : str, serial : str, revision="2.90"):
    print("fn_Handshake")
    lib = Dispatch("FITSDLL.clsDB") 

    fn_initDB = lib.fn_InitDB(model, operation, revision, "dbInnoviz")
    if fn_initDB == "True":
        fn_handshake = lib.fn_Handshake(model, operation, revision, serial)
        if fn_handshake == "True":
            del lib
            return True
        else:
            del lib
            return fn_handshake
    else:
        del lib
        return fn_initDB

def fn_Log(model: str, operation : str, parameters : str, values : str, revision="2.90"):
    list_parameters = {}
    lib = Dispatch("FITSDLL.clsDB")
    ## Define Shift 
    start_day_shift = datetime.strptime("07:00","%H:%M").time()
    end_day_shift = datetime.strptime("19:00","%H:%M").time()
    if start_day_shift <= datetime.now().time() <= end_day_shift:
        list_parameters["Shift"] = "DAY"
    else:
        list_parameters["Shift"] = "NIGHT"
    parameters = parameters + ";" + "Shift"
    values =  values + ";" + list_parameters["Shift"]
    fn_initDB = lib.fn_InitDB(model,operation, revision ,"dbInnoviz")
    if fn_initDB == "True":
        # print(parameters)
        # print(values)
        fn_log = lib.fn_Log(model, operation, revision, parameters, values, ";")
        if fn_log == "True":
            del lib
            return True
        else:
            del lib
            return fn_Log
    else: 
        del lib
        return False

def fn_Query(model: str, operation : str, serial : str, query_parameters : str, revision="2.90"):
    lib = Dispatch("FITSDLL.clsDB")
    query_array = []

    fn_initDB = lib.fn_InitDB(model, operation, revision, "dbInnoviz")
    if fn_initDB == "True":
        for param in query_parameters.split(';'):
            fn_query = lib.fn_Query(model, operation, revision, serial, param, ";")
            fn_query = str(fn_query)
            query_values = fn_query.replace("-;","").replace(";-","").replace("-","")
            query_array.append(query_values)
        query_result = ";".join(query_array)
        del lib
        return query_result
    else:
        del lib
        return False
    
def FitsDebugging():
    FitsLog_Dir = "C:\\TEMP\\FITSDLL_LOG\\*.log"
    datetime_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    newest_datetime = None
    newest_log = None

    files = glob.glob(FitsLog_Dir)
    max_file = max(files, key=os.path.getctime)
    with open(max_file, "r") as read_log:
        for line in read_log:
            match = re.search(datetime_pattern, line)
            if match:
                current_datetime = datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
                
                if newest_datetime is None or current_datetime > newest_datetime:
                    newest_datetime = current_datetime
                    newest_log = line

    if newest_datetime:
        # print("Newest Log:\t", newest_log)
        output = newest_log.split("\n")[0]
    else:
        # print("No valid log")
        output = "No valid log"

    return output

# print(fn_Handshake("Main line", "IN700", "CIN251700000"))