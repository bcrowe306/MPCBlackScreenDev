import mido
import os
from mido import Message
from mpc_studio_display.display import Display, Element, Page
from mpc_studio_display.elements.text_element import TextElement
from mpc_studio_display.transport_section import TransportSection
from mpc_studio_display.session_section import SessionSection
from mpc_studio_display.graphics import PngDrawing
from mpc_studio_display.util import message_length
midi_port_name = "MPC Studio Black MPC Private"

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

session_page = Page("session")
session_page.add_element(transport)
session_page.add_element(session)

mixer_page = Page("mixer")
mixer_page.add_element(text2)

dis = Display(send_payload=send_payload)
dis.add_page("session", session_page)
dis.add_page("mixer", mixer_page)

dis.initialize()


# Main loop
# =================
for msg in in_port:
    # os.system('clear')
    # print(msg.bytes())
    bytes = msg.bytes()
    if bytes == [144, 3, 127]:
        dis.show_page("session")
    elif bytes == [144, 2, 127]:
        dis.show_page("mixer")

    if bytes[0] == 153:
        pad_map = {
            49: "track_1",
            55: "track_2",
            51: "track_3",
            53: "track_4"}
        track_name = pad_map.get(bytes[1])
        if track_name:
            for pad in pad_map:
                tn = pad_map[pad]
                t = getattr(session_page.session_section, tn)
                if tn != track_name:
                    t.state = 1 
                else:
                    t.state = 2
