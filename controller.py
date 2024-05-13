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

'''
controller.py - This file is responsible for keeping global settings available through class properties
'''

#python imports
import imp
import sys
from array import *

'''
controller
Class: This class is is responsible for keeping global settings available through class properties
'''
class controller:
    '''
    Constructor
    '''
    def __init__(self):

        self.debug = False
        self.logdir = ''#input from the --logdir cmd line flag denoting log directory to investigate
        self.domain = ''#input from the --domain cmd line flag denoting target domain to profile
        self.output = ''#input from the --output cmd line flag
        self.captured_content = []#