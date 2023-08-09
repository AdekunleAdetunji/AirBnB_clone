#!/usr/bin/python3
"""
This module contains the class that serves as the entry point to the command
interpreter
"""
import cmd
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re


def update_helper(obj, attribute, value):
    """helper function for update"""

    if not attribute:
        print("** attribute name missing **")
        return False
    if not value:
        print("** value missing **")
        return False
    attribute = attribute.strip('"')
    value = value.strip('"')
    if hasattr(obj.__class__, attribute):
        v = type(getattr(obj.__class__, attribute))
        try:
            setattr(obj, attribute, v(value.strip('"')))
        except ValueError:
            pass
    else:
        if value.startswith('"'):
            value = value.strip('"')
        else:
            number_type = float if "." in value else int
            try:
                value = number_type(value)
            except ValueError:
                pass
        setattr(obj, attribute, value)
    obj.save()


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

    def emptyline(self):
        """Define the console behaviour when an empty command is
        supplied"""
        pass

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

    def do_update(self, line):
        """Updates an instance based on the class name
        and id by adding or updating attribute"""
        if not line:
            print("** class name missing **")
            return False

        exp = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:\S+)))?)?)?'
        match = re.search(exp, line)
        class_name = match.group(1)
        uuid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)

        if not match:
            print("** class name missing **")
            return False
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if not uuid:
            print("** instance id missing **")
            return False
        id = ".".join([class_name, uuid])
        if id not in storage.all():
            print("** no instance found **")
            return False
        obj = storage.all()[id]
        return update_helper(obj, attribute, value)

    def precmd(self, line):
        """Preliminary preparations before executing command"""
        cmds = ["all", "show", "update", "destroy", "count"]
        line = line.strip()
        exp = r'^([A-Z-a-z]+)(?:\.([a-z]+)\(([^\)]*)\))$'
        match = re.search(exp, line)
        if not match:
            return line
        class_name = match.group(1)
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return ""
        command = match.group(2)
        if command not in cmds:
            return line
        args = match.group(3)
        if command == "all":
            result = []
            for k, v in storage.all().items():
                if class_name in k:
                    result.append(str(v))
            print(result)
            return ""
        if command == "count":
            result = 0
            for k, v in storage.all().items():
                if class_name in k:
                    result += 1
            print(result)
            return ""
        if command == "show":
            if not args:
                print("** instance id missing **")
                return ""
            id = ".".join([class_name, args.strip('"')])
            obj = storage.all().get(id)
            if not obj:
                print("** no instance found **")
                return ""
            print(obj)
            return ""
        if command == "destroy":
            if not args:
                print("** instance id missing **")
                return ""
            id = ".".join([class_name, args.strip('"')])
            if id not in storage.all():
                print("** no instance found **")
                return ""
            del storage.all()[id]
            return ""
        if command == "update":
            if not args:
                print("** instance id missing **")
                return ""
            exp = r'^(\"[^"]+\")(?:, (.+))?'
            match = re.search(exp, args)
            if match:
                uuid = match.group(1).strip('"')
                others = match.group(2)
                id = ".".join([class_name, uuid])
                if id not in storage.all():
                    print("** no instance found **")
                    return ""
                obj = storage.all()[id]
                if not others:
                    print("** attribute name missing **")
                    return ""
                exp = r'^(\"[^"]+\")(?:, ((?:\"[^"]+\")|(?:\d+)))?'
                match = re.search(exp, others)
                if match:
                    attribute = match.group(1)
                    value = match.group(2)
                    update_helper(obj, attribute, value)
                    return ""
                exp = r'^(\{(?:.+\:.+,?)*\})'
                match = re.search(exp, others)
                if match:
                    dictionary = match.group(1)
                    if dictionary:
                        try:
                            dictionary = dictionary.replace("'", '"')
                            dictionary = json.loads(dictionary)
                            for k, v in dictionary.items():
                                setattr(obj, k, v)
                            storage.save()
                            return ""
                        except Exception:
                            print("Error")
                            return line
        return line


if __name__ == "__main__":
    HBNBCommand().cmdloop()
