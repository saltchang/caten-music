import xlrd, json, sys

inFile = sys.argv[1]
outFile = sys.argv[2]
data_start = str(int(sys.argv[3]) - 1)

def usageCheck():
    if len(sys.argv) != 4:
        print("Usage: excel_to_json.py [inputFile.xlsx] [outputFile.json] [int: row of first data]")
        exit(1)

def xlsxToJSON(fileURL_, data_start_):
    fileURL = fileURL_

    workbook = xlrd.open_workbook(fileURL)
    booksheet = workbook.sheet_by_index(0)  # 用索引取第一個sheet

    data_start = data_start_  # 第一筆資料的row
    data_num = booksheet.nrows # 最後一筆資料的row

    data = []

    for i in range(int(data_start), int(data_num)):
        song = {
            "id_num": str(booksheet.cell_value(i, 0)),
            "song_title": str(booksheet.cell_value(i, 1)),
            "from_where": str(booksheet.cell_value(i, 2))
        }
        data.append(song)
    
    return data


def data_export(data, outFileURL_):
    out_file = open(outFileURL_, "w")
    out_file.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    usageCheck()
    data = xlsxToJSON(inFile, data_start)
    data_export(data, outFile)
    print("\nConvert finished!\n")
