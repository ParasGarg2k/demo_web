import numpy as np

class ProductFeatureEncoder:
    def __init__(self, products):
        self.products = products
        self.categories = sorted(set(p['category'] for p in products))
        self.diet_tags = sorted(set(tag for p in products for tag in p['diet_tags']))
        self.aisles = sorted(set(p['aisle_id'] for p in products))

        # Mapping for one-hot encoding
        self.category_to_idx = {cat: i for i, cat in enumerate(self.categories)}
        self.tag_to_idx = {tag: i for i, tag in enumerate(self.diet_tags)}
        self.aisle_to_idx = {aisle: i for i, aisle in enumerate(self.aisles)}

    def encode(self, product):
        # One-hot category
        category_vec = np.zeros(len(self.categories))
        category_vec[self.category_to_idx[product['category']]] = 1

        # Multi-hot diet tags
        tag_vec = np.zeros(len(self.diet_tags))
        for tag in product['diet_tags']:
            tag_vec[self.tag_to_idx[tag]] = 1

        # One-hot aisle
        aisle_vec = np.zeros(len(self.aisles))
        aisle_vec[self.aisle_to_idx[product['aisle_id']]] = 1

        # Normalized price (simple min-max normalization assuming known range)
        # For demo, price range: $0 to $10
        price_norm = np.array([(product['price'] / 10)])

        # Combine all features into one vector
        feature_vec = np.concatenate([category_vec, tag_vec, aisle_vec, price_norm])
        return feature_vec

    def encode_all(self):
        features = []
        for p in self.products:
            features.append(self.encode(p))
        return np.array(features)

class ContentBasedRecommender:
    def __init__(self, product_features, product_names):
        from sklearn.metrics.pairwise import cosine_similarity
        self.product_features = product_features
        self.product_names = product_names
        self.product_to_index = {name: i for i, name in enumerate(product_names)}
        self.similarity_matrix = cosine_similarity(self.product_features)

    def recommend(self, product_name, top_k=5):
        if product_name not in self.product_to_index:
            return []

        idx = self.product_to_index[product_name]
        similarity_scores = self.similarity_matrix[idx]
        similar_indices = np.argsort(-similarity_scores)

        recommendations = []
        for i in similar_indices:
            if i == idx:
                continue
            recommendations.append((self.product_names[i], similarity_scores[i]))
            if len(recommendations) >= top_k:
                break
        return recommendations

if __name__ == "__main__":
    import json

    # Your product JSON data (paste here or load from file)
    products_data = {
      "products": [
        {
          "product_id": "p100",
          "name": "Almond Milk",
          "category": "Dairy",
          "aisle_id": "A1",
          "shelf_id": "S1",
          "price": 3.99,
          "barcode": "0123456789012",
          "image_url": "https://example.com/images/almond_milk.jpg",
          "diet_tags": ["vegan", "gluten-free", "nut-free"],
          "stock_quantity": 20
        },
        {
          "product_id": "p101",
          "name": "Cheddar Cheese",
          "category": "Dairy",
          "aisle_id": "A1",
          "shelf_id": "S2",
          "price": 5.49,
          "barcode": "0123456789013",
          "image_url": "https://example.com/images/cheddar_cheese.jpg",
          "diet_tags": ["vegetarian"],
          "stock_quantity": 10
        },
        {
          "product_id": "p102",
          "name": "Whole Wheat Bread",
          "category": "Bakery",
          "aisle_id": "A2",
          "shelf_id": "S3",
          "price": 2.99,
          "barcode": "0123456789014",
          "image_url": "https://example.com/images/whole_wheat_bread.jpg",
          "diet_tags": ["vegetarian"],
          "stock_quantity": 15
        },
        {
          "product_id": "p103",
          "name": "Orange Juice",
          "category": "Beverages",
          "aisle_id": "A3",
          "shelf_id": "S6",
          "price": 4.50,
          "barcode": "0123456789015",
          "image_url": "https://example.com/images/orange_juice.jpg",
          "diet_tags": ["vegan", "gluten-free"],
          "stock_quantity": 25
        },
        {
          "product_id": "p104",
          "name": "Organic Apples",
          "category": "Produce",
          "aisle_id": "A4",
          "shelf_id": "S7",
          "price": 1.20,
          "barcode": "0123456789016",
          "image_url": "https://example.com/images/organic_apples.jpg",
          "diet_tags": ["vegan", "gluten-free"],
          "stock_quantity": 50
        },
        {
          "product_id": "p110",
          "name": "Blueberry Muffin",
          "category": "Bakery",
          "aisle_id": "A2",
          "shelf_id": "S4",
          "price": 3.00,
          "barcode": "0123456789020",
          "image_url": "https://example.com/images/blueberry_muffin.jpg",
          "diet_tags": ["vegetarian"],
          "stock_quantity": 12
        },
        {
          "product_id": "p111",
          "name": "Potato Chips",
          "category": "Snacks",
          "aisle_id": "A5",
          "shelf_id": "S9",
          "price": 2.50,
          "barcode": "0123456789021",
          "image_url": "https://example.com/images/potato_chips.jpg",
          "diet_tags": ["vegan", "gluten-free"],
          "stock_quantity": 30
        },
        {
          "product_id": "p112",
          "name": "Carrot Sticks",
          "category": "Produce",
          "aisle_id": "A4",
          "shelf_id": "S8",
          "price": 1.50,
          "barcode": "0123456789022",
          "image_url": "https://example.com/images/carrot_sticks.jpg",
          "diet_tags": ["vegan", "gluten-free"],
          "stock_quantity": 40
        }
      ]
    }

    products = products_data["products"]
    product_names = [p['name'] for p in products]

    encoder = ProductFeatureEncoder(products)
    features = encoder.encode_all()

    recommender = ContentBasedRecommender(features, product_names)

    query = "Almond Milk"
    recommendations = recommender.recommend(query, top_k=3)

    print(f"Recommendations for '{query}':")
    for name, score in recommendations:
        print(f"- {name} (score: {score:.2f})")
