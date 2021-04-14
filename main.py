from Blockchain import *

def main():

    chain1 = Blockchain()
    # tester, change range for loop size to add values
    for n in range(0):
        chain1.generate_block()
    # hard code in a new block
    chain1.append_new_block("aspirin","james","0 mg")
    chain1.print_chain()
    print(chain1.find_by_index(12345))


if __name__ == '__main__':
    main()

