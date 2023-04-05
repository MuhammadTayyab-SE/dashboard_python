import pandas as pd
import re

def read_dataframe(apt, db_xls):
    # reading dataframe
    df = pd.read_excel(db_xls,sheet_name=apt)
    # checking if the "ATT&CK Technique" column exists in the dataframe
    if "ATT&CK Technique" not in df.columns:
        # raise Exception(f"The 'ATT&CK Technique column doesn't exit in the sheet {sheet}")
        tempdf = df.dropna().reset_index(drop=True)
        tempdf.columns = tempdf.iloc[0].tolist()
        tempdf = tempdf[1:]
        df = tempdf
    return df

def convert_to_list(mapping_elements):
    for element, dit in mapping_elements.items():
        for key, apts in dit.items():
            dit[key] = list(apts)
    return mapping_elements

def get_sub_technique(df,idx):
    df = df.copy()
    df.set_index("ATT&CK Technique", inplace=True)
    return str(df.loc[idx]["Technique/Sub-Technique Title"])

def generate_report(source_file, database_file, output_file):    
    
    # loading the target source file
    xls = pd.ExcelFile(source_file)

    # Loading the database file
    db_xls = pd.ExcelFile(database_file)

    df1 = pd.read_excel(xls, "Sysmon Events")
    df2 = pd.read_excel(xls, "Sigma Rules")

    detection_lst = df1["Detection Rule"].tolist()
    
    # As Sigma rules can be empty so putting the check 
    # to detect whether the sigma rule is empty
    if df2["Tags"].count()!=0:
        tags_lst = df2["Tags"].tolist()
        detection_lst.extend(tags_lst)
        
    # defining the regular expression to extract ID from the string
    regex = "T?t?[0-9]{4}"

    ids = []
    # find all ids present in the line
    for line in detection_lst:
        match = re.findall(regex, line)
        if (len(match) > 0):
            ids.append(re.findall(regex, line)[0])
            
    # ids = [re.findall(regex, line)[0] for line in detection_lst ]
    
    # convert all values with 't' to 'T', in order to maintain the symmetry
    ids = [id.capitalize() for id in ids]

    # convert all database sheet names in
    database_sheets_list = db_xls.sheet_names

    # preparing the dictionary for mapping of id with the sheet name
    mapping_dictionary = dict()
    for idx in ids:
        mapping_dictionary[idx] = dict()

    # iterate through the all sheets in database
    for sheet in database_sheets_list:
        try:
            
            # reading single sheet into dataframe
            df = read_dataframe(sheet, db_xls)
                
            # coverting the ATT&CK Technique column to the list
            all_attacks_list = df["ATT&CK Technique"].tolist()

            # taking insersection of two list  
            common_elements = list(set(ids).intersection(all_attacks_list))
            
           # adding these common elements into dictionary to the specifc index
            sub_technique = ""

            for element in common_elements:
                sub_technique = get_sub_technique(df, element)
                # if sub technique is already added
                if len(mapping_dictionary[element].keys()):
                    mapping_dictionary[element][sub_technique].add(sheet)
                    
                # add the sub technique
                else:
                    mapping_dictionary[element] = {sub_technique:set()}
                    mapping_dictionary[element][sub_technique].add(sheet)
            
        except Exception as e:
            print(f"An error occurred while process sheet {sheet}: {e}")

    # removing data redundancy
    mapping_dictionary = convert_to_list(mapping_elements=mapping_dictionary)
    
    #  saving data into .csv file
    save_in_file(output_file, mapping_dictionary=mapping_dictionary)

def save_in_file(file_name, mapping_dictionary):
    # Saving data to csv file
    file = open(file_name,'w')
    file.write("ID, " +"Sub Techinque," +"Files containig ID\n")
    for id_key, dit in mapping_dictionary.items():
        output_string = id_key+","
        if len( mapping_dictionary[id_key].keys() ):
            for sub_technique, apts in dit.items():
                output_string = output_string + sub_technique
                apt_string = ','.join(str(e) for e in apts)
                file.write(output_string + ',' + apt_string + "\n")
        else:
            file.write(id_key +"," + "\n")
        
    file.close()

