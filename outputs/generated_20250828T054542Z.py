class Point:
    """Represents a 2D point with x and y coordinates."""
    def __init__(self, x=0, y=0):
        """Initialize a point with given x and y coordinates."""
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move the point by dx units in x direction and dy units in y direction."""
        self.x += dx
        self.y += dy


def main():
    """Main function to test the Point class."""
    p = Point()
    p.move(3, 4)
    print(f"{p.x} {p.y}")


if __name__ == "__main__":
    main()