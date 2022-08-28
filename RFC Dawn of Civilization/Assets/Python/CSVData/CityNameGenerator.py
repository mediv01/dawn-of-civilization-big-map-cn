# coding:utf-8

def csvwrite_norownum(csvmap, filename):
    file = open(filename, 'w',newline='')
    import csv
    writer = csv.writer(file)
    try:
        for y in range(len(csvmap)):
            lRow = []
            for x in range(len(csvmap[y])):
                lRow.append(csvmap[y][x])
            writer.writerow(lRow)
    finally:
        file.close()

def csvreader_withrownum(filename):

    import csv
    return_map = []

    file = ''
    try:
        file = open(filename, 'r')
        f_csv = csv.reader(file)
        for row in f_csv:
            return_map.append(row)

    finally:
        if file:
            file.close()

    return return_map
    pass

def utf8encode2(s):
    s1 = ""
    for i in range(len(s)):
        id = ord(s[i])
        if (id>128):
            s1 = s1 + u"&#"  + str(id) + ";"
        else:
            s1 = s1 + s[i]
    return s1


def main():
    CVGAMECORE_PYTHON_CSV_PATH = ''
    cityname = csvreader_withrownum(CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsvCN.csv")
    for i in range(len(cityname)):
        for j in range(len(cityname[0])):
            cityname[i][j] = utf8encode2(cityname[i][j])
            #cityname[i][j] = utils.utf8encode2(u'测试'.encode("gbk"))
    
    csvwrite_norownum(cityname , CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsvCN_Translate.csv")
    
    cityname = csvreader_withrownum(CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsvEN.csv")
    for i in range(len(cityname)):
        for j in range(len(cityname[0])):
            cityname[i][j] = utf8encode2(cityname[i][j])
            #cityname[i][j] = utils.utf8encode2(u'测试'.encode("gbk"))
    
    csvwrite_norownum(cityname , CVGAMECORE_PYTHON_CSV_PATH + "CityNameDataCsvEN_Translate.csv")
    
main()