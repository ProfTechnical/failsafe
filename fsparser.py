import os
import re
import fsanalyzer

sel_log = None
subsystems = []

def add_subsystems():
    subsystems.append(Subsystem("System"))
    subsystems.append(Subsystem("Drive"))
    subsystems.append(Subsystem("Limelight"))

def parse_from_log(parse_log):
    global sel_log

    sel_log = parse_log

    for system in subsystems:
        system.clear_messages()

    with open(sel_log.path) as log:
        index = 1
        for line in log:
            tag = re.compile(r"\[|\]\[?") #Checks for "[" or "]" with or without a "[" afterwards
            message = tag.split(line)

            if message[0] == '':
                parse_subsystem_message(message, index)
            else:
                parse_system_message(message, index)
            index+=1
        log.close()

    fsanalyzer.import_subsystems(get_subsystems())

def parse_subsystem_message(message, index):
    name = message[2]
    subsystem = None
    for system in subsystems:
        if name == system.name:
            subsystem = system
            break
    if subsystem == None:
        print("Invalid subsystem: " + name + " at line " + str(index))
        return
    else:
        level = message[1]
        if level == "Debug":
            subsystem.add_debug(index)
        elif level == "Info":
            subsystem.add_info(index)
        elif level == "Warning":
            subsystem.add_warning(index)
        elif level == "Error":
            subsystem.add_error(index)
        else:
            print("Invalid message level: " + level + " at line " + str(index))
            return

def parse_system_message(message, index):
    pass

def get_subsystems():
    return subsystems
    
class Subsystem:
    debug_level = 0
    info_level = 1
    warning_level = 2
    error_level = 3
    
    def __init__(self, name):
        self.name = name
        self.messages = [[],[],[],[]]
    
    def add_debug(self, line_num):
        self.messages[self.debug_level].append(line_num)

    def add_info(self, line_num):
        self.messages[self.info_level].append(line_num)
    
    def add_warning(self, line_num):
        self.messages[self.warning_level].append(line_num)
    
    def add_error(self, line_num):
        self.messages[self.error_level].append(line_num)

    def get_messages(self):
        return self.messages
    
    def clear_messages(self):
        self.messages = [[],[],[],[]]
    

