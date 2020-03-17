
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
        self.scanFuncs = [
            Scanner.scanIdentifierOrKeyword,
            Scanner.scanNumber,
            Scanner.scanString,
            Scanner.scanOperand,
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
            return Token('eof', '', position, position)
        position = self.src.getCurrentPosition()
        for func in self.scanFuncs:
            possibleToken = func(self.src)
            if possibleToken is not False:
                return possibleToken
        return errortoken

    def screening(self):
        value = True
        while value:
            self.screenWhiteSpace()
            value = Scanner.screenMultilineComment(self.src)
            self.screenWhiteSpace()
            value = value or Scanner.screenSingleLineComment(self.src)

    def screenWhiteSpace(self):
        while (self.src.peek() in [' ', '\t', '\n']):
            self.src.getChar()

    def scanNumber(src):
        def scanDigitPart(src):
            if src.peek().isdigit():
                lexeme = ''
                while src.peek().isdigit():
                    lexeme = lexeme + src.getChar()
                return lexeme
            return False
        startPos = src.getCurrentPosition()
        lexeme = scanDigitPart(src)
        if lexeme is not False:
            if src.peek() == '.':
                lookAhead = src.getChar()
                if src.peek() == '.':
                    column, row = src.getCurrentPosition()
                    src.reverseOnePosition()
                    return Token('integer', lexeme,
                                 startPos, src.getCurrentPosition())
                lexeme = lexeme + lookAhead
                lexeme = lexeme + scanDigitPart(src)
                return Token('decimal', lexeme,
                             startPos, src.getCurrentPosition())
            else:
                return Token('integer', lexeme,
                             startPos, src.getCurrentPosition())
        return False

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
                lexeme = lexeme + src.getChar()
            if src.peek() == '"':
                lexeme = lexeme + src.getChar()
            return Token('string_literal',
                         lexeme, startPos,
                         src.getCurrentPosition())
        return False

    def scanIdentifierOrKeyword(src):
        startPos = src.getCurrentPosition()
        if src.peek().isalpha():
            lexeme = ''
            while src.peek().isalpha() or src.peek() == '_':
                lexeme = lexeme + src.getChar()
            if lexeme in Scanner.keywords:
                return Token(lexeme, lexeme,
                             startPos, src.getCurrentPosition())
            return Token('identifier', lexeme,
                         startPos, src.getCurrentPosition())
        return False

    def scanOperand(src):
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
                while not src.eof():
                    src.getChar()
                    if src.peek() == '*':
                        src.getChar()
                        if src.peek() == '/':
                            src.getChar()
                            return True
                raise LexicalError('Runaway comment')
                return False
            else:
                src.reverseOnePosition()
                return False
