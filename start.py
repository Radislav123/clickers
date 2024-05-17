import arcade

from simple.window import Window


def start() -> None:
    window = Window()
    try:
        window.start()
        arcade.run()
    finally:
        window.stop()


if __name__ == "__main__":
    start()
