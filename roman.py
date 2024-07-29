def to_rom(num):
    val_dict = {"M": 1000, "CM": 900, "D": 500, "CD": 400, "C": 100, "XC": 90,
                "L": 50, "XL": 40, "X": 10, "IX": 9, "V": 5, "IV": 4, "I": 1}
    rom_str = ""
    remainder = num

    for rom_digit, val in val_dict.items():
        multiplier = remainder // val
        remainder = remainder % val
        rom_str += (rom_digit * multiplier)

    return rom_str


def to_num(rom_str):
    # Extra zero-functionality for special occassions
    if rom_str[0] == 'O':
        return 0

    val_dict = {"I": 1, "V": 5, "X": 10, "L": 50,
                "C": 100, "D": 500, "M": 1000}
    num = 0
    prev_val = 0

    for char in rom_str[::-1]:
        val = val_dict[char]
        if val < prev_val:
            num -= val
        else:
            num += val
            prev_val = val

    return num
