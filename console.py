#!/usr/bin/python3
"""
This module contains the class that serves as the entry point to the command
interpreter
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """
    Entry point into the console
    """
    prompt = "(hbnb) "

    def do_quit(self, line):
        """implementation of quit"""
        return True

    def do_EOF(self, line):
        """Exits out of the program console
        """
        print()
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
