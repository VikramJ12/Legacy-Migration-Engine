class Printer:
    """Class to represent a printer that can print messages."""
    def __init__(self):
        """Constructor method to initialize the printer."""
        pass

    def print_message(self, message: str) -> None:
        """Method to print a message using printf."""
        import sys
        print(message, file=sys.stderr)

class Program:
    """Class to represent a program that can run and print messages."""
    def __init__(self):
        """Constructor method to initialize the program."""
        pass

    def run(self) -> None:
        """Method to run the program and print a message."""
        printer = Printer()
        printer.print_message("Hello")
        return

if __name__ == "__main__":
    program = Program()
    program.run()