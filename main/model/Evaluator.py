from model.Card import Card


class Evaluator:
    @staticmethod
    def compare_hands(hand1: list[Card], hand2: list[Card]) -> int:

        return 0
    
    @staticmethod
    def best_hand(cards: list[Card]) -> list[Card]:
        return []
    
    @staticmethod
    def mapper(hand: list[Card]) -> tuple[int, int, int, int, int, int]:
        ranks = []
        suits = []

        rankCount = {}

        for card in hand:
            ranks.append(card.rank)
            suits.append(card.suit)

        ranks.sort()

        for rank in ranks:
            if rank in rankCount:
                rankCount[rank] += 1
            else:
                rankCount[rank] = 1

        # check if straight
        straight = False
        straight_high = 0
        if len(rankCount) == 5:
            # normal straight
            if ranks[-1] - ranks[0] == 4:
                straight = True
                straight_high = ranks[-1]

            # starting with ace
            elif ranks == [2, 3, 4, 5, 14]:
                straight = True
                straight_high = 5


        # check if flush
        flush = False
        if len(set(suits)) == 1:
            flush = True

        # classify hand
        counts = sorted(rankCount.values(), reverse=True)

        if straight and flush: # straight flush
            hand_class = 8

            return (hand_class, straight_high, 0, 0, 0, 0)
        
        elif counts == [4, 1]: # quads
            hand_class = 7
            quad = 0
            kicker = 0

            for rank, count in rankCount.items():
                if count == 4:
                    quad = rank
                elif count == 1:
                    kicker = rank

            return (hand_class, quad, kicker, 0, 0, 0)
        
        elif counts == [3, 2]: # boat
            hand_class = 6
            trip = 0
            pair = 0

            for rank, count in rankCount.items():
                if count == 3:
                    trip = rank
                elif count == 2:
                    pair = rank
            return (hand_class, trip, pair, 0, 0, 0)
        
        elif flush: # flush
            hand_class = 5

            return (hand_class, ranks[-1], ranks[-2], ranks[-3], ranks[-4], ranks[-5])
        
        elif straight: # straight
            hand_class = 4

            return (hand_class, straight_high, 0, 0, 0, 0)
        
        elif counts == [3, 1, 1]: # set
            hand_class = 3
            trip = 0
            kickers = []

            for rank, count in rankCount.items():
                if count == 3:
                    trip = rank
                else:
                    kickers.append(rank)
            
            kickers.sort(reverse = True)
            return (hand_class, trip, kickers[0], kickers[1], 0, 0)
        
        elif counts == [2, 2, 1]: # two pair
            hand_class = 2
            pairs = []
            kicker = 0

            for rank, count in rankCount.items():
                if count == 2:
                    pairs.append(rank)
                else:
                    kicker = rank
            
            pairs.sort(reverse = True)
            return (hand_class, pairs[0], pairs[1], kicker, 0, 0)

        elif counts == [2, 1, 1, 1]: # pair
            hand_class = 1
            pair = 0
            kickers = []

            for rank, count in rankCount.items():
                if count == 2:
                    pair = rank
                else:
                    kickers.append(rank)

            kickers.sort(reverse = True)
            return (hand_class, pair, kickers[0], kickers[1], kickers[2], 0)
        else:
            hand_class = 0
            return (hand_class, ranks[-1], ranks[-2], ranks[-3], ranks[-4], ranks[-5])
