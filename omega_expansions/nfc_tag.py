"""NFC Omega expansion card"""

class Tag:

    def read_card(self):
        print("Put a card on the NFC Reader......")
        #Read card
        card = Card()
        print("Card read successfully....")

        return card.id
