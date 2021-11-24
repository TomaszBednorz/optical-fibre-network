from data_structures import *



if __name__ == "__main__":
    print("Hello world!")
    
    net1 = Network()


    net1.add_building(2,2,1)
    net1.add_building(2,3,2)
    net1.add_building(2,4,3)

    for el in net1.buildings:
        print(el)

    net1.remove_building(2)

    for el in net1.buildings:
        print(el)