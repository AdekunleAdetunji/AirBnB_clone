#!/usr/bin/python3
"""
This module contains the class that serves as the entry point to the command
interpreter
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Entry point into the console
    """
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, line):
        """implementation of quit"""
        return True

    def do_EOF(self, line):
        """Exits out of the program console
        """
        print()
        return True

    def do_create(self, line):
        """creates a new instance of any class and prints the ID"""
        if not line:
            print("** class name missing **")
            return False
        if line not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return False
        new_item = HBNBCommand.classes[line]()
        storage.save()
        print(new_item.id)

    def do_show(self, line):
        """Prints the string representation of an instance
        based on the class name and id"""
        if not line:
            print("** class name missing **")
            return False
        args = line.split()
        if args[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False
        id = ".".join(args)
        requested = storage.all().get(id)
        if not requested:
            print("** no instance found **")
            return False
        print(requested)

    def destroy(self, line):
        """Deletes an instance based on the class name and id"""
        if not line:
            print("** class name missing **")
            return False
        args = line.split()
        if args[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False
        id = ".".join(args)
        if id not in storage.all():
            print("** no instance found **")
            return False
        del storage.all()[id]
        storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
        based or not on the class name."""
        if not line:
            print([str(v) for v in storage.all().values()])
        else:
            if line not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return False
            result = []
            for k, v in storage.all().items():
                if line in k:
                    result.append(str(v))
            print(result)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
