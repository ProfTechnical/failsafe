import os
import datetime
import fsparser
import fsanalyzer

sel_log = None
log_list = []
logs_dir = "D:/Documents/2020 INFINITE RECHARGE Documents/Robot Logs/"

def failsafe():
    global sel_log
    is_running = True
    print('Ahoy captain! What can I do for you today?')
    while is_running:
        prompt = input()
        split = prompt.split(" ")
        command = split[0]
        args = []
        if len(split) > 1:
            del split[0]
            args = split
        
        commands = ["help", "quit", "select", "list", "print", "parse", "find"]

        if command in commands:
            if command == "quit":
                print("Goodbye captain!")
                is_running = False
            elif command == "select":
                listlogs()
                selectlog()
            elif command == "list":
                listlogs()
            elif command == "print":
                printlog()
            elif command == "parse":
                parselog(args)
            elif command == "find":
                findinlog(args)
        else:
            print("""I'm sorry captain, but I don't understand!\n*Please input a valid command...* or \"help\" if you need a list of them!""")

        if is_running:
            print("What else can I help you with today?")

def listlogs():
    with os.scandir(logs_dir) as dir:
        log_list.clear()

        for entry in dir:
            log_list.append(entry)
        log_list.sort(key=lambda entry: entry.stat().st_mtime, reverse=True)

        index = 0
        for entry in log_list:
            if entry.is_file():
                    index += 1
                    filetime = datetime.datetime.fromtimestamp(entry.stat().st_mtime)
                    datespace = 85 - len(entry.name)
                    print((str(index) + "|").rjust(4, ' ') + " " + entry.name + filetime.isoformat(' ', timespec='seconds').rjust(datespace))
        dir.close()

def selectlog():
    global sel_log
    has_valid_index = False
    while not has_valid_index:
        index_raw = input("Select a log number: ")
        index = 0
        if index_raw.isdecimal():
            index = int(index_raw) - 1
        else:
            print("Enter a positive integer.")
            continue

        if 0 <= index and index < len(log_list):
            sel_log = log_list[index]
            has_valid_index = True
            print("Selected log " + str(index + 1) + ": " + sel_log.name + "\n")
        else:
            print("Invalid index. Select an index from 1 to " + str(len(log_list)))

def printlog():
    global sel_log
    check_and_select()

    with open(sel_log.path) as log:
        index = 1
        for line in log:
            print(str(index) + " " + line, end="")
            index+=1
        log.close()
        print("\nEND OF LOG\n")

def parselog(args):
    global sel_log
    check_and_select()
    
    fsparser.parse_from_log(sel_log)
    if args != []:
        system_name = args[0]
        fsanalyzer.print_system(system_name)
    else:
        fsanalyzer.print_summary()

def findinlog(args):
    global sel_log
    check_and_select()

    fsparser.parse_from_log(sel_log)
    fsanalyzer.find(args)

def check_and_select():
    global sel_log
    if sel_log == None:
        print("Captain, it appears that you haven't yet selected a log. *I suggest you do that*")
        listlogs()
        selectlog()

def main():
    fsparser.add_subsystems()
    failsafe()

if __name__ == "__main__":
    main()