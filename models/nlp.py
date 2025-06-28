import spacy
from spacy.matcher import PhraseMatcher
from difflib import get_close_matches

class IntentParser:
    def __init__(self, product_names=None):
        self.nlp = spacy.load("en_core_web_sm")

        # Known product names (load dynamically in production)
        if product_names is None:
            self.known_products = [
                "almond milk", "cheddar cheese", "whole wheat bread",
                "orange juice", "organic apples", "blueberry muffin",
                "potato chips", "carrot sticks"
            ]
        else:
            self.known_products = product_names

        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(p) for p in self.known_products]
        self.matcher.add("PRODUCT", patterns)

    def detect_intent(self, text):
        """Basic intent detection based on keyword matching"""
        lowered = text.lower()
        if any(w in lowered for w in ["find", "where", "locate", "get"]):
            return "navigate"
        elif any(w in lowered for w in ["recommend", "suggest", "like"]):
            return "recommend"
        elif any(w in lowered for w in ["buy", "add to cart", "purchase"]):
            return "add_to_cart"
        return "unknown"

    def fuzzy_match_entity(self, span_text):
        """Fuzzy match input to known products"""
        matches = get_close_matches(span_text.lower(), self.known_products, n=1, cutoff=0.7)
        return matches[0] if matches else span_text

    def parse(self, text):
        doc = self.nlp(text)
        intent = self.detect_intent(text)

        # Phrase matcher for known products
        matches = self.matcher(doc)
        products = set()

        for match_id, start, end in matches:
            span = doc[start:end]
            products.add(span.text.lower())

        # Also try noun chunks (for fuzzy match fallback)
        for chunk in doc.noun_chunks:
            cleaned = chunk.text.strip().lower()
            if cleaned not in products:
                match = self.fuzzy_match_entity(cleaned)
                if match in self.known_products:
                    products.add(match)

        return intent, list(products)
