#!/usr/bin/python
from ttBase import TTBase

class Value(TTBase):
    """ This class is used to hold a single value for the treeItem """
    def __init__(self,value,label):
        super(Value,self).__init__()
        self.value = value
        self.enum = self.enumType.Value
        self.label = label
        self.setParents()
    



