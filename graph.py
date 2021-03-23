from math import sin
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy_garden.graph import Graph, MeshLinePlot,LinePlot
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.tab import MDTabs
Window.size = (300,500)
toolBar = """
BoxLayout:
  pos_hint: {'x': 0.2, 'y': 0.1}
  orientation: 'vertical'
  MDToolbar:
    title: 'Irrigation System'
    left_action_items: [['menu', lambda a: app.navigation_draw()]]
  MDTabs:
    id: tabs
<MyTab>:
  MDLabel: 
    id: label
    text: "MyApp"
    halign: 'center'
"""
class  Hello(Screen):
    pass
sm = ScreenManager()
sm.add_widget(Hello(name = 'hello'))
class MyTab(FloatLayout,MDTabsBase):
    pass
class MyAppFunc(BoxLayout):
    def __init__(self, **kwargs):
        super(MyAppFunc, self).__init__(**kwargs)  # this is only for if kivy code goes in the py file
        self.ticker_list = ['Soil', 'Water Content', 'Humadity', 'Production', 'Rain', "Gain"]
        self.tickers_on_plot = ['Water Content']
        self.plot_colors = [[1, 1, 0, 1], [1, 0, 0, 1], [1, 0, 1, 1], [0.5, .75, .9, 1], [0, 1, 0.3, 1]]
        self.MainProgram()
    def MainProgram(self):
        global box
        screen =ModalView()
        box = Builder.load_string(toolBar)
        screen.add_widget(box)

        graph_theme = {
            'label_options': {
                'color': 'white',  # color of tick labels and titles
                'bold': False},
            'background_color': (0.35,0.35,0.35,1),  # back ground color of canvas
            'tick_color': (1,1,1, 1),  # ticks and grid
            'border_color': (1, 1, 1, 1)}  # border drawn around each graph
        graph2 = Graph(xlabel='DATE', ylabel='SOIL MOISTURE', x_ticks_major=25, y_ticks_major=1, x_grid_label=True,
                       padding=5, pos_hint={'x': 0.0, 'y': 0.2},
                       y_grid=True, x_grid=True, y_grid_label=True, xmin=0, xmax=10, ymin=0, ymax=10, **graph_theme)
        graph2.size_hint_x = 1
        graph2.size_hint_y = 0.6
        graph2.background_color = (0.35,0.35,0.35, 1)
        plot2 = LinePlot(line_width=1, color=[1, 1, 0, 1])
        plot2.points = [(x, sin(x / 10.)) for x in range(5, 101)]
        plot3 = MeshLinePlot(color=[1, 1, 0, 1])
        plot3.points = [(x, sin(x / 15.)) for x in range(0, 101)]
        graph2.add_plot(plot2)
        graph2.add_plot(plot3)
        screen.add_widget(graph2)
        leftbox = BoxLayout(orientation="vertical", size_hint_x=0.3)

        # will contain the ticker gridlayout (top left)
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)

        # holds tickers (top left that will be scrollable)
        ticker_grid = GridLayout(rows=len(self.ticker_list), cols=2, size_hint_y=None)

        # makes the gridlayout scrollabel (top left)
        ticker_grid.bind(minimum_height=ticker_grid.setter("height"))

        # populate the top left scrollable gridlayout (area that shows what tickers are shown)
        # will be marked X or + depending on if it's being shown
        for i in range(0, len(self.ticker_list)):
            ticker_grid.add_widget(Label(text=self.ticker_list[i], size_hint_x=0.6))
            ticker_grid.add_widget(Button(text="+", size_hint_x=0.4))

            # if ticker is shown on plot
            if ((self.ticker_list[i] in self.tickers_on_plot) and len(self.tickers_on_plot) > 0):
                ticker_grid.children[0].text = 'X'
                ticker_grid.children[0].background_color = [1, 0, 0, 1]

            # bind event methods to btns
            if (ticker_grid.children[0].text == "+"):
                ticker_grid.children[0].fbind("on_release", self.plot_add_ticker, ticker_grid.children[1].text,
                                              screen)
            else:
                ticker_grid.children[0].fbind("on_release", self.plot_cancel_ticker, ticker_grid.children[1].text,
                                              screen)
        #scroll.add_widget(ticker_grid)
        #leftbox.add_widget(scroll)

        # the graph doesn't have legend functionality, so make one
        #leftbox.add_widget(self.plot_make_legend())
        #screen.add_widget(leftbox)

        screen.open()
    def plot_make_legend(self):
        # containg_box is just the label saying "legend" then the actual legend
        containing_box = BoxLayout(orientation="vertical", size_hint_y=0.1, padding=10)
        containing_box.add_widget(Label(text="Legend", size_hint=(1, 0.1)))

        # this is the actual legend
        legend_grid = GridLayout(rows=6, cols=2)
        legend_grid.add_widget(Label(text="Ticker"))  # col title
        legend_grid.add_widget(Label(text="Color"))  # col title

        # populated legend_grid
        for i in range(0, len(self.tickers_on_plot)):
            legend_grid.add_widget(Label(text=self.tickers_on_plot[i]))
            legend_grid.add_widget(
                Button(background_color=self.plot_colors[i], disabled=True, background_disabled_normal=""))

        for i in range(len(legend_grid.children) - 1, 11):
            legend_grid.add_widget(Label())

        containing_box.add_widget(legend_grid)

        return containing_box

    def plot_add_ticker(self, ticker, mainview, instance):
        if (len(self.tickers_on_plot) == 5):
            return

        instance.text = "X"
        instance.background_color = [1, 0, 0, 1]

        self.tickers_on_plot.append(ticker)

        mainview.dismiss()  # cancel modalview
        self.MainProgram()  # restart modalview, none replaces instance
    def plot_cancel_ticker(self, ticker, mainview, instance):
        spot = self.tickers_on_plot.index(ticker)
        instance.text = "+"
        instance.background_color = [1, 1, 1, 1]

        del self.tickers_on_plot[spot]

        mainview.dismiss()  # cancel modalview
        self.MainProgram()  # restart modalview, none replaces instance



class myApp(MDApp):
    def build(self):

        return MyAppFunc()

    def navigation_draw(self):
        print("pressed")
    def on_tabs(self):
        global box
        box.ids.tabs.add_widget(MyTab(text="Analysis"))
        box.get_screen('hello').ids.tabs.add_widget(MyTab(text="Report"))
        box.get_screen('hello').ids.tabs.add_widget(MyTab(text="Production"))
myApp().run()
