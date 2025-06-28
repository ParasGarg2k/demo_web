import threading
import time

class InventoryAPI:
    def __init__(self, initial_products):
        """
        initial_products: List of dicts representing products with stock_quantity
        """
        # Using dict keyed by product_id for quick access
        self.products = {p['product_id']: p.copy() for p in initial_products}
        self.lock = threading.Lock()

    def get_product(self, product_id):
        """
        Return product info dict by product_id, or None if not found.
        """
        return self.products.get(product_id)

    def get_stock(self, product_id):
        """
        Return current stock quantity of product.
        """
        product = self.products.get(product_id)
        if product:
            return product.get('stock_quantity', 0)
        return 0

    def update_stock(self, product_id, delta):
        """
        Increase or decrease stock by delta (negative to reduce).
        Returns updated stock quantity or None if product_id invalid.
        Thread-safe.
        """
        with self.lock:
            product = self.products.get(product_id)
            if not product:
                return None
            new_stock = product['stock_quantity'] + delta
            if new_stock < 0:
                new_stock = 0
            product['stock_quantity'] = new_stock
            return new_stock

    def search_products(self, query):
        """
        Search products by name substring (case insensitive).
        Returns list of matching product dicts.
        """
        q = query.lower()
        results = []
        for p in self.products.values():
            if q in p['name'].lower():
                results.append(p)
        return results

    def list_all_products(self):
        """
        Return list of all product dicts.
        """
        return list(self.products.values())


# Demo usage
if __name__ == "__main__":
    sample_products = [
    {
        "product_id": "p100",
        "name": "Almond Milk",
        "stock_quantity": 20
    },
    {
        "product_id": "p101",
        "name": "Cheddar Cheese",
        "stock_quantity": 10
    },
    {
        "product_id": "p102",
        "name": "Whole Wheat Bread",
        "stock_quantity": 15
    },
    {
        "product_id": "p103",
        "name": "Orange Juice",
        "stock_quantity": 25
    },
    {
        "product_id": "p104",
        "name": "Organic Apples",
        "stock_quantity": 50
    },
    {
        "product_id": "p110",
        "name": "Blueberry Muffin",
        "stock_quantity": 12
    },
    {
        "product_id": "p111",
        "name": "Potato Chips",
        "stock_quantity": 30
    },
    {
        "product_id": "p112",
        "name": "Carrot Sticks",
        "stock_quantity": 40
    }
    ]


    api = InventoryAPI(sample_products)

    print("Initial stock for p100:", api.get_stock("p100"))
    api.update_stock("p100", -3)
    print("Stock after selling 3 units:", api.get_stock("p100"))

    search_results = api.search_products("milk")
    print("Search results for 'milk':", [p['name'] for p in search_results])
