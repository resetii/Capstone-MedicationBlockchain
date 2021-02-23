from hashlib import sha256
import json
import time

class Block:
    '''
    Block is defined as the following:
    type = medication name
    created_on = timestamp for block creation
    verified_by = user who tested/entered the dose into system
    quantity = amount in that package (string value to allow for different dosage types (i.e. grams, ounces, etc))
    previous_hash = hash of the last block
    index = the unique indentifier number
    '''
    def __init__(self, type, created_on, verified_by, quantity, previous_hash, index):
        self.index = index
        self.type = type
        self.created_on = created_on
        self.verified_by = verified_by
        self.quantity = quantity
        self.previous_hash = previous_hash

    #override str to allow easy printing of blocks
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def compute_hash(self):
        # Generates hash of contents of block, applied sha256
        block_str = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_str.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    @property
    def last_block(self):
        return self.chain[-1]

    def create_genesis_block(self):
        #Genesis block is the first block in the chain, has zero values and a starting index

        genesis_block = Block("null", time.ctime(), "null", "null", "null", 12345)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def print_chain(self):
        for block in self.chain:
            print(block)

    def generate_block(self):
        while True:
            type = input("Enter a medication name (0 to exit): ")
            if type == "0":
                break

            created_on = time.ctime()

            verified_by = input("Who tested the batch (0 to exit): ")
            if verified_by == "0":
                break

            quantity = input("Enter a quantity (0 to exit): ")
            if quantity == "0":
                break

            new_index = self.last_block.index + 1

            self.chain.append(Block(type, created_on, verified_by, quantity, self.last_block.compute_hash(), new_index))

            return True

