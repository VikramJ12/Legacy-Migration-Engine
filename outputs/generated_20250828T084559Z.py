class Point:
    """Represents a 2D point with x and y coordinates."""

    def __init__(self, x: int = 0, y: int = 0):
        """Initialize a Point with x and y coordinates."""
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        """Move the point by dx units in the x direction and dy units in the y direction."""
        self.x += dx
        self.y += dy


def main():
    """Main function to demonstrate the use of the Point class."""
    p = Point()
    p.move(3, 4)
    print(f"{p.x} {p.y}")


if __name__ == "__main__":
    main()