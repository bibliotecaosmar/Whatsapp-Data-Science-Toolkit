def menu(options):
    items = list(map(lambda item: '# ' + str(item[0] + 1) + '.' + item[1], enumerate(options)))
    print('#=======================================')
    [print(item) for item in items]
    print('#=======================================')
