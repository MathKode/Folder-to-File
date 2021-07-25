# Folder-to-File
An little code which turn a a folder and his file into one file .ftf and do the inverse (Like a .zip but whitout the compression ≈ .tar)

# Installation

It's only to linux. You need these libraries :
`````
pip3 install argparse
```````
````
pip3 install binascii
````````
````
pip3 install os
``````

# Command

Create a .ftf file :
````
python3 main.py -f FILE_NAME
``````

Open a .ftf file :
````
python3 main.py -f FILE_NAME
``````

***Warning : this code over write, take attention you haven't a folder name like the FILE-NAME***

# How it's work

1) Create

At first, this code change the name of the file with space or ' (to avoid an erreur with the other commands)

Then, he create 2 lists, directory (which contains the path of directory) and file (which contains the paths of the file). Like : 
````
directory = ["folder","folder/folder2"] file = ["folder/file1.txt","folder/folder2/file2.txt"]
```````
At third, he stocks this informations into a result vr :

result = "FTFO" (type of file) + Len_directory_el + "S" + directory_el + "\" 

What made with the last example :

`````
result = FTF0 + 6 + S + folder + 14 + S + folder/folder2 + \
result = FTF06Sfolder14Sfolder/folder2\
````````

After, this code get the hexa of every file in file_list and modify result like :

result += Len_file_path + "S" + file_path + Len_file_hexa + "S" + hexa

With the last example this done (if hexa_file1.txt = e465 and hexa_file2 = 6fffa) :

``````
To file1.txt :
result += 16 + S + folder/file1.txt + 4 + S + e465
To file2.txt :
result += 24 + S + folder/folder2/file2.txt + 5 + S + 6fffa
```````

2) Reading a file

To read the file, the code recreate the list directory :
-The S is useful because he allows my code to recognize when the len (number) is finish
