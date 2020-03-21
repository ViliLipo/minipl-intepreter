
class Token:

    def __init__(self, tokenType, lexeme, startposition, endposition):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.endposition = endposition
        self.startposition = startposition

    def __str__(self):
        return 'Type: {}, Lexeme: {}'\
            .format(self.tokenType, self.lexeme)

    def __repr__(self):
        return self.__str__()


class LexicalError(Exception):
    pass


class Scanner:

    keywords = ['var', 'for', 'end', 'in', 'do', 'read',
                'print', 'int', 'string', 'bool', 'assert']

    def __init__(self, src):
        self.src = src
        # These scanner functions are called in order
        self.scanFuncs = [
            Scanner.scanIdentifierOrKeyword,
            Scanner.scanNumber,
            Scanner.scanString,
            Scanner.scanOperator,
            Scanner.scanSemicolon,
            Scanner.scanColonOrIdent,
            Scanner.scanBrackets,
            Scanner.scanRange,
        ]

    def scanNextToken(self):
        position = self.src.getCurrentPosition()
        errortoken = Token('error', '', position, position)
        try:
            self.screening()
        except LexicalError:
            return errortoken
        if self.src.eof():
            position = self.src.getCurrentPosition()
            return Token('eof', '', position, position)
        for func in self.scanFuncs:
            possibleToken = func(self.src)
            if possibleToken is not False:
                return possibleToken
        self.src.getChar()  # discard a bad character
        return errortoken

    def screening(self):
        commentFound = True
        while commentFound:
            self.screenWhiteSpace()
            commentFound = Scanner.screenMultilineComment(self.src)
            self.screenWhiteSpace()
            commentFound = (commentFound
                            or Scanner.screenSingleLineComment(self.src))

    def screenWhiteSpace(self):
        while (self.src.peek() in [' ', '\t', '\n']):
            self.src.getChar()

    def scanNumber(src):
        def scanDigitPart(src):
            startPos = src.getCurrentPosition()
            if src.peek().isdigit():
                lexeme = ''
                while src.peek().isdigit():
                    lexeme = lexeme + src.getChar()
                return Token('integer', lexeme,
                             startPos, src.getCurrentPosition())
            return False
        return scanDigitPart(src)

    def scanRange(src):
        startPos = src.getCurrentPosition()
        if src.peek() == '.':
            lexeme = src.getChar()
            if src.peek() == '.':
                lexeme = lexeme + src.getChar()
                return Token('..', lexeme, startPos, src.getCurrentPosition())
            else:
                return Token('error', '', startPos, src.getCurrentPosition())
        return False

    def scanString(src):
        startPos = src.getCurrentPosition()
        if src.peek() == '"':
            lexeme = src.getChar()
            while src.peek() != '"':
                if src.peek() == '\\':
                    lexeme = Scanner\
                        .__handleEscapeCharacters__(src, lexeme)
                else:
                    lexeme = lexeme + src.getChar()
            lexeme = lexeme + src.getChar()
            return Token('string_literal',
                         lexeme, startPos,
                         src.getCurrentPosition())
        return False

    def __handleEscapeCharacters__(src, lexeme):
        src.getChar()
        char = src.getChar()
        if char == '\\':
            lexeme = lexeme + '\\'
        if char == 'n':
            lexeme = lexeme + '\n'
        elif char == 't':
            lexeme = lexeme + '\t'
        elif char == '"':
            lexeme = lexeme + '"'
        return lexeme

    def scanIdentifierOrKeyword(src):
        startPos = src.getCurrentPosition()
        if src.peek().isalpha():
            lexeme = ''
            while src.peek().isalnum() or src.peek() == '_':
                lexeme = lexeme + src.getChar()
            if lexeme in Scanner.keywords:
                return Token(lexeme, lexeme,
                             startPos, src.getCurrentPosition())
            return Token('identifier', lexeme,
                         startPos, src.getCurrentPosition())
        return False

    def scanOperator(src):
        startPos = src.getCurrentPosition()
        if src.peek() in ['+', '-', '*', '/', '<', '=', '&', '!']:
            lexeme = src.getChar()
            return Token(lexeme, lexeme, startPos, src.getCurrentPosition())
        else:
            return False

    def scanSemicolon(src):
        startPos = src.getCurrentPosition()
        if src.peek() == ';':
            lexeme = src.getChar()
            return Token(lexeme, lexeme, startPos, src.getCurrentPosition())
        else:
            return False

    def scanColonOrIdent(src):
        startPos = src.getCurrentPosition()
        if src.peek() == ':':
            lexeme = src.getChar()
            if src.peek() == '=':
                lexeme = lexeme + src.getChar()
            return Token(lexeme, lexeme, startPos, src.getCurrentPosition())
        else:
            return False

    def scanBrackets(src):
        startPos = src.getCurrentPosition()
        if src.peek() in ['(', ')']:
            lexeme = src.getChar()
            return Token(lexeme, lexeme, startPos, src.getCurrentPosition())
        else:
            return False

    def screenSingleLineComment(src):
        if src.peek() == '/':
            src.getChar()
            if src.peek() == '/':
                src.getChar()
                while not (src.peek() == '\n' or src.eof()):
                    src.getChar()
                return True
            else:
                src.reverseOnePosition()
                return False

    def screenMultilineComment(src):
        if src.peek() == '/':
            src.getChar()
            if src.peek() == '*':
                openCount = 1
                while not src.eof():
                    src.getChar()
                    if src.peek() == '/':
                        src.getChar()
                        if src.peek() == '*':
                            src.getChar()
                            openCount = openCount + 1
                    if src.peek() == '*':
                        src.getChar()
                        if src.peek() == '/':
                            src.getChar()
                            openCount = openCount - 1
                            if openCount == 0:
                                return True
                raise LexicalError('Runaway comment')
            else:
                src.reverseOnePosition()
                return False
