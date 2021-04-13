from Blockchain import *

def main():
    '''dose1 = ManageBlocks()
    dose1 = dose1.generateBlock()
    print(dose1)'''

    chain1 = Blockchain()
    chain1.create_genesis_block()
    for n in range(1):
        chain1.generate_block()
    chain1.print_chain()

if __name__ == '__main__':
    main()

