import json

# self == this, in java sau javascript.
# all methods surrounded by __, like __str__ are Dunder methods.

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.nationality = "Romanian"

    def to_json(self):
        d1 = {"name": self.name, "age": self.age, "nationality": self.nationality}
        return json.dumps(d1)


    def say_hello(self):
        print(self.name + " says hi!")

    def return_attrs(self):
        return "" + self.name + " " + str(self.age) + ", " + self.nationality

    def __str__(self):
        return "" + self.name + " " + str(self.age) + ", " + self.nationality


if __name__ == "__main__":
    # folosind User() intializam o instanta a clasei User.
    sonia = User("Sonia", 30)
    dragos = User("Dragos", 35)

    dragos.age = 40
    dragos.hobby = "Warhammer 40k"

    print(sonia)
    print(dragos.return_attrs())

    print(sonia.name)
    sonia.say_hello()

    print(dragos.hobby)
    print(dragos.to_json())


    # structuri de date:

    # list: [10, 20, 30]
    # dict: {"name": "adrian", "age": 33}

    # set, unordered list.

    s1 = set([10, 30, 40, 40])
    print(s1)

    d1 = {
        "name": "Debra"
    }

    print(d1["name"])

    # JSON

    json_text = '{"name": "Jason", "age": 25}'
    created_dict = json.loads(json_text)

    print(created_dict["name"])

    # invalid
    # 1var = 10
    # -var = 10














