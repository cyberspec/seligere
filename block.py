"""
Created on 20180718

@author: jenkinski

This is clearly just a very basic example. Will be expanding upon it very soon!
"""
#!/usr/bin/env python
# coding: utf-8
import time,hashlib,logging, random

class block():
    def __init__(self,index,previousHash,timestamp,data):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.generateHash()

    def generateHash(self):
        nextHash = hashlib.sha256()
        nextHash.update(str(self.index).encode())
        nextHash.update(self.previousHash.encode())
        nextHash.update(str(self.timestamp).encode())
        nextHash.update(self.data.encode())
        return nextHash.hexdigest()

class blockchain():
    def __init__(self):
        self.blockchain = []
        self.main()

    def main(self):
        genesisBlock = block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', 1465154705, 'my genesis block!!')

        self.blockchain.append(genesisBlock)

    def getLatestBlock(self):
        return self.blockchain[len(self.blockchain)-1]

    def addBlock(self,newBlock):
        self.blockchain.append(newBlock)

    def createBlock(self,blockData):
        previousBlock = self.getLatestBlock()
        previousHash = previousBlock.hash
        nextIndex = len(self.blockchain)
        nextTimestamp = str(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime()))
        nextHash = previousBlock.hash
        newBlock = block(nextIndex,previousHash,nextTimestamp,blockData)

        self.addBlock(newBlock);

    def calculateHashForBlock(block):
        return generateHash(block.index,block.previousHash,block.timestamp,block.data)

    def isValidNewBlock(newBlock, previousBlock):
        if not isValidBlockStructure(newBlock):
            logging.debug('invalid structure')
            return false

        if len(blockchain) != newBlock.index:
            logging.debug('invalid structure')
            return false

        elif previousBlock.hash != newBlock.previousHash:
            logging.debug('invalid structure')
            return false

        elif calculateHashForBlock(newBlock) != newBlock.hash:
            logging.debug('invalid structure')
            return false

        return true


class prosel_block(block):
    def __init__(self,index,previousHash,timestamp,data,registrations,deadnodes):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.registrations = registrations
        self.deadnodes = deadnodes
        self.hash = self.generateHash()

    def generateHash(self):
        nextHash = hashlib.sha256()
        nextHash.update(str(self.index).encode())
        nextHash.update(self.previousHash.encode())
        nextHash.update(str(self.timestamp).encode())
        nextHash.update(self.data.encode())
        nextHash.update(str(self.registrations).encode())
        nextHash.update(str(self.deadnodes).encode())
        return nextHash.hexdigest()

class prosel_chain(blockchain):
    def __init__(self):
        self.registrations = []
        self.deadnodes = []
        self.blockchain = []
        self.main()

    def main(self):
        genesisBlock = prosel_block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', 1465154705, 'my genesis block!!',[],[])

        self.blockchain.append(genesisBlock)

    def createBlock(self,blockData):
        previousBlock = self.getLatestBlock()
        previousHash = previousBlock.hash
        nextIndex = len(self.blockchain)
        nextTimestamp = str(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime()))
        nextHash = previousBlock.hash
        newBlock = prosel_block(nextIndex,previousHash,nextTimestamp,blockData,self.registrations,self.deadnodes)

        self.addBlock(newBlock);
        self.registrations = []
        self.deadnodes = []

    def registerNode(self,pubkey):
        addme = True
        for block in self.blockchain:
            if pubkey in block.registrations:
                addme = False

        if addme and pubkey not in self.registrations:
            self.registrations.append(pubkey)

    def logDeadNode(self,pubkey):
        addme = False

        for block in self.blockchain:
            if pubkey in block.registrations:
                addme = True

        if addme and pubkey not in self.deadnodes:
            self.deadnodes.append(pubkey)

    def generateSelectee(self):
        registrants = []
        deadnodes = []
        for block in self.blockchain:
            registrants += block.registrations
            deadnodes += block.deadnodes

        for x in deadnodes:
            registrants.remove(x)

        print(self.getLatestBlock().hash)
        random.seed(self.getLatestBlock().hash)
        print(random.choice(registrants))

x = prosel_chain()
x.registerNode('123')
x.registerNode('234')
x.createBlock('blah')
x.registerNode('456')
x.registerNode('423')
x.createBlock('yea')
x.createBlock('yea')
x.logDeadNode('123')
x.createBlock('yead')
x.registerNode('644')
x.createBlock('yead')

for y in x.blockchain:
    print(y.data,y.previousHash,y.timestamp,y.index, y.registrations, y.deadnodes,y.hash)

x.generateSelectee()
