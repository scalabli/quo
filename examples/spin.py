from quo.spin import Spinner



with Spinner():
    import time
    time.sleep(5)
    print("Hello, world")
