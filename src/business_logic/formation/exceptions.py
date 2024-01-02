class NoOnisepAPIException(Exception):
    """
    Raised when we cannot communicate wit Onisep API
    """

    pass


class ProcessFormationException(Exception):
    """
    Raised when we cannot process json formation
    """
