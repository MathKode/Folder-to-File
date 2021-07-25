import argparse
import binascii
import os

parser = argparse.ArgumentParser(description="Code to turn a folder and his file into one file .ftf and do the inverse")

parser.add_argument("-f","--file",type=str,help="The name/way of the folder or the one of the .ftf file")
parser.add_argument("-r","--replace",type=str,default="-",help="The caractere who replace the space and the ' in the name of the files")

args = parser.parse_args()

def _open_(name):
    #Output : b2b3de2076582858505d909a4989422ff3af...
    file = open(name,'rb')
    content = file.read()
    file.close()
    hexa = str(binascii.hexlify(content))[2:-1]
    return hexa

def _create_(name,hexa):
    #Input : 89504e470d0a1a0
    hexa = binascii.unhexlify(hexa) #Transform into : b'\x89PNG\r\n\x1a\n\x00\x00\
    file = open(name,'wb')
    file.write(hexa)
    file.close()

def _list(chemin):
    #Do an ls on linux and dir on Windows
    """
    if os.name == "nt":
        cm = os.popen(f"dir {chemin}")
    else:
    """
    if True:
        cm = os.popen(f"ls -l {chemin}")
        r = cm.read().split('\n')
        del r[0] #total 512
        del r[-1] # ''
        file = []; directory=[]
        for i in r :
            if i[0] == '-':file.append(i.split(' ')[-1])
            else:directory.append(i.split(' ')[-1])
        return file, directory

def del_space(file,replace):
    #Rename all files and folder with space (' ' -> '-')
    ls = [file]
    for i in ls:
        cm = os.popen(f"ls {i}")
        content = cm.read().split('\n')
        del content[-1]
        for j in content:
            if ' ' in list(j):
                j2 = str(replace).join(j.split(" "))
                print(i,j,j2)
                os.system(f'mv "{i}/{j}" "{i}/{j2}"')
                j = j2
            if "'" in list(j):
                j2 = str(replace).join(j.split("'"))
                print(i,j,j2)
                os.system(f'mv "{i}/{j}" "{i}/{j2}"')
            cm = os.popen(f"ls -l {i}")
            r = cm.read().split('\n')
            del r[0] #total 512
            del r[-1] # ''
            file = []; directory=[]
            for t in r :
                if t[0] == 'd': ls.append(f"{i}/{t.split(' ')[-1]}")
            
def _create(file_,replace):
    #TREE
    del_space(file_,replace)
    #List the content of the file
    directory = [file_]
    file = []
    for i in directory:
        f, d = _list(i)
        for j in f:
            file.append(f"{i}/{j}")
        for j in d:
            directory.append(f"{i}/{j}")
    #print(file)
    #print(directory)
    result = "FTFO"
    for i in directory:
        result += str(len(i)) + "S" + str(i)
    result += str("\ ")[0]
    for i in file:
        result += str(len(i)) + "S" + str(i)
        hexa = _open_(i)
        result += str(len(hexa)) + "S" + str(hexa)
    #print(result)
    file = open(f"NEW_{file_}.ftf","w")
    r = []
    for i in range(int(len(result)/10000)+1):
        r.append(result[i*10000:(i+1)*10000])
    file.write("\n".join(r))
    file.close()
    print("Creation is done")

def _reverse(file_):
    file = open(file_,"r")
    content = "".join(file.read().split("\n"))
    file.close()
    if content[:4] != "FTFO":
        print('It s not a ftf file')
        exit(0)
    content = content[4:]
    print(content)
    directory = []
    while True:
        t = ""
        find = True
        while find:
            if content[0] == "S":
                print(t)
                t = int(t)
                find = False
            else :
                t += content[0]
            content = content[1:]
        directory.append(content[:t])
        content = content[t:]
        if content[0] == str("\ ")[0]:
            content = content[1:]
            break
    print(directory)

    for i in directory:
        os.system(f"mkdir {i}")
    
    file = []
    while True:
        t = ""
        find = True
        while find:
            if content[0] == "S":
                t = int(t)
                find = False
            else :
                t += content[0]
            content = content[1:]
        chemin = content[:t]
        content = content[t:]
        find = True
        t = ""
        while find:
            if content[0] == "S":
                t = int(t)
                find = False
            else :
                t += content[0]
            content = content[1:]
        hexa = content[:t]
        file.append([chemin,hexa])
        content = content[t:]
        if len(content) == 0:
            break
    
    print(file)
    for i in file:
        _create_(i[0],i[1])

    print("Restauring is done")
    
def main(file,replace):
    if file.split('.')[-1] == "ftf":
        _reverse(file)
    else :
        _create(file,replace)

if __name__ == "__main__":
    main(args.file,args.replace)