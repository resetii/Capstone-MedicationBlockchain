# Capstone-MedicationBlockchain

Abstract: The blockchain structure is an immutable, constantly growing record that was first implemented in a real-world use case in 2008 by the person/group known as Satoshi Nakamoto. This technology was used as the ledger system for the cryptocurrency they implemented Bitcoin but this structure itself has many more practical scenarios it can be applied to. This project will focus on implementing a blockchain structure to act as the backbone for a medicine distribution system that can not only provide a labelling system for individually created and dispensed doses but also will use the blockchain to encapsulate data related to the initial creation and distribution of that dose to ensure its legitimacy and security. We will be using Python to create the blockchain itself and use currently available libraries to assist with the hashing feature of the software. Once the structure itself is created, it will temporarily be accessible through our website and allow users to create their own blocks and check on the data related to any other block in the system. The final portion is to generate a unique ID for each of these blocks (each representing a single bottle/dose) which will also can be used to produce a QR code-based label. 

Block is defined as the following:
    type = medication name
    created_on = timestamp for block creation
    verified_by = user who tested/entered the dose into system
    quantity = amount in that package (string value to allow for different dosage types (i.e. grams, ounces, etc))
    block_hash = hash of the data contained in values {type, created_on, verified_by, quantity, index} in json format
    previous_hash = hash of the last block
    index = the unique indentifier number
