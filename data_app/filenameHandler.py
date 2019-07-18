import os
import sys

DIR = ""

def checkArgs():
    if len(sys.argv) != 3:
        print("Usage: filenameHandler.py test [dir]")
        print("for one dir test")
        print("or")
        print("Usage: filenameHandler.py run [dir]")
        print("for run process")
        exit(1)
    
    if sys.argv[1] == "test":
        return 0
    elif sys.argv[1] == "run":
        return 1

def getList(dir):
    originList = os.listdir(dir)
    newList = []
    

    for file in originList:
        if ".pdf" not in file:
            print("Error:" + file + "has not PDF file?")
            exit(2)

        newName = file.replace(".pdf", "").replace("-已轉檔", "").replace("-已融合", "")
        newList.append(newName.split("-"))
    
    finalList = []

    for nameList in newList:
        if len(nameList[1]) == 1:
            nameList[1] = "0" + nameList[1]
        if len(nameList[2]) == 1:
            nameList[2] = "0" + nameList[2]
        finalName = nameList[0] + "0" + nameList[1] + "0" + nameList[2] + ".pdf"
        finalList.append(finalName)

    # for i in range(len(originList)):
    #     print(originList[i])
    #     print(finalList[i])
    #     print()

    for l in finalList:
        print(l)

    return [originList, finalList]

def rewirte(oldList, newList):
    pdir = DIR + "/"
    for i in range(len(oldList)):
        os.rename(pdir + oldList[i], pdir + newList[i])
        print(pdir + oldList[i] + " -> " + pdir + newList[i])
    
    print()
    print("DONE!")


if __name__ == "__main__":
    mode = checkArgs()
    DIR = sys.argv[2]
    if mode == 0:
        getList(DIR)
    elif mode == 1:
        plist = getList(DIR)
        rewirte(plist[0], plist[1])
    else:
        print("Error!")
        exit(3)
