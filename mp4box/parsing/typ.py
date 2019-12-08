def parse_typ(reader, my_size, klass):
    major_brand = reader.read32_as_str()
    minor_version = reader.read32()
    compatible_brands = []
    cnt = 0
    while cnt < my_size - 16:
        compatible_brands.append(reader.read32_as_str())
        cnt += 4
    box = klass(my_size, major_brand, minor_version, compatible_brands)
    return box
