"""
Author: Heather Shaw
Email: heathershaw@disroot.org

This file was created and maintained by Heather Shaw.
For questions or contributions, please contact the author.
"""


from ranger.gui.colorscheme import ColorScheme
from ranger.gui.color import *

import os
import re

def parse_ls_colors():
    ls = os.environ.get("LS_COLORS", "")
    # parse key=values like di=38;5;215
    pairs = ls.split(":")
    colors = {}
    for pair in pairs:
        if "=" not in pair:
            continue
        key, val = pair.split("=", 1)
        # Extract 256 color code
        m = re.search(r"38;5;(\d+)", val)
        if m:
            colors[key] = int(m.group(1))
        else:
            # fallback: try to parse simple codes like "01;31"
            m2 = re.search(r"(\d+)", val)
            if m2:
                if int(m2.group(1)) == 0:
                    colors[key] = -1
                else:
                    colors[key] = int(m2.group(1))
    return colors

LS_COLORS_MAP = parse_ls_colors()

class DynamicLSColors(ColorScheme):
    progress_bar_color = LS_COLORS_MAP.get("di", 215)  # fallback to sunset apricot

    def use(self, context):
        fg, bg, attr = -1, -1, 0  # Default: Rosy Brown on Charcoal

        if context.reset:
            return fg, bg, attr

        elif context.in_browser:
            if context.selected:
                attr |= bold | reverse 
            elif context.marked:
                attr |= bold | reverse
                fg = 196  # Bright RED
            elif context.link:
                fg = LS_COLORS_MAP.get("ln", 51)
            elif context.directory:
                fg = LS_COLORS_MAP.get("di", 215)
            elif context.executable and not context.media:
                fg = LS_COLORS_MAP.get("ex", 51)
            elif context.media:
                fg = LS_COLORS_MAP.get("*.jpg", 215)
            elif context.container:
                fg = LS_COLORS_MAP.get("*.tar", 215)
            elif context.socket:
                fg = LS_COLORS_MAP.get("so", 217)
            elif context.fifo or context.device:
                fg = LS_COLORS_MAP.get("bd", 215)
            else:
                fg = -1

        elif context.in_titlebar:
            attr |= reverse

        elif context.in_statusbar:
            if context.permissions:
                fg = 215
            elif context.marked:
                attr |= bold
                fg = 51
            else:
                fg = -1

        elif context.text:
            fg = -1

        if context.highlight:
            attr |= reverse

        return fg, bg, attr

