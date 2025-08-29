class Point:
    """Represents a 2D point with x and y coordinates."""
    def __init__(self, x=0, y=0):
        """Initialize a Point object with x and y coordinates."""
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move the point by dx units in the x direction and dy units in the y direction."""
        self.x += dx
        self.y += dy

# Example usage:
p = Point()
p.move(3, 4)
print(f"{p.x} {p.y}")