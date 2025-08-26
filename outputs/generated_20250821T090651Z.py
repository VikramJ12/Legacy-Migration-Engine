class Point:
    """Represents a point in 2D space with x and y coordinates."""

    def __init__(self, x=0, y=0):
        """Initialize a point with x and y coordinates."""
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move the point by dx units in the x direction and dy units in the y direction."""
        self.x += dx
        self.y += dy

class Program:
    """Represents a program that can run a main method."""

    def main(self):
        """Run the main method, creating a point, moving it, and printing its coordinates."""
        p = Point()
        p.move(3, 4)
        print(f"{p.x} {p.y}")

if __name__ == "__main__":
    prog = Program()
    prog.main()