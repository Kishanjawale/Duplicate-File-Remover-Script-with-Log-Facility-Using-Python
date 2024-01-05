import os
from sys import *
import time 
import hashlib
import datetime

Date= str(datetime.date.today())
Time_t1 = time.localtime()
current_time = str(time.strftime("%H-%M-%S",Time_t1))
current_time1 = str(time.strftime("%H:%M:%S",Time_t1))    
filename=str(str(current_time)+str(Date)) 
File1= open( str(filename +".csv"),"w")

def DeleteFiles(Dict1):
    Results= list(filter(lambda x:len(x)>1,Dict1.values()))
    icnt=0
    if len(Results)>0:
        for result in Results:
            for Subresult in result:
                icnt+=1
                if icnt >=2:
                    os.remove(Subresult)
            icnt=0  
    else:
        print("NO Duplicate Files Found..") 

def hashfile(path,blocksize=1024):
    Afile= open(path,'rb')
    hasher= hashlib.md5()
    buffer= Afile.read(blocksize)

    while len(buffer)>0:
        hasher.update(buffer)
        buffer=Afile.read(blocksize)
    Afile.close()

    return hasher.hexdigest()


def PrintResult(Dict1):
    Results= list(filter(lambda x:len(x)>1,Dict1.values()))
    
    if len(Results)>0:
        print("Duplicate Found:")
        print("The Following Files Are Duplicate")
        for result in Results:
            for Subresult in result:
                print('\t\t\%s'% Subresult)
    else:
        print("NO Duplicate Files Found..") 


def WriteResult(Dict1):
    Results= list(filter(lambda x:len(x)>1,Dict1.values()))
    
    if len(Results)>0:
        File1.write("Duplicate Found:\n")
        File1.write("The Following Files Are Duplicate:\n")
        
        for result in Results:
            for Subresult in result:
                File1.write('\t\t\%s'% Subresult +"\n")
    else:
        File1.write("NO Duplicate Files Found..") 


def FindDuplicate(path):
    flag = os.path.isabs(path)
    
    if flag==False:
        flag=os.path.abspath(path)
    
    Exists = os.path.isdir(path)

    Duplicate={}
    if Exists:
        for DirName ,Subdirs,FileList in os.walk(path):
            print("Current Folder is :"+DirName)
            for Filen in FileList:
                path=os.path.join(DirName,Filen)
                file_hash=hashfile(path)

                if file_hash in Duplicate:
                    Duplicate[file_hash].append(path)
                else:
                    Duplicate[file_hash] = [path]
        return Duplicate
    else:
        print("Invalid Path.....")


def main():
    print("_____Automation Script By Kishan Jawale_____")
    print("Application Name:",argv[0])
    
    if(len(argv)!=2):
        print("Error:Invalid Input...")
        exit()
    if(argv[1] =="-h"or argv[1]=="-H"):
        print("This script is used to traverse a specific directory and delete duplicate files")
        exit()

    if(argv[1] =="-u"or argv[1]=="-U"):
        print("Usage: AppliactionName Absolute_Path_Of_Directory Extention")
        exit()
    try:
        Arr={}
        StartTime = time.time()
        
        Arr = FindDuplicate(argv[1])
        
        PrintResult (Arr)
        DeleteFiles(Arr)
        WriteResult(Arr)

        EndTime= time.time()
        print("Took %s Seconds to Delete The Files"%(EndTime-StartTime))
        File1.write("Took %s Seconds to Delete The Files"%(EndTime-StartTime))


    except ValueError:
        print("Error: Invalid Data Type of input....")
    
    except Exception as E:
        print("Error: Invalid Input...",E)

if __name__=="__main__":
    main()