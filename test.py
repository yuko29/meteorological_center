import time

class temp():
    def foo(self):
        self.b(self.foo)


    def b(self, foo):
        print(foo.__name__)

a = temp()
a.foo()


import time

a = "2023-05-13 02:00:00"
a = time.strptime(a, "%Y-%m-%d %H:%M:%S")
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", a)

print("Formatted Time:", formatted_time)

print("Formatted Time:", formatted_time)



c= ["a"]
print(type(c) == str)
