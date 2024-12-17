




from teste.controllers.base import BaseController
from teste.dtos.user import UserDTO


if __name__ == "__main__":

    base = BaseController("user")

    # user = UserDTO(name="user")
    # base.create(user)

    data = base.get_by_id("67620318848bffbaa4b204f3", UserDTO)
    print("result", data)