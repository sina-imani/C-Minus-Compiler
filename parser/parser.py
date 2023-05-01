import scanner.scanner as scanner


def run():
    scanner.get_next_token()
    while True:
        result = scanner.get_next_token()
        print(result)
        if result[0] == '$':
            break
