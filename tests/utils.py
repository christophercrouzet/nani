import numpy


def array_to_list(array):
    if isinstance(array, numpy.ndarray):
        return array_to_list(array.tolist())
    elif isinstance(array, list):
        return [array_to_list(item) for item in array]
    elif isinstance(array, tuple):
        return tuple(array_to_list(item) for item in array)
    else:
        return array
