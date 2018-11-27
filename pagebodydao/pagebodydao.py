class PageBodyDao:

    '''
    Provides interface to retrieve HTML bodies from
    persistent storage
    '''

    def __init__(self, **config):

        '''
        Setup an instance of PageBodyDao
        :param **config: Configuration passed to implementation
        '''
        pass

    def retrieveBody(self, parseOrder):

        '''
        Retrieves a string containing the page body associated
        with the given parse order.
        '''
        pass

    def storeText(self, parseOrder, text):
        pass
