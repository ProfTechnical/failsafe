import os
import re
import fsanalyzer
from subsystem import Subsystem

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
        line_num = 1
        for line in log:
            tag = re.compile(r"\[|\]\[?") #Checks for "[" or "]" with or without a "[" afterwards
            message = tag.split(line)

            if message[0] == '':
                parse_subsystem_message(line, message, line_num)
            else:
                parse_system_message(line, message, line_num)
            line_num+=1
        log.close()

    fsanalyzer.import_subsystems(get_subsystems())

def parse_subsystem_message(line, message, line_num):
    name = message[2]
    subsystem = None
    for system in subsystems:
        if name == system.name:
            subsystem = system
            break
    if subsystem == None:
        print("Invalid subsystem: " + name + " at line " + str(line_num))
        return
    else:
        level = message[1]
        if level == "Debug":
            subsystem.add_debug(line, line_num)
        elif level == "Info":
            subsystem.add_info(line, line_num)
        elif level == "Warning":
            subsystem.add_warning(line, line_num)
        elif level == "Error":
            subsystem.add_error(line, line_num)
        else:
            print("Invalid message level: " + level + " at line " + str(line_num))
            return

def parse_system_message(line, message, line_num):
    pass

def get_subsystems():
    return subsystems