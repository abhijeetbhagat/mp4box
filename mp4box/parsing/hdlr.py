from mp4box.box import HandlerBox

def parse_hdlr(reader, size):
    version = reader.read32()
    box = HandlerBox(size, version, 0)
    box.predefined = reader.read32()
    box.handler_type = reader.read32_as_str()
    box.reserved.append(reader.read32())
    box.reserved.append(reader.read32())
    box.reserved.append(reader.read32())
    box.name = reader.readn_as_str(size - 32)
    return box
