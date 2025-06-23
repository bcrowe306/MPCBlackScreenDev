import os
import sys

def to_msb_lsb(value):
    if not (0 <= value <= 16383):
        raise ValueError("Value must be between 0 and 16383 (14-bit).")
    lsb = value & 0x7F  # lower 7 bits
    msb = (value >> 7) & 0x7F  # upper 7 bits
    return msb, lsb


def from_msb_lsb(msb, lsb):
    return ((msb & 0x7F) << 7) | (lsb & 0x7F)

number = 240
print(from_msb_lsb(*to_msb_lsb(number)) == number)


class Command:

    def __init__(self, name, label, action, alternative=None, alternative_label=None):
        self.name = name
        self.label = label
        self.action = action
        self.alternative = alternative
        self.alternative_label = alternative_label if alternative_label else f"{label} (Alt)" if label else "Alternative Action"

    def execute(self, alternative=False):
        if alternative and self.alternative:
            if callable(self.alternative):
                return self.alternative()

        if callable(self.action):
            return self.action()


class CommandMenu:
    def __init__(self, control_count=4):
        self._control_count = control_count
        self._current_page_index = 0
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    def get_current_page(self):
        start_index = self._current_page_index * self._control_count
        end_index = start_index + self._control_count
        return self._commands[start_index:end_index]

    def next_page(self):
        if (self._current_page_index + 1) * self._control_count < len(self._commands):
            self._current_page_index += 1
            return True
        return False

    def previous_page(self):
        if self._current_page_index > 0:
            self._current_page_index -= 1
            return True
        return False

    def get_command(self, control_index):
        if control_index < 0 or control_index >= self._control_count:
            raise IndexError("Control index out of range")
        commands = self.get_current_page()
        if control_index < len(commands):
            return commands[control_index]
        return None

    def execute_command(self, control_index, alternative=False):
        command = self.get_command(control_index)
        if command:
            return command.execute(alternative=alternative)
        return None


cm = CommandMenu(control_count=4)
cm.add_command(Command("cmd1", "Command 1", lambda: print("Executing Command 1")))
cm.add_command(Command("cmd2", "Command 2", lambda: print("Executing Command 2")))
cm.add_command(Command("cmd3", "Command 3", lambda: print("Executing Command 3")))
cm.add_command(Command("cmd4", "Command 4", lambda: print("Executing Command 4")))
cm.add_command(Command("cmd5", "Command 5", lambda: print("Executing Command 5")))
cm.add_command(Command("cmd6", "Command 6", lambda: print("Executing Command 6")))
cm.add_command(Command("cmd7", "Command 7", lambda: print("Executing Command 7")))
cm.add_command(Command("cmd8", "Command 8", lambda: print("Executing Command 8")))  
cm.add_command(Command("cmd9", "Command 9", lambda: print("Executing Command 9")))
cm.add_command(Command("cmd10", "Command 10", lambda: print("Executing Command 10")))
cm.add_command(Command("cmd11", "Command 11", lambda: print("Executing Command 11")))

def print_current_page():
    for cmd in cm.get_current_page():
        print(f"{cmd.label} - {cmd.name}")


print_current_page()
selection = input("Select command (0-3) or 'n' for next page, 'p' for previous page: ")

while selection.lower() not in ['q', 'exit']:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    if selection.lower() == 'n':
        if cm.next_page():
            pass
        
    elif selection.lower() == 'p':
        if cm.previous_page():
            pass
    else:
        try:
            index = int(selection) -1
            if 0 <= index < cm._control_count:
                cm.execute_command(index)
            else:
                print(f"Invalid selection. Please choose a number between 0 and {cm._control_count - 1}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'n'/'p'.")
    print_current_page()
    selection = input("Select command (0-3) or 'n' for next page, 'p' for previous page: ")
os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console