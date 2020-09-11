class Config(object):
    __class_metadata_extractor = None

    @staticmethod
    def set_class_metadata_extractor(extractor_impl):
        Config.__class_metadata_extractor = extractor_impl

    @staticmethod
    def get_class_metadata_extractor():
        return Config.__class_metadata_extractor
