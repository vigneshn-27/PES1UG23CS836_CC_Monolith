import json
from cart import dao
from products import Product, get_product


class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data: dict) -> "Cart":
        return cls(
            id=data['id'],
            username=data['username'],
            contents=data['contents'],
            cost=data['cost'],
        )


def get_cart(username: str) -> list[Product]:
    """
    Retrieve the cart contents for a user, returning a list of Product objects.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    products_in_cart = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Safely parse JSON
        except json.JSONDecodeError:
            continue

        for product_id in contents:
            product = get_product(product_id)
            if product:
                products_in_cart.append(product)

    return products_in_cart


def add_to_cart(username: str, product_id: int) -> None:
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """
    Delete the user's cart entirely.
    """
    dao.delete_cart(username)
