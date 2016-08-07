import logging
import curses

class MonitorWindowBase:
    '''
    Base class for all windows of the Godville Monitor

    '''
    def __init__(self,
                 title,
                 height,
                 width,
                 parent_window,
                 y = 0,
                 x = 0):

        self.title        = title
        self.text_entries = []

        self.height      = height
        self.width       = width
        self.x           = x
        self.y           = y
        self.window      = parent_window.subwin(self.height,
                                                 self.width,
                                                 self.y,
                                                 self.x)
        self.window.box()
        self.init_text_entries()

    def add_text_entry(self, entry):
        self.text_entries.append(entry)

    def update(self, state):
        logging.debug('%s: Updating window \'%s\'',
                      self.update.__name__,
                      self.title)

        self.window.erase()
        self.window.box()
        self.window.addstr(0, 2, self.title)

        for entry in self.text_entries:
            entry.update(state)

        self.write_text(self.text_entries)
        self.window.refresh()

    def init_text_entries(self):
        pass

    def split_text(self, text, length):
        chunks = []

        if len(text) == 0:
            chunks.append('')

        for i in range(0, len(text), length):
            chunks.append(text[i:i + length])

        return chunks

    def write_text_chunks(self, chunks, color, start_line):
        for i, chunk in enumerate(chunks):
            self.window.addnstr(start_line + i,
                                1,
                                chunk,
                                self.width - 2,
                                curses.color_pair(color))


    def write_text(self, entries):
        offset = 1 # Offset for correcting line number for splitted text

        for i, entry in enumerate(entries):
            logging.debug('%s: Writting text \'%s\'',
                          self.write_text.__name__,
                          entry.text)

            chunks = self.split_text(entry.text, self.width - 2)
            self.write_text_chunks(chunks, entry.color, i + offset)
            offset += len(chunks) - 1
