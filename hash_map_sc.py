# Name: YU AN PAN
# OSU Email: panyua@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: Hash Map Implementation
# Due Date: 3/11/2022 11:59pm
# Description: Using the chaining algorithm to implement the HashMap class,
# including the following methods: put(), get(), remove(), contains_key(), clear(), empty_buckets(),
# resize_table(), table_load(), get_keys()


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clear the contents of the hash map.
        It does not change the underlying hash table capacity.
        :param:
            None
        :return:
            None
        """
        self.buckets = DynamicArray()
        for i in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        :param:
            key (str): the given key.
        :return:
            value (object): the value associated with the given key.
        """
        # Get the index
        index = self.hash_function(key) % self.capacity

        # Get the value
        if self.buckets[index].contains(key) is not None:
            value = self.buckets[index].contains(key).value
            return value
        return None

    def put(self, key: str, value: object) -> None:
        """
        Update the key/value pair in the hash map. If the given key already exists in the hash map,
        it associated value must be replaced with the new value. If the given key is not in the hash map,
        a key / value pair must be added.
        :param:
            key (str): the added key.
            value (object): the added value.
        :return:
            None
        """
        # Get the index
        index = self.hash_function(key) % self.capacity

        # If there is a duplicated key, remove it first.
        if self.contains_key(key):
            self.buckets[index].remove(key)
            self.size -= 1

        # Insert the key and value
        self.buckets[index].insert(key, value)

        # Increase the size
        self.size += 1

        # Check if threshold = 0.6 (the entries in table are filled). If it is, resize the hash table.
        if self.table_load() >= 0.6:
            self.resize_table(self.capacity)

    def remove(self, key: str) -> None:
        """
        Remove the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        :param:
            key (str): the given key.
        :return:
            None
        """
        # If the key is not exist, just do nothing
        if self.contains_key(key) is False:
            return

        # Get the index
        index = self.hash_function(key) % self.capacity

        # Remove the key and value
        self.buckets[index].remove(key)

        # Decrease the size
        self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        :param:
            key (str): the given key.
        :return:
            (bool): return True if the given key is in the hash map, otherwise it returns False.
        """
        # Get the index
        index = self.hash_function(key) % self.capacity
        # Check key is in the LinkedList or not
        if self.buckets[index].contains(key) is None:
            return False
        return True

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        :param:
            None
        :return:
            num(int): number of the empty buckets in the hash table.
        """
        num = 0
        for i in range(self.buckets.length()):
            if self.buckets[i].head is None:
                num += 1
        return num

    def table_load(self) -> float:
        """
        Return the current hash table load factor.
        It's total number of elements stored in the table / number of buckets.
        :param:
            None
        :return:
            table_load_factor (float): the current hash table load factor.
        """
        num_buckets = self.buckets.length()
        table_load_factor = self.size / num_buckets
        return table_load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map,
        and all hash table links must be rehashed. If new_capacity is less than 1, the method does nothing.
        :param:
            new_capacity (int): the given new capacity.
        :return:
            None
        """
        # If new_capacity is less than 1, the method does nothing.
        if new_capacity < 1:
            return

        # Change the capacity of the internal hash table.
        self.capacity = new_capacity

        # Create new empty buckets with new capacity
        new_buckets = DynamicArray()
        for i in range(new_capacity):
            new_buckets.append(LinkedList())

        # Rehash all hash table links
        # Traverse through the buckets
        for i in range(self.buckets.length()):
            # Traverse through the LinkedList
            cur = self.buckets[i].head
            while cur is not None:
                key = cur.key       # get key
                value = cur.value   # get value
                new_index = self.hash_function(key) % new_capacity  # get new index
                new_buckets[new_index].insert(key, value)           # insert nodes to the new_buckets index
                cur = cur.next

        # Reassign new_buckets to buckets
        self.buckets = new_buckets

    def get_keys(self) -> DynamicArray:
        """
        Return a DynamicArray that contains all the keys stored in the hash map.
        The order of the keys in the DA does not matter
        :param:
            None
        :return:
            result (DynamicArray): the new DynamicArray that contains all the keys stored in the hash map.
        """
        result = DynamicArray()
        # Traver through the array
        for i in range(self.buckets.length()):
            # Traver through the LinkedList            
            cur = self.buckets[i].head
            while cur is not None:
                key = cur.key       # get key
                result.append(key)  # append it to the result
                cur = cur.next
        return result


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]

    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())


