def integer(line):
    while True:
        try:
            _int = input(line).strip()
            if not _int:  # if int is empty
                raise ValueError('No data was entered.')
            if not _int.isdigit():  # if int is not a number
                raise ValueError('Please enter an integer.')
            return _int
        except ValueError as e:
            print(e)

def main():
    ...

if __name__ == "__main__":
    main()