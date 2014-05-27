"""
Listing files in directories and subdirectories
by Daniel Shiffman.    

This example has three functions:<br />
1) List the names of files in a directory<br />
2) List the names along with metadata (size, lastModified)<br /> 
of files in a directory<br />
3) List the names along with metadata (size, lastModified)<br />
of files in a directory and all subdirectories (using recursion) 
"""
import java.util.Date


def setup():
    # Path
    path = sketchPath
    println("Listing all filenames in a directory: ")
    filenames = listFileNames(path)
    println(filenames)

    println("\nListing info about all files in a directory: ")
    files = listFiles(path)
    for i in range(len(files)):
        f = files[i]
        println("Name: " + f.getName())
        println("Is directory: " + f.isDirectory())
        println("Size: " + len(f)())
        lastModified = Date(f.lastModified()).toString()
        println("Last Modified: " + lastModified)
        println("-----------------------")

    println(
        "\nListing info about all files in a directory and all subdirectories: ")
    ArrayList < File > allFiles = listFilesRecursive(path)

    for f in allFiles:
        println("Name: " + f.getName())
        println("Full path: " + f.getAbsolutePath())
        println("Is directory: " + f.isDirectory())
        println("Size: " + len(f)())
        lastModified = Date(f.lastModified()).toString()
        println("Last Modified: " + lastModified)
        println("-----------------------")

    noLoop()
# Nothing is drawn in this program and the draw() doesn't loop because
# of the noLoop() in setup()


def draw():
# This function returns all the files in a directory as an array of Strings
    listFileNames(dir)
    file = File(dir)
    if file.isDirectory():
        names = file.list()
        return names
    else:
        # If it's not a directory
        return null

# This function returns all the files in a directory as an array of File objects
# This is useful if you want more info about the file
    listFiles(dir)
    file = File(dir)
    if file.isDirectory():
        files = file.listFiles()
        return files
    else:
        # If it's not a directory
        return null

# Function to get a list of all files in a directory and all subdirectories
ArrayList < File > listFilesRecursive(dir)
    ArrayList < File > fileList = ArrayList < File > ()
    recurseDir(fileList, dir)
    return fileList
# Recursive function to traverse subdirectories


def recurseDir(ArrayList < File > a, dir):
    File file = File(dir)
    if file.isDirectory():
        # If you want to include directories in the list
        a.add(file)
        File[] subfiles = file.listFiles()
        for i in range(len(subfiles)):
            # Call this function on all files in this directory
            recurseDir(a, subfiles[i].getAbsolutePath())

    else:
        a.add(file)

