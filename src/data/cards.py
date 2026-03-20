import json
import requests

from utils.config import ROOT


def get_cards() -> list:
    # Use card data from local json
    cards_path = ROOT / "src" / "data" / "cards.json"

    if cards_path.exists():
        print(f"[data.cards.get_cards] Using local cards.json from {cards_path}")
        with open(cards_path) as f:
            return json.load(f)

    # Fetch card data json from official source
    cards_url = "https://raw.githubusercontent.com/the-fab-cube/flesh-and-blood-cards/refs/heads/omens-of-the-third-age/json/english/card.json"
    print(f"[data.cards.get_cards] No local card data. Fetching cards from {cards_url}")
    response = requests.get(cards_url)
    response.raise_for_status()
    cards = response.json()

    # Ensure directory exists and save locally
    cards_path.parent.mkdir(parents=True, exist_ok=True)

    with open(cards_path, "w") as f:
        json.dump(cards, f)

    return cards


def get_matches(keyword: str, cards: list) -> list:
    # Return list of "Name (Colour)"
    keyword = keyword.lower()

    matches: list = []
    for card in cards:
        card_name_lower = card["name"].lower()
        if keyword in card_name_lower:
            matches.append(card)
            print(f"[data.cards.get_matches] {card['name']} ({card['color']})")

    return matches
