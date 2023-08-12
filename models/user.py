#!/usr/bin/python3
"""module containing User class"""


from models.base_model import BaseModel


class User(BaseModel):
    """Class for User instances extends from BaseModel"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
