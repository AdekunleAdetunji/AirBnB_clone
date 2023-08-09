#!/usr/bin/env python3
"""Module containing file storage engine"""


import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """serializes instances to a JSON file and
    deserializes JSON file to instances

    private artributes:
        __object: dictionary of objects saved
        __file_path: path of file storage
    """

    __file_path = "file.json"
    __objects = {}
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """returns the __object dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """adds a new object to the dictionary"""
        obj_class_name = obj.__class__.__name__
        obj_id = "{}.{}".format(obj_class_name, obj.id)
        FileStorage.__objects[obj_id] = obj

    def save(self):
        """saves __object to file"""
        obj_to_dicts = {key: val.to_dict()
                        for key, val in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_to_dicts, file)

    def reload(self):
        """deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists;
        otherwise, do nothing)"""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                obj_of_dicts = json.load(file)
                FileStorage.__objects =\
                    {key: FileStorage.__classes[val["__class__"]](**val)
                     for key, val in obj_of_dicts.items()}

        except Exception:
            return
