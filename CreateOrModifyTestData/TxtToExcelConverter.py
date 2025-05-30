import os
import pandas as pd
import numpy as np

#This template takes 3 files and creates / overwrites a new excel file with the right coloring and spacing for viewing such a large map


DATA_FILEPATH = os.getcwd() + '/Data/'
DATA_FILEPATH = ''
filepath1 = '151x151_100Percent_InputMap.txt'
filepath2 = '2x16_ResultMap.txt'
filepath3 = '2x16_TouchdownPos.txt'

data1 = np.loadtxt(DATA_FILEPATH + filepath1, dtype=int)
data2 = np.loadtxt(DATA_FILEPATH + filepath2, dtype=int)
data3 = np.loadtxt(DATA_FILEPATH + filepath3, dtype=int)

# Create ExcelWriter object
excel_writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

# Convert numpy arrays to pandas DataFrames and write them to separate worksheets
df1 = pd.DataFrame(data1)
df1.to_excel(excel_writer, sheet_name=filepath1, index=False, header=False)

df2 = pd.DataFrame(data2)
df2.to_excel(excel_writer, sheet_name=filepath2, index=False, header=False)

df3 = pd.DataFrame(data3)
df3.to_excel(excel_writer, sheet_name=filepath3, index=False, header=False)




# Get the xlsxwriter workbook and worksheet objects
workbook  = excel_writer.book

# Add a format for highlighting cells with values greater than 5, for example
formatYellow = workbook.add_format({'bg_color': '#FFFF00', 'font_color': '#000000'})
formatRed = workbook.add_format({'bg_color': '#FF0000', 'font_color': '#000000'})
formatGreen = workbook.add_format({'bg_color': '#00FF00', 'font_color': '#000000'})
formatBlue = workbook.add_format({'bg_color': '#00FFFF', 'font_color': '#000000'})
formatGray = workbook.add_format({'bg_color': '#808080', 'font_color': '#000000'})
formatWhite = workbook.add_format({'bg_color': '#FFFFFF', 'font_color': '#000000'})
formatDefault = workbook.add_format()

for sheet_name in excel_writer.sheets:
    #Set size of a columns
    excel_writer.sheets[sheet_name].set_column('A:ZZ999', 3)  
    #Zoom out
    excel_writer.sheets[sheet_name].set_zoom(18)
    excel_writer.sheets[sheet_name].set_zoom(25)
    # Apply the conditional formatting rule
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                             {'type': 'cell', 'criteria': '=', 'value': 0,'format': formatRed},
                             )
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                             {'type': 'cell', 'criteria': '=', 'value': 1,'format': formatGreen},
                             )
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                             {'type': 'cell', 'criteria': '=', 'value': 2,'format': formatYellow},
                             )
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                             {'type': 'cell', 'criteria': '=', 'value': 3,'format': formatBlue},
                             )
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                             {'type': 'cell', 'criteria': '=', 'value': 4,'format': formatGray}
                             )
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                                 {'type': 'blanks', 'format': formatWhite})
    excel_writer.sheets[sheet_name].conditional_format('A1:ZZ999', 
                                 {'type': 'blanks', 'format': formatDefault})

# Save the Excel file
excel_writer.close()

print("Finished writing Excel")