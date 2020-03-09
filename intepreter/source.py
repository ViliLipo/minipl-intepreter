
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

    def handleLine(self):
        if self.columnNumber >= len(self.lines[self.rowNumber]):
            self.rowNumber = self.rowNumber + 1
            self.columnNumber = 0

    def eof(self):
        return (self.rowNumber >= len(self.lines)
                or (self.rowNumber == len(self.lines) - 1
                    and
                    self.columnNumber == len(self.lines[self.rowNumber]) - 1))

    def getChar(self):
        self.handleLine()
        if self.eof():
            return False
        char = self.lines[self.rowNumber][self.columnNumber]
        self.columnNumber = self.columnNumber + 1
        return char

    def peek(self):
        if not self.eof():
            if self.columnNumber < len(self.lines[self.rowNumber]):
                return self.lines[self.rowNumber][self.columnNumber]
            elif self.rowNumber + 1 < len(self.lines):
                return self.lines[self.rowNumber + 1][0]
            else:
                return False
        else:
            return False

    def getCurrentPosition(self):
        return (self.columnNumber, self.rowNumber + 1)

    def setCurrentPosition(self, column, row):
        self.columnNumber = column - 1
        self.rowNumber = row - 1
