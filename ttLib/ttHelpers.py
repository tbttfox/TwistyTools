#! /usr/bin/python
def remD(arry,key=lambda x: x,last=False):
    """
    removes doubles
    if last=False, the first occurance of an item will be stored
    if last=True, the last occurance will be stored
    """
    seen = {}
    result = []
    index = 0

    if last:
        arry = reversed(arry)

    for item in arry:
        marker = key(item)
        if marker in seen:
            continue
        else:
            seen[marker] = index
            index += 1
            result.append(item)
    return result

