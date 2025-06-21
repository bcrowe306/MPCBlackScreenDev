import mido
import os
from mido import Message
from mpc_studio_display.display import Display, Page
from mpc_studio_display.elements.text_element import TextElement
from mpc_studio_display.transport_section import TransportSection
from mpc_studio_display.session_section import SessionSection, TrackDetailsSection

from mpc_studio_display.browser_page import create_browser_page
from mpc_studio_display.util import message_length
midi_port_name = "MPC Studio Black MPC Private"
from mpc_studio_display.browser_api import BrowserItem, Browser


class MidiMsg:
    def __init__(self, msg):
        self.msg = msg
        self.bytes = msg.bytes()
        self.msg_type = int(self.bytes[0]) & 0xF0
        self.channel = int(self.bytes[0]) & 0x0F
        self.id = self.bytes[1]
        self.value = self.bytes[2]

    def __str__(self) -> str:
        return f"Type: {hex(self.msg_type)}, Channel: {self.channel}, ID: {self.id}, Value: {self.value}"

    def __repr__(self) -> str:
        return self.__str__()

def choose_output(midi_port_name: str):
    outPorts = mido.get_output_names()
    found_port = False
    outPortIndex: int
    for i, port in enumerate(outPorts):
        if port == midi_port_name:
            found_port = True
            outPortIndex = i
            break
    if not found_port:
        for i, port in enumerate(outPorts):
            print(f"{i}:, {port}")
        portNumber = input("Select output index ")
        outPortIndex = int(portNumber)
    selected_port = outPorts[outPortIndex]
    print(f"Opening output: {selected_port}")
    return mido.open_output(selected_port)
def choose_input(midi_port_name: str):
    in_ports = mido.get_input_names()
    found_port = False
    in_port_index: int
    for i, port in enumerate(in_ports):
        if port == midi_port_name:
            found_port = True
            in_port_index = i
            break
    if not found_port:
        for i, port in enumerate(in_ports):
            print(f"{i}:, {port}")
        in_port_selection = input("Select output index ")
        in_port_index = int(in_port_selection)

    selected_port = in_ports[in_port_index]
    print(f"Opening Input: {selected_port}")
    return mido.open_input(selected_port)


SYSEX_START_BYTE = 0xF0
MANUFACTURE_ID = 0x47
CATEGORY_ID = 0x7F
PRODUCT_ID = 0x3D
MSG_TYPE_MODE = 0x62
MODE_PRIVATE = 0x61
MODE_PUBLIC = 0x02
MSG_TYPE_DISPLAY = 0x04
MSG_TYPE_PING = 0x52
SYSEX_END_BYTE = 0xF7
SYSEX_HEADER = (MANUFACTURE_ID, CATEGORY_ID, PRODUCT_ID)
SYSEX_END = (0xF7,)
NUM_SCENE_CONTROLS = 6
PADS_ARRANGEMENT = [
    [49, 55, 51, 53],
    [48, 47, 45, 43],
    [40, 38, 46, 44],
    [37, 36, 42, 82],
]


in_port = choose_input(midi_port_name)
out_port = choose_output(midi_port_name)


def send_sysex_message(msg_id, msg_payload):

    if not isinstance(msg_payload, tuple):
        msg_payload = (msg_payload,)

    msg_length = message_length(msg_payload)
    sysex_message = (
        SYSEX_HEADER
        + (msg_id,)
        + msg_length
        + msg_payload
        # + SYSEX_END
    )
    # logger.info("Sysex Message: %s", sysex_message)
    msg = Message("sysex", data=sysex_message)
    out_port.send(msg)

def send_payload(msg_payload):
    send_sysex_message(MSG_TYPE_DISPLAY, msg_payload)


send_sysex_message(MSG_TYPE_MODE, (MODE_PRIVATE,))


# Create display
# =================


text2 = TextElement("mixer_title", "Mixer", 0, 0, 60, 12, selected=True)
transport = TransportSection()
session = SessionSection()
track_details_section = TrackDetailsSection()

browser_page = create_browser_page()

session_page = Page("session")
session_page.add_element(transport)
session_page.add_element(session)
session_page.add_element(track_details_section)

mixer_page = Page("mixer")
mixer_page.add_element(text2)

dis = Display(send_payload=send_payload)
dis.add_page("session", session_page)
dis.add_page("mixer", mixer_page)
dis.add_page("browser", browser_page)
dis.initialize()
dis.show_page("browser")

pad_map = {
    49: (0,0), 55: (1,0), 51: (2, 0), 53: (3, 0),
    48: (0,1), 47: (1,1), 45: (2, 1), 43: (3, 1),
    40: (0,2), 38: (1,2), 46: (2, 2), 44: (3, 2),
    37: (0,3), 36: (1,3), 42: (2, 3), 82: (3, 3),
}


# Create a browser structure with folders and devices
root = BrowserItem("Root", is_folder=True)
for i in range(40):
    folder = BrowserItem(f"Folder {i}", is_folder=True)
    for j in range(30):
        subfolder = BrowserItem(
            f"Sub Folder {i}-{j}", is_device=False, is_loadable=False, is_folder=True
        )
        for k in range(15):
            device = BrowserItem(
                f"Device {i}-{j}-{k}", is_device=True, is_loadable=True
            )
            subfolder.add_child(device)
        folder.add_child(subfolder)
    root.add_child(folder)
browser = Browser(root, lines=6)

def update_browser_sidebar_menu():
    current_browser_frame = browser.get_current_frame()
    lines_text = []
    selected_line_index = 0
    for i, item in enumerate(current_browser_frame):
        item_text = item["item"].name
        item_index = item["index"]
        if item_index == browser.get_selected_index():
            selected_line_index = i
        lines_text.append(item_text)
    browser_page.BrowserSidebarMenu.set_lines_text(lines_text, selected_line_index=selected_line_index)

def endless_encoder(midi_value):
    direction = not midi_value >> 6
    amount = midi_value & 0b0111111
    if not direction:
        amount = amount - 64
    return amount

volume = 64

# Main loop
# =================
update_browser_sidebar_menu()
for msg in in_port:
    # os.system('clear')
    # print(msg.bytes())
    bytes = msg.bytes()
    if bytes == [144, 3, 127]:
        dis.show_page("session")
    elif bytes == [144, 2, 127]:
        dis.show_page("mixer")
    elif bytes == [144, 50, 127]:
        dis.show_page("browser")

    midi_msg = MidiMsg(msg)
    print(midi_msg)
    if midi_msg.channel == 0x9:

        coordinates = pad_map.get(bytes[1])
        if coordinates:
            track_index, clip_index = coordinates
            for i, track in enumerate(session_page.session_section.tracks):
                if i == track_index:
                    track.state = 2
                    track.select_clip(clip_index)
                    session_page.track_details_section.track_name.text = track.track_name_element.text
                else:
                    track.state = 1
    if midi_msg.msg_type == 0xB0:
        if midi_msg.id == 16:
            volume = max(0, min(127, volume + endless_encoder(midi_msg.value)))
            session_page.track_details_section.meter_element.set_volume_from_midi(volume)

        if midi_msg.id == 101 and midi_msg.value == 127:
            browser.decrement_selection()
            update_browser_sidebar_menu()

        if midi_msg.id == 101 and midi_msg.value == 1:
            browser.increment_selection()
            update_browser_sidebar_menu()
