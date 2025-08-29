class Point:
    """
    Represents a 2D point with x and y coordinates.
    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        Initializes a Point object with given x and y coordinates.

        Args:
            x (int): The x coordinate. Defaults to 0.
            y (int): The y coordinate. Defaults to 0.
        """
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        """
        Moves the point by dx units in the x direction and dy units in the y direction.

        Args:
            dx (int): The change in x coordinate.
            dy (int): The change in y coordinate.
        """
        self.x += dx
        self.y += dy


def main():
    """
    The main function.
    """
    p = Point()
    p.move(3, 4)
    print(f"{p.x} {p.y}")


if __name__ == "__main__":
    main()