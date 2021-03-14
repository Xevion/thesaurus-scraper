import demjson


class CustomJSON(demjson.JSON):
    """
    A simple override for the demjson.JSON class to map all instances of undefined into 'null'.
    """

    def encode_undefined(self, state):
        """Return null as undefined."""
        state.append('null')
