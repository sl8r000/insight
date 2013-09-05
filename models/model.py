EXCEPTION_FORMATTER = ('Method {method_name} not implemented!'
                       '{class_name} is an abstract class meant only to guarantee a consistent'
                       'interface across different models.')

class Model(object):
    
    def train(self, data_source, feature_extractor, truth_function):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='train', class_name='Model'))

    def recommend(self, data_source, user_id, number):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='recommend', class_name='Model'))

    def test(self, data_source, user_ids, feature_extractor, truth_function):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='recommend', class_name='Model'))
