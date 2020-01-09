import config as config

class cmp_tar:

    def __init__(self, filename, sourcefile):
        # Return an object
        self.filename   =   filename
        self.extension  =   "tar"
        self.mimetype   =   "application/x-tar"
        self.fullname   =   self.filename + "." + self.extension
        self.ospath = config.filespath() + self.fullname

        # Generate the file

        import tarfile

        tar = tarfile.open(self.ospath, "w")
        tar.add(sourcefile)
        tar.close()

