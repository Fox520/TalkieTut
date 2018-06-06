
import List
from List import MDList
from label import MDLabel

GridLayout:
    cols: 1
    rows: 0
    spacing: 5
    padding: 10
    canvas:
        Color:
            rgba: get_color_from_hex(hex_value)  
        Rectangle:
            pos: self.pos
            size: self.size
    ScrollView:
        do_scroll_x: False
        MDList:
            id: ml

#MDLIST
def add_two_line(self,from_who,msg_to_add):
    self.ml.add_widget(List.TwoLineListItem(text=msg_to_add,
        secondary_text=from_who,
        markup=True,
        text_size=(self.width,None),
        size_hint_y=None,
        font_size=(self.height / 23)))