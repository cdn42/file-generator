import config as config

class cmp_tgz:

    def __init__(self, filename, sourcefile):
        # Return an object
        self.filename   =   filename
        self.extension  =   "tar"
        self.mimetype   =   "application/x-gtar"
        self.fullname   =   self.filename + "." + self.extension
        self.ospath = config.filespath() + self.fullname

        # Generate the file

        import tarfile

        tar = tarfile.open(self.ospath, "w:gz")
        tar.add(sourcefile)
        tar.close()

