

def debug(fun):
    def tmp(self, *args, **kwargs):
        try:
            str_args = str(args)
        except Exception as e:
            str_args = "Error args"

        try:
            str_kwargs = str(kwargs)
        except Exception as e:
            str_kwargs = "Error kwargs"

        try:
            self.log.debug(
                '|   > | %s.%s args: %s kwargs: %s',
                self.__class__.__name__, fun.__name__, str_args, str_kwargs)
        except Exception as e:
            self.log.debug(
                '|   > | %s.%s args: %s kwargs: %s',
                self.__class__.__name__, fun.__name__,
                str_args[:200], str_kwargs[:200])

        result = fun(self, *args, **kwargs)

        try:
            str_result = str(result)
        except Exception as e:
            str_result = "Error result"

        try:
            self.log.debug(
                '| <   | %s.%s result: %s'
                % (self.__class__.__name__, fun.__name__, str_result))
        except Exception as e:
            self.log.debug(
                '| <   | %s.%s result: %s'
                % (self.__class__.__name__, fun.__name__, str_result[:200]))

        return result
    return tmp
