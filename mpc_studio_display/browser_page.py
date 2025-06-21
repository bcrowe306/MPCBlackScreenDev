from mpc_studio_display.header_bar_section import HeaderBarSection
from mpc_studio_display.function_button_section import FunctionButtonSection
from mpc_studio_display.sidebar_menu_section import SidebarMenuSection
from mpc_studio_display.browser_main_section import BrowserMainSection
from .graphics import ImageSection, Icons_5x5
from .display import Page, DISPLAY_WIDTH, DISPLAY_HEIGHT

def create_browser_page():
    """
    Create a browser page with a title and an icon.
    """
    browser_page = Page("browser")
    BrowserHeaderBar = HeaderBarSection("BrowserHeaderBar", "Browser")
    BrowserSidebarMenu = SidebarMenuSection("BrowserSidebarMenu", x=0, y=12, width=90, height=DISPLAY_HEIGHT - 24)
    BrowserMain = BrowserMainSection("BrowserMain", x=91, y=12, width=DISPLAY_WIDTH - 91, height=DISPLAY_HEIGHT - 24)
    BrowserFunctionButtons = FunctionButtonSection("BrowserFunctionButtons", x=0, y=DISPLAY_HEIGHT - 12, width=DISPLAY_WIDTH, height=12)
    BrowserFunctionButtons.function_button_1.text = "Back"
    BrowserFunctionButtons.function_button_2.text = "Fwd"
    BrowserFunctionButtons.function_button_3.text = "Down"
    BrowserFunctionButtons.function_button_4.text = "Up"
    BrowserFunctionButtons.function_button_5.text = "Prev"
    BrowserFunctionButtons.function_button_6.text = "Load"
    browser_page.add_element(BrowserHeaderBar, "BrowserHeaderBar")
    browser_page.add_element(BrowserSidebarMenu, "BrowserSidebarMenu")
    browser_page.add_element(BrowserMain, "BrowserMain")
    browser_page.add_element(BrowserFunctionButtons, "BrowserFunctionButtons")

    return browser_page
