x=10
def baz():
    nonlocal x
    print(x)  # This will cause an error if there's any assignment to x below
    x+= 30  # Local assignment without declaring as global
    print(x)
baz()