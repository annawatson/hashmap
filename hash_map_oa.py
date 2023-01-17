# Name: YU AN PAN
# OSU Email: panyua@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: Hash Map Implementation
# Due Date: 3/11/2022 11:59pm
# Description: Using the open addressing and quadratic probing algorithm to implement the HashMap class,
# including the following methods: put(), get(), remove(), contains_key(), clear(), empty_buckets(),
# resize_table(), table_load(), get_keys()


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
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
        # Create a new buckets and assign it to the self buckets
        new_buckets = DynamicArray()
        for i in range(self.capacity):
            new_buckets.append(None)
        self.buckets = new_buckets
        self.size = 0

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        Quadratic probing required
        :param:
            key (str): the given key.
        :return:
            value (object): the value associated with the given key.
        """

        # Get the index
        index = self.hash_function(key) % self.capacity
        initial_index = index
        j = 0
        while j < self.capacity:
            index = (initial_index + j ** 2) % self.capacity

            # If buckets[index] is None, check the next one
            if self.buckets[index] is None or self.buckets[index].is_tombstone is True:
                j += 1
                continue

            # Check if key is equal, if it is, get the key's value.
            if self.buckets[index].key == key:
                value = self.buckets[index].value
                return value
            j += 1

        # If key is not in the buckets, it returns None.
        return None

    def put(self, key: str, value: object) -> None:
        """
        Update the key / value pair in the hash map. If the given key already exists in the hash map,
        its associated value must be replaced with the new value. If the given key is not in the hash map,
        a key / value must be added.
        If the load factor is greater than or equal to 0.5, resize the table before putting the new key/value pair.
        Quadratic probing required.
        :param:
            key (str): the given key.
            value (object):  the added value.
        :return:
            None
        """
        # Check if threshold is equal to 0.5. If it is, resize it.
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        # Get the index
        index = self.hash_function(key) % self.capacity
        initial_index = index

        has_key = self.contains_key(key)
        # Spin until finding an empty bucket or j == capacity
        j = 0
        while j < self.capacity:
            index = (initial_index + j ** 2) % self.capacity
            # If the given key already exists in the hash map, find the corresponding slot for insertion
            if has_key:
                if self.buckets[index] is not None and self.buckets[index].is_tombstone is False:
                    if self.buckets[index].key == key:
                        break
            else:
                # If the given key do not already exist in the hash map, find an empty slot for insertion
                if self.buckets[index] is None or self.buckets[index].is_tombstone:
                    break
            j += 1

        # Cannot find empty slots
        if j == self.capacity:
            return

        # Insert the hash entry into the empty bucket
        self.buckets[index] = HashEntry(key, value)

        # Increase the size if there is no duplicate key
        if has_key is False:
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Remove the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing (no exception needs to be raised).
        Quadratic probing required
        :param:
            key (str): the given key.
        :return:
            None
        """
        # If the key is not in the hash map, the method does nothing
        if self.contains_key(key) is False:
            return

        # Get the index
        index = self.hash_function(key) % self.capacity
        initial_index = index

        # Spin until finding the key or j == capacity
        j = 0
        while j < self.capacity:
            index = (initial_index + j ** 2) % self.capacity

            # If buckets[index] is an empty slot, keep checking next ones.
            if self.buckets[index] is None or self.buckets[index].is_tombstone:
                j += 1
                continue
            # If the key is found, break at the corresponding index
            if self.buckets[index].key == key:
                break
            j += 1

        # Cannot find empty slots
        if j == self.capacity:
            return

        # Set is_tombstone to True
        self.buckets[index].is_tombstone = True

        # Decrease size
        self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        :param:
            key (str): the given key.
        :return:
            True/False (bool): return True if the given key is in the hash map, otherwise it returns False.
        """
        # Get the index
        index = self.hash_function(key) % self.capacity
        initial_index = index
        j = 0
        while j < self.capacity:
            index = (initial_index + j ** 2) % self.capacity

            # If bucket is an empty slot, check next ones
            if self.buckets[index] is None or self.buckets[index].is_tombstone:
                j += 1
                continue

            # If the key is found, return True
            if self.buckets[index].key == key:
                return True

            j += 1

        # If the given key is not in the hash map, return False.
        return False

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        :param:
            None
        :return:
            num (int): number of the empty buckets in the hash table.
        """
        num = self.buckets.length() - self.size
        return num

    def table_load(self) -> float:
        """
        Return the current hash table load factor.
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
        Change the capacity of the internal hash table. All existing key / value pair must remain in the new hash map,
        and all non-deleted entries must be rehashed into a new table. If new_capacity is less than 1 or less than the
        current number of elements in the map, the method does nothing.
        :param:
            new_capacity (int): the given new capacity.
        :return:
            None
        """
        # If new_capacity is less than 1, the method does nothing.
        if new_capacity < 1:
            return

        # If new capacity is less than the current number of elements in the map, the method does nothing
        if new_capacity < self.size:
            return

        # Create a tmp_buckets which is the copy of the original buckets
        tmp_buckets = DynamicArray()
        for i in range(self.buckets.length()):
            tmp_buckets.append(self.buckets[i])

        # Create a new empty self.buckets with new capacity
        self.buckets = DynamicArray()
        for i in range(new_capacity):
            self.buckets.append(None)
        self.capacity = new_capacity
        self.size = 0

        # Move all keys in the original buckets to the new self.buckets
        for i in range(tmp_buckets.length()):
            if tmp_buckets[i] is None or tmp_buckets[i].is_tombstone:
                continue
            key = tmp_buckets[i].key      # get key from the tmp_buckets
            value = tmp_buckets[i].value  # get value from the tmp_buckets
            self.put(key, value)          # put key and value into the self.buckets
        # Update the capcity to self.buckets' length (since it may be updated in self.put())
        self.capacity = self.buckets.length()

    def get_keys(self) -> DynamicArray:
        """
        Return a DynamicArray that contain all the keys stored in the hash map.
        The order of the keys in the DA does not matter.
        :param:
            None
        :return:
            result (DynamicArray):
        """
        result = DynamicArray()
        # Traver through the array
        for i in range(self.buckets.length()):
            if self.buckets[i] is None or self.buckets[i].is_tombstone is True:
                continue
            result.append(self.buckets[i].key)
        return result


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
    # this test assumes that put() has already been correctly implemented
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
    m = HashMap(50, hash_function_1)
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
