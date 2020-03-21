
class Source:
    def __init__(self, filename):
        self.filename = filename
        self.rowNumber = 0
        self.columnNumber = 0
        f = open(filename, "r")
        self.lines = []
        for line in f:
            self.lines.append(line)
        f.close()

    def __handleline__(self):
        if self.columnNumber >= len(self.lines[self.rowNumber]):
            self.rowNumber = self.rowNumber + 1
            self.columnNumber = 0

    def eof(self):
        return self.rowNumber >= len(self.lines)

    def getChar(self):
        if self.eof():
            return ''
        char = self.lines[self.rowNumber][self.columnNumber]
        self.columnNumber = self.columnNumber + 1
        self.__handleline__()
        return char

    def peek(self):
        if not self.eof():
            if self.columnNumber < len(self.lines[self.rowNumber]):
                return self.lines[self.rowNumber][self.columnNumber]
            elif self.rowNumber + 1 < len(self.lines):
                return self.lines[self.rowNumber + 1][0]
            else:
                return ''
        else:
            return ''

    def getCurrentPosition(self):
        """
        Get current cursor position of source.
        These indexes start from 1, to ease in
        error correction from a buffer.
        """
        return (self.columnNumber + 1, self.rowNumber + 1)

    def reverseOnePosition(self):
        if (self.columnNumber == 0 and self.rowNumber == 0):
            return
        elif self.columnNumber == 0:
            self.rowNumber = self.rowNumber - 1
            self.columnNumber = len(self.lines[self.rowNumber]) - 1
        else:
            self.columnNumber = self.columnNumber - 1
