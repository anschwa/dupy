# -*- coding: utf-8 -*-

"""
Dupy: Find and remove duplicate files.
file: dupy.py
author: Adam Schwartz
created: 2014-07-14 12:11:32

Based on Sebastien Sauvage's doublesdetector.py
http://sebsauvage.net/python/doublesdetector.py

Usage:
    dirs = ['tests/one', 'tests/two']
    get_dups(dirs)
"""

import os.path
from os import stat
import sha


def fileSHA(filepath):
    """ Compute SHA (Secure Hash Algorythm) of a file.
        Input : filepath : full path and name of file (eg. 'c:\windows\emm386.exe')
        Output : string : contains the hexadecimal representation of the SHA of the file.
                          returns '0' if file could not be read (file not found, no read rights...)
    """

    try:
        file = open(filepath, 'rb')
        digest = sha.new()
        data = file.read(65536)
        while len(data) != 0:
            digest.update(data)
            data = file.read(65536)
        file.close()
    except:
        return '0'
    else:
        return digest.hexdigest()


def detect_doubles(directories):
    fileslist = {}
    # Group all files by size (in the fileslist dictionary)
    for directory in directories:
        directory = os.path.abspath(directory)
        # scan_msg = 'Scanning directory '+directory+'...'
        os.path.walk(directory, callback, fileslist)

    # comp_msg = 'Comparing files...'
    # Remove keys (filesize) in the dictionnary which have only 1 file
    for (filesize, listoffiles) in fileslist.items():
        if len(listoffiles) == 1:
            del fileslist[filesize]

    # Now compute SHA of files that have the same size,
    # and group files by SHA (in the filessha dictionnary)
    filessha = {}
    while len(fileslist) > 0:
        (filesize, listoffiles) = fileslist.popitem()
        for filepath in listoffiles:
            # print '.' (progress update)
            sha = fileSHA(filepath)
            if sha in filessha:
                filessha[sha].append(filepath)
            else:
                filessha[sha] = [filepath]
    if '0' in filessha:
        del filessha['0']

    # Remove keys (sha) in the dictionnary which have only 1 file
    for (sha, listoffiles) in filessha.items():
        if len(listoffiles) == 1:
            del filessha[sha]
    # return list of hashes and progress messages
    return filessha


def callback(fileslist, directory, files):
    # print '.' (progress update)
    for fileName in files:
        filepath = os.path.join(directory, fileName)
        if os.path.isfile(filepath):
            filesize = stat(filepath)[6]
            if filesize in fileslist:
                fileslist[filesize].append(filepath)
            else:
                fileslist[filesize] = [filepath]


def get_dups(dir_list):
    doubles = detect_doubles(dir_list)

    big_dups = [doubles[filesha] for filesha in doubles.keys()]

    map(lambda n: n.insert(0, 'The following files are identical:'), big_dups)
    map(lambda x: x.append(''), big_dups)  # add empty item to each sublist

    # flatten / merge the nested list
    return [item for subitem in big_dups for item in subitem]
