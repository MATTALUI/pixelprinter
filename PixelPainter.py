import arcade
import config
from arcade.gui import UIElement, UIEvent, MOUSE_PRESS, MOUSE_RELEASE
from pyglet.event import EventDispatcher
from brushes import BasicBrush, EraserBrush

class PixelPainter(arcade.Window, EventDispatcher):
    def __init__(self):
        print('Pixel Painter!')
        width = config.RESOLUTION_WIDTH * config.PIXEL_SIZE
        height = (config.RESOLUTION_HEIGHT * config.PIXEL_SIZE) + config.COMMAND_HEIGHT
        super().__init__(width, height, config.TITLE)
        arcade.set_background_color(arcade.csscolor.WHITE)
        self.setup()

    def setup(self):
        self.current_brush = 0
        self.brushes = [BasicBrush(), EraserBrush()]
        self.palette = [False] * (config.RESOLUTION_WIDTH * config.RESOLUTION_HEIGHT)

    def on_draw(self):
        arcade.start_render()
        self._draw_command_pallette()
        self._draw_palette()

    @property
    def selected_brush(self):
        return self.brushes[self.current_brush]

    def _draw_command_pallette(self):
        # MAIN COMMAND
        arcade.draw_rectangle_filled(
            center_x=self.width/2,
            center_y=self.height-(config.COMMAND_HEIGHT/2),
            width=self.width,
            height=config.COMMAND_HEIGHT,
            color=arcade.csscolor.BLACK
        )
        # COMMAND INSET
        arcade.draw_rectangle_filled(
            center_x=self.width/2,
            center_y=self.height-(config.COMMAND_HEIGHT/2),
            width=(self.width)-(config.COMMAND_PADDING*2),
            height=config.COMMAND_HEIGHT-(config.COMMAND_PADDING*2),
            color=arcade.color.DARK_GRAY,
        )
        # BOTTOM BORDER
        arcade.draw_line(
            start_x=0,
            start_y=self.height-config.COMMAND_HEIGHT,
            end_x=self.width,
            end_y=self.height-config.COMMAND_HEIGHT,
            color=arcade.csscolor.DARK_RED,
        )
        self._draw_brushset()

    def _draw_brushset(self):
        # config.BRUSH_WIDTH = (self.width-(config.COMMAND_PADDING*2))/len(self.brushes)
        brushbox_height = config.COMMAND_HEIGHT-(config.COMMAND_PADDING*2)
        for i in range(len(self.brushes)):
            center_x=config.COMMAND_PADDING+((config.BRUSH_WIDTH*(i+1)))+i-(config.BRUSH_WIDTH/2)
            center_y=self.height-(config.COMMAND_HEIGHT/2)
            color = arcade.color.EGGSHELL
            if i == self.current_brush:
                color = arcade.color.DARK_RED
            arcade.draw_rectangle_filled(
                center_x=center_x,
                center_y=center_y,
                width=config.BRUSH_WIDTH,
                height=brushbox_height,
                color=color,
            )
    def _draw_palette(self):
        for i in range(len(self.palette)):
            # TODO: have more robust "pixels"
            if self.palette[i]:
                x, y = self._convert_index_to_cords(i)
                arcade.draw_rectangle_filled(
                    center_x=x,
                    center_y=y,
                    width=config.PIXEL_SIZE,
                    height=config.PIXEL_SIZE,
                    color=arcade.color.BLACK,
                )

    def on_mouse_press(self, x, y, button, modifiers):
        if y > self.height - config.COMMAND_HEIGHT:
            self._change_brush(x, y)
        else:
            self.selected_brush.active=True
            index = self._convert_cords_to_index(x, y)
            self.selected_brush.paint(self.palette, index)
            # self._paint(index)

    def on_mouse_release(self, x, y, button, modifiers):
        self.selected_brush.active=False

    def on_mouse_motion(self, x, y, button, modifiers):
        if self.selected_brush.active and y < self.height - config.COMMAND_HEIGHT:
            index = self._convert_cords_to_index(x, y)
            self.selected_brush.paint(self.palette, index)
            # self._paint(index)

    def _change_brush(self, x, y):
        relative_x = x - config.COMMAND_PADDING
        new_brush = relative_x // config.BRUSH_WIDTH
        if new_brush < len(self.brushes):
            self.current_brush = new_brush

    def _convert_cords_to_index(self, x, y):
        y_base = (y // config.PIXEL_SIZE) * config.RESOLUTION_WIDTH
        x_offset = x // config.PIXEL_SIZE

        return y_base + x_offset

    def _convert_index_to_cords(self, index):
        half = config.PIXEL_SIZE / 2 # use halves so coord ar in center of pixel
        x = (index % config.RESOLUTION_WIDTH) * config.PIXEL_SIZE + half
        y = (index // config.RESOLUTION_WIDTH) * config.PIXEL_SIZE + half

        return (x, y)

    def _paint(self, index):
        # TODO: implement different types of brushes
        self.palette[index] = True
