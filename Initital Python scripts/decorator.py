def decorator(kuchbhi):
    def hello():
        print("Hello")
        kuchbhi()
    return hello

@decorator
def world():
    print ("World!")

world()