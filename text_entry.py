class Colors:
    STANDART        = 1
    HEALTH_POINTS   = 2
    POWER_POINTS    = 3
    ATTENTION       = 4


class TextEntry:
    def __init__(self, predefined_text, key, width, color = Colors.STANDART):
        self._predefined_text = predefined_text
        self._key             = key
        self._width           = width
        self._color           = color
        self._attribute       = None
        self._text            = ''

    @property
    def predefined_text(self):
        return self._predefined_text

    @property
    def width(self):
        return self._width

    @property
    def key(self):
        return self._key

    @property
    def text(self):
        return self._text

    @property
    def text(self):
        return self._text

    @property
    def color(self):
        return self._color

    @property
    def attribute(self):
        return self._attribute

    @property
    def attribute(self, attribute):
        self._attribute = attribute

    def update(self, state, attribute = None):
        key_width   = self.width - len(self.predefined_text) - 2
        custom_text = ''
        text_format = '{0}{1:>{2}}'

        if self.key == '':
            self._text = ''
            return

        # In case of empty predefined text use center alignment
        if self.predefined_text == '':
            text_format = '{0}{1:^{2}}'

        try:
            custom_text = '{0}'.format(state[self.key])
        except KeyError:
            self._text = '{0} key not found'.format(self.key)
            return

        if key_width < 1:
            self._text = '{0} text doesn\'t fit'.format(key)
            return

        self._text = text_format.format(self.predefined_text,
                                        custom_text,
                                        key_width)

