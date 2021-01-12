
import typing
from typing import List

import pickle
import os

class Person:
    def __init__(self, name):
        self.name : str = name

class Contestant:
    def __init__(self, person):
        self.person : Person = person

class Battle:
    def __init__(self):
        self.contestants : List[Contestant] = []

battles : List[Battle] = []
persons : List[Person] = []

def load_persons():
    global persons
    try:
        with open("data/battle/persons.pickle","rb") as f:
            persons = pickle.load(f)
    except FileNotFoundError:
        pass

def save_persons():
    os.makedirs("data/battle")
    with open("data/battle/persons.pickle","wb") as f:
        pickle.dump(persons, f)

def add_person(name):
    persons.append(Person(name))
    save_persons()
    
load_persons()