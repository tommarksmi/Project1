__author__ = 'Tom Smith'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector


class MovementGame(Widget):
    """
    Main widget of the program, most of the code in this class was adapted from the pong
    kivy tutorial.
    """
    item = ObjectProperty(None)

    item2 = ObjectProperty(None)

    player = ObjectProperty(None)

    target = [0, 0]

    def on_touch_down(self, touch):
        """
        :param touch: the location of the screen where a touch event has occurred
        :return:
        """

        # the following IF statements ensure that no part of the player object will move off screen
        if touch.x + self.player.width > self.width:
            touch.x = self.width - self.player.width - 3

        if touch.y + self.player.height > self.height:
            touch.y = self.height - self.player.height - 3

        # The rest of this method calculates the difference between the player position and the touch event,
        #then taking the difference and uses the values to set the velocity vector of the player object.
        dif_x = touch.x - self.player.x
        dif_y = touch.y - self.player.y
        self.player.velocity = Vector(dif_x, dif_y).normalize() * 2.5

        #The values from the touch event are stored as a list in the MovementGame Object
        #These values are used to make comparisons with in the update method of this class
        self.target[0] = touch.x
        self.target[1] = touch.y
        print("item 1 type: ", type(self.item), " item2 type: ", type(self.item2), " player type: ", type(self.player))


    def update(self, delta_time):
        """
        This method was derived using the update method from the pong tutorial. But has had significant additions made.
        """
        self.player.move()

        # if statements below stop the player when it reaches the edges of the window

        if self.player.x > self.width - self.player.width or self.player.x < 0:
            self.player.velocity = (0, 0)

        if self.player.y > self.height - self.player.height or self.player.y < 0:
            self.player.velocity = (0, 0)

        #the following if statement checks the players objects current position and compares it to the location of the
        #touch event. If the players position is within 3 pixels of the touch even then the player object is stopped.
        if abs(int(self.target[0]) - int(self.player.x)) < 3 and abs(int(self.target[1] - int(self.player.y))) < 3:
            self.player.velocity = (0, 0)

        #checks for collision with pickup item
        if self.player.collide_widget(self.item):
            self.remove_widget(self.item)

        if self.player.collide_widget(self.item2):
            self.remove_widget(self.item2)


class MovementApp(App):
    """
    This class is a modified version of the App class from the kivy pong tutorial.
    It handles updating of the screen during program execution.
    """

    def build(self):
        game = MovementGame()
        print(type(game.player))
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


class Player(Widget):
    """
    This player class is taken from the PongBall Class in the Pong Kivy tutorial.
    """
    x_velocity = NumericProperty(0)
    y_velocity = NumericProperty(0)
    velocity = ReferenceListProperty(x_velocity, y_velocity)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PickUp(Widget):
    """
    This class is for the pick up item placed on the screen at program start.
    """
    pass


if __name__ == '__main__':
    MovementApp().run()
