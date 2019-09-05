from mp4box.isofile import ISOFile

class MP4Box:
    def __init__(self, stream):
        self.file = ISOFile(stream)

    def get_info(self, stream): 
        self.file.parse()
        return self.file.get_all_info()

    def on_error(self, l):
        pass

    def on_ready(self, l):
        pass

    def on_moov_start(self, l):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def flush(self):
        pass
