def listDiff(list1, list2):
    return [i for i in list1 if not i in list2]


def forceList(var):

    if type(var) is not list:
        var = [var]
    return var
