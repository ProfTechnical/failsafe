import os
import re

sel_log = None
subsystems = []

def add_subsystems():
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
            tag = re.compile("\[|\]\[?") #Checks for "[" or "]" with or without a "[" afterwards
            message = tag.split(line)

            if message[0] == '':
                parse_subsystem_message(message, index)
            else:
                parse_system_message(message, index)
            index+=1
        log.close()

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

def print_summary():
    debug = 0
    debug_s = 0
    info = 0
    info_s = 0
    warning = 0
    warning_s = 0
    error = 0
    error_s = 0
    for system in subsystems:
        messages = system.get_messages()
        debug_count = len(messages[Subsystem.debug_level])
        info_count = len(messages[Subsystem.info_level])
        warning_count = len(messages[Subsystem.warning_level])
        error_count = len(messages[Subsystem.error_level])

        if debug_count != 0:
            debug += debug_count
            debug_s += 1
        if info_count != 0:
            info += info_count
            info_s += 1
        if warning_count != 0:
            warning += warning_count
            warning_s += 1
        if error_count != 0:
            error += error_count
            error_s += 1

    
    print("Summary of Log:\n")
    print(str(debug) + " Debug Messages across " + str(debug_s) + " systems")
    print(str(info) + " Info Messages across " + str(info_s) + " systems")
    print(str(warning) + " Warnings across " + str(warning_s) + " systems")
    print(str(error) + " Errors across " + str(error_s) + " systems\n")

def print_system(system_name):
    subsystem = None
    for system in subsystems:
        if system_name == system.name:
            subsystem = system
            break
    
    if subsystem == None:
        print("Captain, I don't have the \"" + system_name + "\" subsystem stored in my databases!\n")
        print("I do have these ones which you might be looking for: ")
        for system in subsystems:
            print(system.name)
        print()
        return
    
    debug_count = len(system.messages[Subsystem.debug_level])
    info_count = len(system.messages[Subsystem.info_level])
    warning_count = len(system.messages[Subsystem.warning_level])
    error_count = len(system.messages[Subsystem.error_level])

    debug_lines = ""
    info_lines = ""
    warning_lines = ""
    error_lines = ""

    if debug_count > 0:
        debug_lines = " at lines: "
        for line in system.messages[Subsystem.debug_level]:
            debug_lines += str(line) + ", "
        debug_lines = debug_lines.rstrip(', ')
    if info_count > 0:
        info_lines = " at lines: "
        for line in system.messages[Subsystem.info_level]:
            info_lines += str(line) + ", "
        info_lines = info_lines.rstrip(', ')
    if warning_count > 0:
        warning_lines = " at lines: "
        for line in system.messages[Subsystem.warning_level]:
            warning_lines += str(line) + ", "
        warning_lines = warning_lines.rstrip(', ')
    if error_count > 0:
        error_lines = " at lines: "
        for line in system.messages[Subsystem.error_level]:
            error_lines += str(line) + ", "
        error_lines = error_lines.rstrip(', ')

    print("Summary of " + system_name + "\n")
    print(str(debug_count) + " Debug Messages" + debug_lines)
    print(str(info_count) + " Info Messages" + info_lines)
    print(str(warning_count) + " Warnings" + warning_lines)
    print(str(error_count) + " Errors" + error_lines)

    
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
    

