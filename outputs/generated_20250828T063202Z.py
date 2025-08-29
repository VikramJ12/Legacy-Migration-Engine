class Point:
    """Represents a 2D point with x and y coordinates."""
    def __init__(self, x=0, y=0):
        """Initialize a Point with x and y coordinates."""
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move the point by dx units in the x direction and dy units in the y direction."""
        self.x += dx
        self.y += dy

# Mapping summary:
# C struct Point -> Python class Point
# C function move -> Python method move in class Point
# C variable p -> Python object p of class Point
# C function printf -> Python print function

# Example usage:
p = Point()
p.move(3, 4)
print(p.x, p.y)