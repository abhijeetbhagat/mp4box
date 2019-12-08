def parse_iods(reader, my_size):
    # TODO abhi: skip iods parsing for now
    reader.skip(my_size - 8)  # -8 since we have already parse the length and box name
    return None
