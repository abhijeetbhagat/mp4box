from mp4box.box import AVCCConfigurationBox

def parse_avcc(reader, my_size):
    box = AVCCConfigurationBox(my_size)
    #TODO abhi: implement avcC parsing
    return box
