'''
Created on 01.11.2012

@author: jakob
'''

class Engine(object):
    def __init__(self):
        self.fixtures = []
    
    def addFixture(self, fixture):
        self.fixtures.append(fixture)
        
    def removeFixture(self, fixture):
        self.fixtures.remove(fixture)