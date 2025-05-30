import random
import numpy as np

class MyClass:
    def __init__(self):
        self.tdObjects = []
    
    def __repr__(self):
        return f"List:{self.tdObjects}"

touchdownMap = np.empty((15,15), dtype=MyClass)


for x in range(touchdownMap.shape[0]):
    for y in range(touchdownMap.shape[1]):
            touchdownMap[x][y] = MyClass()

            for t in range(5):
                 touchdownMap[x][y].tdObjects.append(f"{t}")

##############
class CustomObject:
    def __init__(self, arrList):
        self._arrList = arrList

    @property
    def content(self):
        return self._arrList

    @content.setter
    def content(self, value):
        self._arrList = value

    @property
    def length(self):
        return len(self._arrList)

    def __repr__(self):
            return f"Val:{self._arrList}"

class LengthArray:
    def __init__(self, object_array):
        self.object_array = object_array


    def __repr__(self):
        return f"List:{len(self.object_array)}"


# Create a 2D list of CustomObject instances
object_array = [
    CustomObject("hello"), CustomObject("world"), CustomObject("numpy"), CustomObject("array")
]


touchdownMap = np.empty((3,3), dtype=MyClass)


for x in range(touchdownMap.shape[0]):
    for y in range(touchdownMap.shape[1]):
        touchdownMap[x][y] = LengthArray(object_array)
        print(touchdownMap[x][y])

# Change the content of an object
object_array.append(CustomObject("ASD"))

for x in range(touchdownMap.shape[0]):
    for y in range(touchdownMap.shape[1]):
        print(touchdownMap[x][y])


#######################
def create_random_custom_object_array(rows, cols):
    # Initialize a 2D array with None
    array = np.empty((rows, cols), dtype=MyClass)

    # Step 3: Fill the array with random instances of CustomObject
    for i in range(rows):
        for j in range(cols):
            random_value = random.randint(0, 100)
            array[i, j] = CustomObject(random_value)
    
    return array

custom_object_array = create_random_custom_object_array(touchdownMap.shape[0], touchdownMap.shape[1])


for x in range(custom_object_array.shape[0]):
    for y in range(custom_object_array.shape[1]):
        print(custom_object_array[x][y])


for x in range(custom_object_array.shape[0]):
    for y in range(custom_object_array.shape[1]):
        print(custom_object_array[x][y])

        
print()