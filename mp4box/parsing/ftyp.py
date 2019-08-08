from mp4box.box import FileTypeBox

def parse_ftyp(reader, my_size):
    major_brand = reader.read32_as_str()
    minor_version = reader.read32()
    compatible_brands = []
    cnt = 0
    while cnt < my_size + 4 - 16 - 4:
        compatible_brands.append(reader.read32_as_str())
        cnt += 4
    box = FileTypeBox(my_size, major_brand, minor_version, compatible_brands)
    return box


