import openpyxl
import numpy as np

INPUT_EXCEL_FILENAME = "Data_Handcrafted/ExampleGrid_100Percent.xlsx" #MUST BE xlsx
OUTPUT_TXT_FILENAME = "ConvertedExcelFile.txt" #MUST BE TXT 
DEFAULT_DATA_DIRECTORY = "/Data/"

def ExcelToTxtConverter(inputFilePath, outputFilePath):
    print("Starting ExcelToTxtConverter")

    # Load the Excel file
    workbook = openpyxl.load_workbook(inputFilePath)
    sheet = workbook.active

    # Initialize a list to store the coordinates
    coordinates_list = []
    for row in sheet.iter_rows(values_only=True): # Iterate through each cell in the sheet
        coordinates_row = []
        for cell in row:
            # Extract coordinates from each cell
            if cell is None or cell == '?': #Unknown shall be 0
                coordinates_row.append(0) 
            elif (cell >= 0 and cell <= 100):
                coordinates_row.append(cell)
            else:
                coordinates_row.append(0) 
        coordinates_list.append(coordinates_row)

    # Convert the list to a NumPy array
    coordinates_array = np.array(coordinates_list)

    #CONVERT and SAFE TXT FILE
    print(f"Converted: '{inputFilePath}' and saved to TXT: '{outputFilePath}'\nValues:\n{coordinates_array}")
    np.savetxt(outputFilePath, coordinates_array, fmt='%d')

if __name__ == '__main__':
    inputFilePath = INPUT_EXCEL_FILENAME
    outputFilePath = OUTPUT_TXT_FILENAME
    ExcelToTxtConverter(inputFilePath, outputFilePath)
