import numpy as np

class Ray:
    def __init__(self, radius: float=None, theta: float=None, quality: float=None, copy = None):
        if copy is None:
            self.__radius = radius
            self.__theta = theta
            self.__quality = quality
        else:
            self.__radius = copy.radius
            self.__theta = copy.theta
            self.__quality = copy.quality

    @property
    def radius(self) -> float:
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        if value > 0:
            self.__radius = value

    @property
    def theta(self) -> float:
        return self.__theta

    @theta.setter
    def theta(self, value: float):
        if value > 0:
            self.__theta = value

    @property
    def quality(self) -> float:
        return self.__quality

    @quality.setter
    def quality(self, value: float):
        if value > 0:
            self.__quality = value

    @property
    def ray(self) -> np.array:
        return np.array([self.__radius, self.__radius])

    @property
    def data(self) -> np.array:
        return np.array([self.__radius, self.__theta, self.__quality])

class Stack:

    # stack will clear values off the bottom of the stack when values are pushed
    # if the max size (depth) has been set.

    def __init__(self, depth: int = 0 ):
        self.__depth = depth
        self.__stack = []

    def push(self, obj):
        self.__stack.append(obj)
        if self.__stack.__len__() >= self.__depth > 0:
            self.__stack.remove(self.__stack[0])

    def pop(self) -> list:
        temp = self.__stack.pop()
        return temp

    def reset(self):
        self.__stack = []

    @property
    def length(self):
        return self.__stack.__len__()

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, value: int):
        if value > 0:
            self.__depth = value

    @property
    def top(self):
        if self.__stack.__len__() > 0:
            return self.__stack[self.__stack.__len__() - 1]
        return None

    @property
    def bottom(self):
        return self.__stack[0]

    @property
    def stack(self):
        return self.__stack.copy()