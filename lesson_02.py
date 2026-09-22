import json

# self == this, in java or javascript


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.nationality = "Romanian"

    def say_hello(self):
        print(self.name + " says hi!")

    def __str__(self):
        return "" + self.name + " " + str(self.age) + ", " + self.nationality

    def return_attrs(self):
        return "" + self.name + " " + str(self.age) + ", " + self.nationality

    def to_json(self):
        d1 = {"name": self.name, "age": self.age, "nationality": self.nationality}
        return json.dumps(d1)


if __name__ == "__main__":
    # folosind User() initializam o instanta a clasei Use
    sonia = User("Sonia", 30)
    dragos = User("Dragos", 35)

    print(sonia.name)

    print(dragos.name)

    print(sonia)

    sonia.say_hello()

    dragos.age = 40
    dragos.hobby = "Warhammer 40"

    print(dragos.return_attrs())

    print(dragos.hobby)

    print(dragos.to_json())

    # structuri de date:

    # list: [10, 20, 30]
    # dict: {"name":"adrian", "age":33}

    # set, unordered list

    s1 = set([10, 30, 40, 40])
    print(s1)

    d1 = {
        "name": "Debra"
    }

    print(d1["name"])

    json_text = '{"name": "Jason", "age": 25}'
    created_dict = json.loads(json_text)

    print(created_dict["name"])
