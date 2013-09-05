EXCEPTION_FORMATTER = ('Method {method_name} not implemented!'
                       '{class_name} is an abstract class meant only to guarantee a consistent'
                       'interface across different data sources.')


class DataSource(object):

    # Return all the answers submitted by User user_id.
    def get_user_answers(self, user_id):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='get_user_answers', class_name='DataSource'))

    # Return all questions with the given id or ids
    def get_questions(self, question_id_or_ids):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='get_questions', class_name='DataSource'))

    # Return a list of candidate questions to classify
    def get_candidate_questions(self, tags):
        raise NotImplementedError(
            EXCEPTION_FORMATTER.format(method_name='get_candidate_questions', class_name='DataSource'))
