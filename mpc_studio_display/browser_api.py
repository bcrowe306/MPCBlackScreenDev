from uuid import uuid4
import os
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


class BrowserItem:
    def __init__(self, name: str, is_folder: bool = False, is_device: bool = False, is_loadable: bool = False, is_selected: bool = False):
        self.children = []
        self.is_device = is_device
        self.is_folder = is_folder
        self.is_loadable = is_loadable
        self.is_selected = is_selected
        self.parent = None  # Parent item, if any
        self.name = name
        self.source = uuid4().__str__()
        self.uri = uuid4().__str__()

    def __str__(self):
        return f"BrowserItem(name={self.name}, is_device={self.is_device}, is_folder={self.is_folder})"

    def __repr__(self):
        return self.__str__()

    @property
    def is_root(self):
        return self.parent is None

    def set_parent(self, parent: 'BrowserItem'):
        if isinstance(parent, BrowserItem):
            self.parent = parent
        else:
            raise TypeError("Parent must be an instance of BrowserItem")

    def add_child(self, child: 'BrowserItem'):
        if isinstance(child, BrowserItem):
            child.set_parent(self)
            self.children.append(child)
        else:
            raise TypeError("Child must be an instance of BrowserItem")

class ScrollHistoryStack:
    class HistoryItem:
        def __init__(self, start_index, end_index, selected_index, name):
            self.start_index = start_index
            self.end_index = end_index
            self.selected_index = selected_index
            self.name = name

    def __init__(self):
        self.history = []

    def push(self, history_item):
        self.history.append(history_item)

    def pop(self):
        if self.history:
            return self.history.pop()
        return 0

    def current(self):
        if self.history:
            return self.history[-1]
        return 0
    
    def get_history(self):
        return self.history

class BrowserFrame:
    def __init__(self, children_count, lines=5):
        self.lines = lines
        self.children_count = children_count
        self.start_index = 0
        self.end_index = lines - 1

    def inc_frame(self):
        if self.end_index < self.children_count - 1:
            self.start_index += 1
            self.end_index += 1

    def dec_frame(self):
        if self.start_index > 0:
            self.start_index -= 1
            self.end_index -= 1

    def reset_frame(self, children_count):
        self.children_count = children_count
        self.start_index = 0
        self.end_index = min(self.lines - 1, children_count - 1)

    def set_start_index(self, index: int):
        if 0 <= index < self.children_count:
            self.start_index = index
            self.end_index = min(
                self.start_index + self.lines - 1, self.children_count - 1
            )

    def set_end_index(self, index: int):
        if 0 <= index < self.children_count:
            self.end_index = index
            self.start_index = max(0, self.end_index - self.lines + 1)

class Browser:

    def __init__(self, root: BrowserItem, lines: int = 5):
        self.lines: int = lines
        self.selected_index: int = 0
        self.root = root
        self.frame = BrowserFrame(len(self.root.children), lines)
        self.scroll_history_stack = ScrollHistoryStack()

    def __calculate_frame(self):
        if self.selected_index < self.frame.start_index:
            self.frame.set_start_index(self.selected_index)
            self.frame.set_end_index(self.selected_index + self.lines - 1)
        elif self.selected_index > self.frame.end_index:
            self.frame.set_end_index(self.selected_index)
            self.frame.set_start_index(self.selected_index - self.lines + 1)

    def print_frame(self):
        self.__calculate_frame()
        for i in range(self.frame.start_index, self.frame.end_index + 1):
            item = self.root.children[i] if i < len(self.root.children) else None
            if item is not None:
                if i == self.selected_index:
                    print(f"> {item.name} (Selected)")
                else:
                    print(f"  {item.name}")
            else:
                print(" " * 4 + "No more items to display")

    def get_current_frame(self):
        # Return the current frame of items based on the start and end index.
        current_frame = []
        self.__calculate_frame()
        for i in range(self.frame.start_index, self.frame.end_index + 1):
            item = self.root.children[i] if i < len(self.root.children) else None
            if item is not None:
                current_frame.append({"index": i, "item": item})
        return current_frame

    def get_selected_index(self):
        # Return the index of the currently selected item.
        return self.selected_index

    def get_selected_item(self):
        # Return the currently selected item.
        if self.__index_in_bounds(self.selected_index):
            return self.root.children[self.selected_index]
        return None

    def increment_selection(self):
        if self.selected_index < len(self.root.children) - 1:
            self.selected_index += 1

    def decrement_selection(self):
        if self.selected_index > 0:
            self.selected_index -= 1

    def __index_in_bounds(self, index):
        # Check if the index is within the bounds of the children list.
        return 0 <= index < len(self.root.children)

    def select_item(self, index):
        # Select an item by index, ensuring it is within bounds.
        if self.__index_in_bounds(index):
            self.selected_index = index
            return True
        return False

    def open_item(self, index):
        # Select an item by index, ensuring it is within bounds. If it is folder, replace the current root with the selected item.
        if self.__index_in_bounds(index):
            self.selected_index = index
            selected_item = self.root.children[self.selected_index]

            if selected_item.is_folder:
                # If the selected item is a folder, set it as the new root.
                self.scroll_history_stack.push(
                    ScrollHistoryStack.HistoryItem(
                        self.frame.start_index, self.frame.end_index, self.selected_index, selected_item.name
                    )
                )
                self.root = selected_item
                self.selected_index = 0
                self.frame.reset_frame(len(self.root.children))

    def to_parent(self):
        # Navigate to the parent folder, if it exists. make parent the new root and reset the selected index.
        if self.root.is_root:
            return
        self.root = self.root.parent
        self.selected_index = 0
        if self.scroll_history_stack.current():
            history_item = self.scroll_history_stack.pop()
            self.frame.set_start_index(history_item.start_index)
            self.frame.set_end_index(history_item.end_index)
            self.selected_index = history_item.selected_index
        else:
            self.frame.reset_frame(len(self.root.children))

        self.frame.reset_frame(len(self.root.children))

    def get_scroll_history(self):
        # Return the scroll history stack.
        return self.scroll_history_stack.get_history()


if __name__ == "__main__":

    root = BrowserItem("Root", is_folder=True)
    for i in range(10):
        folder = BrowserItem(f"Folder {i}", is_folder=True)
        for j in range(10):
            device = BrowserItem(f"Device {i}-{j}", is_device=True, is_loadable=True)
            folder.add_child(device)
        root.add_child(folder)

    # Example of adding a new device to a folder
    browser = Browser(root, lines=5)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        browser.print_frame()
        key = input("\nUse 'up' and 'down' arrows to navigate, 'enter' to select, 'backspace' to go up a folder, and 'esc' to exit.")

        if key == "d":
            browser.increment_selection()
        elif key == "u":
            browser.decrement_selection()
        elif key == "e":
            browser.open_item(browser.selected_index)
        elif key == "b":
            browser.to_parent()
        if key == "q":
            print("Exiting...")
            break
