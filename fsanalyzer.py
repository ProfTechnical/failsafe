import os
import re
from subsystem import Subsystem
import fsparser

subsystems = []

def import_subsystems(subsystem_list):
    global subsystems
    subsystems = subsystem_list

def has_subsystems():
    global subsystems
    if subsystems == []:
        print("Captain, I don't have any subsystems to analyze! Please call the parser!")
        return False
    return True

def subsystem_namecheck(system_name):
    subsystem = None
    for system in subsystems:
        if system_name.lower() == system.name.lower():
            subsystem = system
            break
    
    if subsystem == None:
        print("Captain, I don't have the \"" + system_name + "\" subsystem stored in my databases!\n")
        print("I do have these ones which you might be looking for: ")
        for system in subsystems:
            print(system.name)
        print()
    return subsystem

def print_summary():
    if not has_subsystems():
        return
    
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
    if not has_subsystems():
        return

    system = subsystem_namecheck(system_name)
    if system == None:
        return
    
    messages = system.get_messages()
    
    debug_count = len(messages[Subsystem.debug_level])
    info_count = len(messages[Subsystem.info_level])
    warning_count = len(messages[Subsystem.warning_level])
    error_count = len(messages[Subsystem.error_level])

    debug_lines = ""
    info_lines = ""
    warning_lines = ""
    error_lines = ""

    if debug_count > 0:
        debug_lines = " at lines: "
        for line in messages[Subsystem.debug_level]:
            debug_lines += str(line[1]) + ", "
        debug_lines = debug_lines.rstrip(', ')
    if info_count > 0:
        info_lines = " at lines: "
        for line in messages[Subsystem.info_level]:
            info_lines += str(line[1]) + ", "
        info_lines = info_lines.rstrip(', ')
    if warning_count > 0:
        warning_lines = " at lines: "
        for line in messages[Subsystem.warning_level]:
            warning_lines += str(line[1]) + ", "
        warning_lines = warning_lines.rstrip(', ')
    if error_count > 0:
        error_lines = " at lines: "
        for line in messages[Subsystem.error_level]:
            error_lines += str(line[1]) + ", "
        error_lines = error_lines.rstrip(', ')

    print("Summary of " + system_name + "\n")
    print(str(debug_count) + " Debug Messages" + debug_lines)
    print(str(info_count) + " Info Messages" + info_lines)
    print(str(warning_count) + " Warnings" + warning_lines)
    print(str(error_count) + " Errors" + error_lines)

def find(args):
    if args == []:
        print("Captain, you haven't specified anything for me to find!")
        print("*Try something like this*\n")
        print("find level [subsystem]")
        return
    
    msg_levels = ["debug", "info", "warning", "error"]
    level = args[0].lower()

    if level in msg_levels:
        if level == "debug":
            level = Subsystem.debug_level
        elif level == "info":
            level = Subsystem.info_level
        elif level == "warning":
            level = Subsystem.warning_level
        else:
            level = Subsystem.error_level
    else:
        print("Captain, there isn't a message level of: " + level)
        print("Use \"debug\", \"info\", \"warning\", or \"error\"")
        return
    
    system_name = None
    if args[1] != None:
        system_name = args[1].lower()
    
        system = None
        if system_name != None:
            #TODO Subsystem check, then run search function for subsystem
            system = subsystem_namecheck(system_name)
            if system == None:
                return

        messages = system.get_messages()
        for line in messages[level]:
            print(str(line[1]) + " " + str(line[0]).rstrip("\n"))
        print()

    else:
        #TODO Run search function across entire log
        pass
