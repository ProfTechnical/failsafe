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
