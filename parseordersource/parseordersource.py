class ParseOrderSource:

    '''
    Provides continouus stream of ParseOrder objects to be processed
    '''

    def __init__(self, config):

        '''
        Setup an instance of ParseOrderSource
        :param **config: Configuration passed to implementation
        '''
        pass

    def getOrder(self):

        '''
        Get the next ParseOrder
        '''
        pass
#
#    def markAsProcessed(id):
#
#        '''
#        Marks consumed RawPageData objects up until and including
#        the one specified through the given ID as processed and
#        propagates this information further upstream.
#        '''
#        pass
