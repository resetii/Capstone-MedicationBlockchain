from hashlib import sha256
import json
import time

#this is the raw block data
class Block:
    '''
    Block is defined as the following:
    type = medication name
    created_on = timestamp for block creation
    verified_by = user who tested/entered the dose into system
    quantity = amount in that package (string value to allow for different dosage types (i.e. grams, ounces, etc))
    block_hash = hash of the data contained in values {type, created_on, verified_by, quantity, index} in json format
    previous_hash = hash of the last block
    index = the unique indentifier number
    '''
    def __init__(self, type, created_on, verified_by, quantity, previous_hash, block_hash, index):
        self.index = index  # serial number
        self.type = type  #name of medication
        self.created_on = created_on   #timestamp of creation
        self.verified_by = verified_by   #user who tested batch
        self.quantity = quantity   #dosage amount
        self.block_hash = block_hash
        self.previous_hash = previous_hash

    #override str to allow easy printing of blocks
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def print_value_table(self):
        data_Dict = {
            "type": self.type,
            "created_on": self.created_on,
            "verifed_by": self.verified_by,
            "quantity": self.quantity,
            "index": self.index}
        return data_Dict

    def compute_hash(self):
        # Generates hash of contents of block, applied sha256
        data_Dict = {
  		"type": self.type,
  		"verifed_by": self.verified_by,
        "quantity": self.quantity}

        # Dumps bit data from the json format to prep it for sha256 hash
        block_str = json.dumps(data_Dict, sort_keys=True)
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

        genesis_block = Block(type="null", created_on=time.ctime(), verified_by="null", quantity="null", previous_hash="null", index=12345, block_hash="null")
        genesis_block.block_hash = genesis_block.compute_hash()
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

            temp_block = Block(type, created_on, verified_by, quantity, self.last_block.block_hash, "null", new_index)
            this_hash = temp_block.compute_hash()
            temp_block.block_hash = this_hash
            self.chain.append(temp_block)

            return True

    def append_new_block(self, type, verified_by, quantity):
        created_on = time.ctime()
        new_index = self.last_block.index + 1
        temp_block = Block(type, created_on, verified_by, quantity, self.last_block.block_hash, "null", new_index)
        this_hash = temp_block.compute_hash()
        temp_block.block_hash = this_hash
        self.chain.append(temp_block)
