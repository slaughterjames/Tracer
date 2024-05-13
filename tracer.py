#! /usr/bin/env python3
'''
Tracer v0.1 - Copyright 2024 James Slaughter,
This file is part of Tracer v0.1.

Tracer v0.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Tracer v0.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tracer v0.1.  If not, see <http://www.gnu.org/license>.
'''

#python import
import sys
import os
import argparse
import difflib
from bs4 import BeautifulSoup
from termcolor import colored

#programmer generated imports
from controller import controller
#from fileio import fileio

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    print ('Usage: [required] --logdir --domain [optional] --output --debug --help')
    print ('Example: /opt/tracer/tracer.py --logdir /home/scalp/differlogs --domain domain.com --output /your/directory --debug')
    print ('Required Arguments:')
    print ('--logdir - Directory where the log files of interest are.')
    print ('--domain - Domain to trace accross time.')
    print ('Optional Arguments:')
    print ('--output - Choose where you wish the output to be directed')
    print ('--debug - Prints verbose logging to the screen to troubleshoot issues with a Differ installation.')
    print ('--help - You\'re looking at it!')
    sys.exit(-1)
            
'''
Parse() - Parses program arguments
'''
def Parse(args):        
    parser = argparse.ArgumentParser(description='Process some program arguments.')

    parser.add_argument('--logdir', help='Directory where the log files of interest are.')
    parser.add_argument('--domain', help='Domain to trace accross time.')
    parser.add_argument('--output', help='The output location')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    parser.add_argument('--usage', action='store_true', help='Display program usage.')

    args = parser.parse_args()  

    print ('[*] Arguments: ')
    if args.usage:
        return -1

    if args.logdir:        
        CON.logdir = args.logdir
        print ('logdir: ', CON.logdir)

    if args.domain:
        CON.domain = args.domain       
        print ('domain: ' + CON.domain) 
           
    if args.output:
        #This is an optional param and needs to be checked at read time
        CON.output = args.output
        print ('output: ', CON.output)
        if len(CON.output) < 3:
            if not (CON.output == '<>'):
                print (colored('[x] output must be a viable location.', 'red', attrs=['bold']))
                print ('')
                return -1

    if args.debug:
        CON.debug = True
        print('debug: ', CON.debug)

    if (len(CON.logdir) < 3):
        print (colored('[x] logdir is a required argument.', 'red', attrs=['bold']))
        print ('')
        return -1         
    
    if (len(CON.domain) < 3):
        print (colored('[x] domain is a required argument.', 'red', attrs=['bold']))
        print ('')
        return -1
    
    if (CON.output == ''):
        CON.output = 'output.txt'     
    
    return 0

'''
Execute()
Function: - Does the doing
'''
def Execute():
    captured_content = []

    # List all entries in the directory
    entries = os.listdir(CON.logdir)
    # Filter entries to include only directories and then sort by access time
    subdirectories = [entry for entry in entries if os.path.isdir(os.path.join(CON.logdir, entry))]
    subdirectories.sort(key=lambda x: os.path.getmtime(os.path.join(CON.logdir, x)), reverse=False) 
       
    for subdirectory in subdirectories:
        #print (subdirectory + ':')
        captured_content = find_and_capture_lines(subdirectory)
        CON.captured_content += captured_content

    # Print the results
    for line in CON.captured_content:
        print(line, end='')    

    return 0

'''
find_and_capture_lines()
Function: - Secondary ops  
'''
def find_and_capture_lines(subdirectory):

    capture = False
    captured_lines = []
    file_path = CON.logdir + '/' + subdirectory + '/differ.log'
    end_term = '-----------------------------------------------------------------------------'
    Header = False
    
    with open(file_path, 'r') as file:
        for line in file:
            if CON.domain in line:
                capture = True  # Start capturing when the term is found
            if capture:
                if (Header == False):
                    captured_lines.append('\r\n' + subdirectory + ':\n')
                    Header = True
                captured_lines.append(line)
            if capture and end_term in line:
                break  # Stop capturing after the end term is found            

    return captured_lines    

'''
Terminate()
Function: - Attempts to exit the program cleanly when called  
'''
     
def Terminate(exitcode):
    sys.exit(exitcode)

'''
This is the mainline section of the program and makes calls to the 
various other sections of the code
'''

if __name__ == '__main__':
    
    ret = 0

    #Stores our args
    CON = controller()            

    #Parses our args
    ret = Parse(sys.argv)

    #Something bad happened
    if (ret == -1):
        Usage()
        Terminate(ret)

    if not os.path.exists(CON.logdir):
        print (colored('[x] Log directory does not exist.  Terminating...', 'red', attrs=['bold']))
        Terminate(-1)
    
    #Do the doing
    Execute()

    print ('')
    print (colored('[*] Program Complete', 'green', attrs=['bold']))

    Terminate(0)
'''
END OF LINE
'''