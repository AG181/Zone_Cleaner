import arcade
from views.menu_view import MenuView


def main():
    screen_width, screen_height = arcade.get_display_size()

    window = arcade.Window(
        width=screen_width,
        height=screen_height,
        title="Zone Cleaner",
        fullscreen=True
    )

    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = screen_width
    SCREEN_HEIGHT = screen_height

    window.show_view(MenuView())

    arcade.run()


if __name__ == "__main__":
    main()
