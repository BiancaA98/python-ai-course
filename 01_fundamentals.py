
var1 = 10
var1 = var1 + 30
var2 = 60
var3 = var2 + var1

print(var3)

# fundamental data structures.

arr = [30, 40, 100, 99, -1, "Harry Potter Chamber of Secrets, by JK Rowling."]
#       0   1    2   3   4                                                 5
print(arr[0])

var4 = {
    "name": "Adrian",
    "age": 33
}

print(arr)

def add(a, b):
    result = a + b
    return result


def multiply(a: int, b: int) -> int:
    return a * b


var5 = add(4, 10)
print(var5)

var6 = multiply(2, 5)
print(var6)
print("hello" + "world")

# type hint: ": int"

# Tipuri de date:
# 0, 1, -1, 100 -> int -> integer, numar intreg.
# 0.5, 1.5, 3.14342354345 -> float/double, numere reale.
# True, False -> bool, boolean.
# "hello world" -> str, string, sir de caractere.
# [] -> list
# {} -> dict

# dynamically typed. -> python
# statically typed.  -> .net, uipath


offer_letter = True

if offer_letter == True:
    print("Yes all good!")
else:
    print("if statement encountered a false value")

age = 30
if age > 25:
    print("Millennial")


# range -> iterator.
for i in range(10):
    print(i)

for x in [10, 20, 33]:
    print(x)


i = 0
while i <= 30:
    print(i)
    i = i + 1

# while True:
#     print(i)
#     i += 1
#     if i > 900:
#         break

while True:
    user_input = input("you>")
    if user_input == "q":
        break
    print(user_input)




