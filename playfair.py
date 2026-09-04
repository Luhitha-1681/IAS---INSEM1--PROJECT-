def generate_key_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()

    for ch in key:
        if ch.isalpha() and ch not in used:
            used.add(ch)
            matrix.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            used.add(ch)
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0,25,5)]


def find_position(matrix, ch):
    if ch == 'J':
        ch = 'I'
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j


def prepare_text(text):
    text = text.upper().replace("J","I")
    text = "".join([c for c in text if c.isalpha()])

    result = ""
    i = 0

    while i < len(text):
        a = text[i]

        if i+1 < len(text):
            b = text[i+1]
            if a == b:
                result += a + "X"
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + "X"
            i += 1

    return result


def encrypt(text,key):
    matrix = generate_key_matrix(key)
    text = prepare_text(text)

    cipher = ""

    for i in range(0,len(text),2):

        a = text[i]
        b = text[i+1]

        r1,c1 = find_position(matrix,a)
        r2,c2 = find_position(matrix,b)

        if r1 == r2:

            cipher += matrix[r1][(c1+1)%5]
            cipher += matrix[r2][(c2+1)%5]

        elif c1 == c2:

            cipher += matrix[(r1+1)%5][c1]
            cipher += matrix[(r2+1)%5][c2]

        else:

            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher


def decrypt(cipher,key):

    matrix = generate_key_matrix(key)

    text = ""

    for i in range(0,len(cipher),2):

        a = cipher[i]
        b = cipher[i+1]

        r1,c1 = find_position(matrix,a)
        r2,c2 = find_position(matrix,b)

        if r1 == r2:

            text += matrix[r1][(c1-1)%5]
            text += matrix[r2][(c2-1)%5]

        elif c1 == c2:

            text += matrix[(r1-1)%5][c1]
            text += matrix[(r2-1)%5][c2]

        else:

            text += matrix[r1][c2]
            text += matrix[r2][c1]

    return text