from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class Address(BaseModel):
    city: str
    street: str


class UserValidator(BaseModel):
    name: str = Field(min_length=2, max_length=10)
    age: int = Field(ge=0, le=120, default=18)
    nationality: Literal["Romanian", "Moldovean"] = "Moldovean"
    external: bool | None = True


received_user = {
    "name": "Vincentiu",
    "age": 25,
    "nationality": "Romanian",
    "address": {
        "city": "Brasso",
        "street": "Principala"
    }
}


if __name__ == "__main__":

    print("===============Validations=============")

    # try-catch (except)

    try:
        validated_user = UserValidator.model_validate(received_user, strict=True)
        print(validated_user.name)
    except ValidationError as e:
        print(e)
        print(e.errors())
    finally:
        print("Done")

    varx = None
    print(varx)

    def function2():
        v = 10
        v += 20
        # return None -> return-ul este implicit None

    print(function2())
