import json
from lesson_03_data_validation import UserValidator
with open("user_data.json", "r") as f:
    # json.loads() - deserealizeaza un string din format JSON in obiect python
    data = json.load(f) # deserealizeaza un fisier care contine informatii JSON, in obiect python
    validated_user = UserValidator.model_validate(data, strict=True)
    print(validated_user)
    f.write("hello")
