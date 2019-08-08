from mp4box.box import VideoMediaHeaderBox

def parse_vmhd(reader, size):
    reader.read32()
    box = VideoMediaHeaderBox(size, 0, 1)
    box.graphics_mode = reader.reader16()
    box.opcolor.append(reader.reader16())
    box.opcolor.append(reader.reader16())
    box.opcolor.append(reader.reader16()) 
    return box
