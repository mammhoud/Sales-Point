from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread

from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ColorProperty, ListProperty, ObjectProperty, StringProperty,NumericProperty
from kivy.core.window import Window
from kivy.metrics import dp, sp
from random import randint


Builder.load_string("""
<FlatField>:
    padding: [dp(6), (self.height - self.line_height)/2]
<SuggestionWidget>:
    size_hint_x: None
    height: dp(42)
    spacing: dp(8)
    padding:[dp(12),0]
    #color: rgba("#ffffff")
    canvas.before:
        Color: 
            rgba: rgba("#afaa22")
        Rectangle:
            pos: self.pos
            size: self.size
    Text:
        text: str(root.pcode) #catched error !
        color: rgba("#ffffff")
        font_size: app.fonts.size.h4
        font_name: app.fonts.body
        size_hint_x: .3
    Text:
        text: str(root.name)
        color: rgba("#ffffff")
        font_size: app.fonts.size.h4
        font_name: app.fonts.body
        size_hint_x: .3
    Text:
        text: "$%s"%str(round(root.price,2))
        color: rgba("#ffffff")
        font_size: app.fonts.size.h4
        font_name: app.fonts.body
        size_hint_x: .2
""")

class FlatField(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_active = ""
        self.background_disabled = ""
        self.background_color = [0,0,0,0]
        self.write_tab = False

class TextField(FlatField):
    bcolor = ColorProperty([0,0,0,1])
    main_color = ColorProperty([1,1,1,1])
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.border_color = Color(rgba=self.bcolor)
            self.border_draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            self.back_color = Color(rgba=self.main_color)
            self.back_draw = RoundedRectangle(
                pos=[self.pos[0]+1.5, self.pos[1]+1.5], 
                size=[self.size[0]-3, self.size[1]-3], 
                radius=self.radius
                )

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_main_color(self, inst, value):
        self.back_color.rgba = value

    def on_bcolor(self, inst, value):
        self.border_color.rgba = value

    def update(self, *args):
        self.border_draw.pos = self.pos
        self.border_draw.size = self.size

        self.back_draw.pos=[self.pos[0]+1.5, self.pos[1]+1.5] 
        self.back_draw.size=[self.size[0]-3, self.size[1]-3]

    def on_radius(self, *args): 
        self.back_draw.radius=self.radius
        self.border_draw.radius=self.radius

class OutlineTextField(FlatField):
    bcolor = ColorProperty([0,0,0,1])
    main_color = ColorProperty([1,1,1,1])
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.border_color = Color(rgba=self.bcolor)
            self.border_draw = Line(
                width=dp(1.5),
                rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]
            )
            self.border_draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            self.back_color = Color(rgba=self.main_color)
            self.back_draw = RoundedRectangle(
                pos=[self.pos[0]+1.5, self.pos[1]+1.5], 
                size=[self.size[0]-3, self.size[1]-3], 
                radius=self.radius
                 )

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_main_color(self, inst, value):
        self.back_color.rgba = value

    def on_bcolor(self, inst, value):
        self.border_color.rgba = value

    def update(self, *args):
        self.border_draw.rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]

    def on_radius(self, *args): 
        self.border_draw.rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]       


class SearchBar(FlatField):
    choices = ListProperty([])
    products = ListProperty([])

    suggestion_widget= ObjectProperty(allownone=True)
    callback= ObjectProperty(alownone=True)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.multiline= False
        self.dropdown=None
    def on_text(self, inst, text):
        try:
            print( "on_text")
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
                
            self.show_suggestions(text)
            
        except Exception as e:
            print(e,'on_text')
        
    def keyboard_on_key_down(self, window,kc, text, modifiers):
        try:
            print( "keyboard_on_key_down")
        # if len(self.text) == 1 or not text:
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
            
            super().keyboard_on_key_down(window,kc,text,modifiers)
        except Exception as e:
            print(e+ "keyboard_on_key_down")
    
    
    def show_suggestions(self, suggestion: str):
            try:
                suggestions = self.get_suggestions(suggestion)
                self.choices.clear()####
                self.choices= suggestions
            except Exception as e:
                print(e+ "show_suggestions")
    
    def on_choices(self, inst, choices):
        print('changed --on_choices---')
        try: 
            # get the suggestions 
            self.dropdown = DropDown()
            self.dropdown.autowidth= False
            self.dropdown.size_hint_x = None
            self.dropdown.width = Window.width*.4
            print("#######################################")

            x:int = 0
            print(self.choices)
            print("#######################################")
            for c in self.choices:
                #b= Button()
                b= SuggestionWidget()
                #if self.suggestion_widget:
                 #   b=self.suggesion_widge()
                b.name = c['name']
                b.pcode= c['pcode']
                b.price= c['price']
                b.size_hint_y = None
                b.height = dp(54)
                #b.height = dp(54)
                b.width= self.width
                b.bind(on_release= self.suggest)

                self.dropdown.add_widget(b)
                
                x+= 1
                
            if x> 0:
                self.dropdown.open(self)
        except Exception as e:
            print(e,"on_choices file")
    def suggest(self,inst):
        if self.callback:
            self.callback(inst)
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
            
        
    def get_suggestions(self, suggestion):
        prods = self.products 
        print(prods)
      #  for x in range(4):
        #    pcode = randint(1,2)
         #   prod= {  
         #       "name": f"Product {x}",
          #      "qty": 1,
           #     "price": 400,
           #     "pcode": str(pcode).zfill(8)
           # } 
            #prods.append(prod)
        return prods 
        
    def close_dropdowns(self):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None             
    def open_dropdown(self, *args):
        if self.dropdown:
            self.dropdown.open(self)
        
        #if self.dropdown:
        #    self.dropdown.dismiss()
        #    self.dropdown = None
            
class SuggestionWidget(ButtonBehavior, BoxLayout):
    pcode= StringProperty(0)
    name= StringProperty("")    
    price= NumericProperty(0)