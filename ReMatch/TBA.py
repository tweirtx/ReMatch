import tbapi


class TBA:
    with open('tbakey.txt', 'r') as key:
        client = tbapi.TBAParser(key.read(), cache=False)

    def DB_setup(self, key, timestamp):
        matches = self.client.get_event() # Todo once I have the right method available
        for match in matches:
            print(match.time, match.key)
