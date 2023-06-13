""" 
Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution. Hash function is dependent on string-type keys. Contains a method 
which displays the statistics of the hash function. 

"""
from __future__ import annotations
from re import I
__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, and Jackson Goerner. Code by Khor Jia Wynn'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'


from referential_array import ArrayR
from typing import TypeVar, Generic
from primes import LargestPrimeIterator
T = TypeVar('T')


class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        Attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.

            :param arg1: expected_size - the expected size of the table

            :param arg2: tablesize_override - default = -1

            :pre: None

            :return: None
            
            :complexity: Best/Worst O(N), where N is the size of the hash table, which is either 
                         the tablesize_override or the first prime number greater or equal to expected size.
        """
        self.count = 0 # number of elements in the hash table
        self.primes = LargestPrimeIterator(expected_size, 2) 

        # initialize the table size
        if tablesize_override != -1:
            table_size = tablesize_override
        else:
            prime = 2
            # Get the first prime number that is larger or equal to expected_size
            while expected_size > prime:
                prime = next(self.primes)
            table_size = prime
        self.tablesize = table_size

        self.table = ArrayR(self.tablesize) # create the table, O(N)

        # Statistics 
        self.rehash_count = 0
        self.conflict_count = 0
        self.probe_total = 0
        self.probe_max = 0

    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable. Based on the characters in the string. Returns index to be inserted.

            :param: key - the string I wish to hash

            :pre: None

            :return: int - hash value

            :complexity: O(N), where N is the length of the key(str)/ O(1) if string comparisons are done in constant time?
        """
        # good hash
        value = 0
        a = 31415 # start with a prime coefficient
        hash_base = 31 # prime base
        for char in key: 
            value = (ord(char) + a * value) % self.tablesize
            a = a * hash_base % (self.tablesize - 1) # coefficient changes for each position pseudo-randomly, tablesize-1 is coprime with tablesize
        
        return value

        # bad hash
        # return ord(key[0]) % 9

    def statistics(self) -> tuple:
        """
            Return the statistics of the hash table

            :param: None

            :pre: None

            :returns: a tuple of 4 values:
                -the total number of conflicts (conflict_count)

                -the total distance probed throughout the execution of the code (probe_total)

                -the length of the longest probe chain throughout the execution of the code (probe_max)

                -the total number of times rehashing is done (rehash_count)

            :complexity: Best/Worst O(1)
        """
        return (self.conflict_count, self.probe_total, self.probe_max, self.rehash_count)

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table

            :param: None

            :pre: None

            :return: int - the length of the table
            
            :complexity: Best/Worst O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing

            :param arg1: key - the key I wish to find

            :param arg2: is_insert - if True, the key exists in the table

            :pre: None

            :return: int - the position of the key
            
            :complexity: Best O(K) if first position is empty, where K is the size of the key
                         Worst O(K + N) when we've searched the entire table, where N is the tablesize, K is key comparison
            
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash, O(N)
        probe_chain = 0 # reset probe_chain

        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    # print("position of " + key + " is " + str(position))

                    # update probe_max if new probe_chain is larger than previous
                    if probe_chain > self.probe_max: 
                        self.probe_max = probe_chain

                    # update conflict count(happens when linear probing is required to find a position for the value being inserted)
                    if probe_chain != 0: # probe_chain != 0 means the first position was not None so linear probe occured at least once
                        self.conflict_count += 1
                    return position
                else:
                    raise KeyError(key)  # so the key is not in

            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)
                self.probe_total += 1 # update total probe chain length
                probe_chain += 1


        raise KeyError(key) 

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.

            :param: None

            :pre: None

            :return: list - A list of string which is the keys of the table
            
            :complexity: Best/Worst O(N), when N is size of hash table
        """
        res = []
        for x in range(len(self.table)): 
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.

            :param: None

            :pre: None

            :return: list - A list of string which is the items of the table
            
            :complexity: Best/Worst O(N), when N is size of hash table
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)

            :param: key - the string I wish to search

            :pre: if the given key already exist

            :return: boolean - True if it exists
            

            :complexity: Best O(K) first position is empty, where K is the size of the key
                         Worst O(K + N) when we've searched the entire table, where N is the tablesize
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist

            :param: key - the string I wish to search

            :pre: None

            :return: item

            :complexity: Best O(K) first position is empty, where K is the size of the key
                         Worst O(K + N) when we've searched the entire table, where N is the tablesize
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)

            :param arg1: key - the string I wish to set

            :param arg2: data - the item I wish to set

            :pre: None

            :return: None

            :complexity: Best O(K) first position is empty, where K is the size of the key
                         Worst if rehash O(M*(K+M)), where M is the table size, K is the size of the key for rehash
                         else O(K + M) when we've searched the entire table, where M is the tablesize, K is key comparison
        """
        # print("Inserting " + key + " and count is " + str(self.count))
        # rehash if number of elements in the hash table is more than half
        if self.count > self.tablesize/2:
            self._rehash()
            self.rehash_count += 1 # update rehash count
            # print("Inserting " + key + " and count is " + str(self.count))

        position = self._linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1 # update number of elements if it's an insertion

        self.table[position] = (key, data)

    def is_empty(self) -> bool:
        """
            Returns whether the hash table is empty

            :param: None

            :pre: None

            :return: boolean - True if the table is empty

            :complexity: Best/Worst O(1)
        """
        return self.count == 0

    def is_full(self) -> bool:
        """
            Returns whether the hash table is full

            :param: None

            :pre: None

            :return: boolean - True if the table is full

            :complexity: Best/Worst O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)

            :param arg1: key - the string I wish to insert

            :param arg2: data - the item I wish to insert

            :pre: None

            :return: None

            :complexity: Best O(K) first position is empty, where K is the size of the key
                         Worst if rehash O(M*(K+M)), where M is the table size, K is the size of the key for rehash
                         else O(K + M) when we've searched the entire table, where M is the tablesize, K is key comparison

        """
        self[key] = data

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values

            :param: None

            :pre: None

            :return: None

            :complexity: Best/Worst O(M*(K+M)), where M is the table size, K is the size of the key
        """
        keys = self.keys() # O(M), when M is size of hash table
        values = self.values() # O(M), when M is size of hash table
        potential_new_size = self.tablesize * 2 # double the original size
        # print("Potential new size is", potential_new_size)

        # Find the first prime number greater than or equal to potential new size and make it the new table size
        prime = int()
        primes = LargestPrimeIterator(potential_new_size, 2)
        while prime < potential_new_size:
            prime = next(primes) # O(A*N), where N is the upper bound and A is the potential new size
        new_table_size = prime
        
        self.table = ArrayR(new_table_size) # O(M), where M is the table size
        self.tablesize = new_table_size # reset table size
        self.count = 0 # reset the number of elements in the table

        # reinsert everything, O(M*(K+M))
        for key, value in zip(keys, values): # loop O(M) times
            self.insert(key, value) # O(K+M),where M is the table size, K is the size of the key(there should not be another rehash called)


    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).

            :param: None

            :pre: None

            :return: string - all they key/value pairs

            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result


# if __name__ == "__main__":
    # Test statistics using good hash
    # t = LinearProbeTable(9, -1)
    # print(t.tablesize)
    # t.insert("a", 5)
    # t.insert("b", 4)
    # t.insert("c", 3)
    # t.insert("d", 2)
    # t.insert("e", 1)
    # t.insert("f", None)
    # t.insert("g", None)
    # print(len(t.table))
    # t.insert("h", None)
    # print(len(t.table))
    # for char in "ghijklmnopqrs":
    #     t.insert(char, None)
    # for char in ["ab", "cd", "ef", "gh", "hi", "jk", "lm", "mn","op"]:
    #     t.insert(char, None)
    # print(t.tablesize)
    # print(t, "number of elements is " + str(t.count))
    # print(t.statistics()) 


    #Test statistics using good hash with bad table size
    # t = LinearProbeTable(41, 9)
    # print(t.hash("a"))
    # print(t.hash("aar"))
    # print(t.hash("bilious"))
    # print(t.hash("bulbous"))
    # t.insert("a", 5)
    # t.insert("aar", 4)
    # t.insert("bilious", 3)
    # t.insert("bulbous", 2)
    # print(t.statistics()) # One conflict occurs most likely because table size not prime


    # Test statistics using bad hash(need to uncomment bad hash and comment out good hash)
    # t = LinearProbeTable(41, 9)
    # print(t.hash("a"))
    # print(t.hash("aar"))
    # print(t.hash("bilious"))
    # print(t.hash("bulbous"))
    # t.insert("a", 5)
    # t.insert("aar", 4)
    # t.insert("bilious", 3)
    # t.insert("bulbous", 2)
    # print(t.statistics())

    # tablesize = [20021,402221,1000081]
    # for size in tablesize:
    #     print(size)
    #     t1 = LinearProbeTable(size,size)
    #     with open('indian_cities.txt', 'r') as file1:
    #         for line in file1:
    #             t1.insert(line, None)

    #     print(t1.statistics())