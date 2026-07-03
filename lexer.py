"""
cyberHunt Lexer - Tokenizes Roman Urdu code
Complete lexer with all token types
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Keywords
    SHURO = auto()          # start
    KHATAM = auto()         # end
    LIKHO = auto()          # print
    AGAR = auto()           # if
    VARNA = auto()          # else
    JABBTAK = auto()        # while
    FUNC = auto()           # function
    RETURN = auto()         # return
    
    # Operators
    ASSIGN = auto()         # =
    PLUS = auto()           # jodo (addition)
    MINUS = auto()          # ghatao (subtraction)
    MULTIPLY = auto()       # gunaa (multiplication)
    DIVIDE = auto()         # bhago (division)
    
    # Comparison
    GREATER = auto()        # bara (>)
    LESS = auto()           # chhota (<)
    EQUAL = auto()          # barabar (==)
    
    # Special
    INPUT = auto()          # ?
    COLOR_TEXT = auto()     # #1, #2, etc
    COLOR_BG = auto()       # ##1, ##2, etc
    
    # Delimiters
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    COMMA = auto()          # ,
    SEMICOLON = auto()      # ;
    NEWLINE = auto()
    
    # End of file
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"

class Lexer:
    """Complete tokenizer for Roman Urdu code"""
    
    KEYWORDS = {
        'shuro': TokenType.SHURO,
        'khatam': TokenType.KHATAM,
        'likho': TokenType.LIKHO,
        'agar': TokenType.AGAR,
        'varna': TokenType.VARNA,
        'jabbtak': TokenType.JABBTAK,
        'func': TokenType.FUNC,
        'return': TokenType.RETURN,
        'jodo': TokenType.PLUS,
        'ghatao': TokenType.MINUS,
        'gunaa': TokenType.MULTIPLY,
        'bhago': TokenType.DIVIDE,
        'bara': TokenType.GREATER,
        'chhota': TokenType.LESS,
        'barabar': TokenType.EQUAL,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        """Raise lexer error"""
        raise SyntaxError(f"Lexer Error at line {self.line}, column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Look ahead at character"""
        pos = self.position + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Move to next character"""
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        """Skip whitespace except newlines"""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip comments starting with //"""
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_string(self, quote_char: str) -> str:
        """Read string literal"""
        value = ""
        self.advance()  # Skip opening quote
        
        while True:
            char = self.peek()
            if char is None:
                self.error("Unterminated string")
            if char == quote_char:
                self.advance()
                break
            if char == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote_char:
                    value += quote_char
                else:
                    value += next_char
            else:
                value += self.advance()
        
        return value
    
    def read_number(self):
        """Read number literal (integer or float)"""
        num_str = ""
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        
        if '.' in num_str:
            return float(num_str)
        return int(num_str)
    
    def read_identifier(self) -> str:
        """Read identifier or keyword"""
        ident = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        return ident
    
    def read_color(self) -> tuple:
        """Read color code like #2 or ##3"""
        hash_count = 0
        start_col = self.column
        
        while self.peek() == '#':
            hash_count += 1
            self.advance()
        
        color_num = ""
        while self.peek() and self.peek().isdigit():
            color_num += self.advance()
        
        if not color_num:
            self.error("Invalid color code")
        
        return (hash_count, int(color_num))
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            # Comments
            if self.peek() == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            char = self.peek()
            line = self.line
            column = self.column
            
            # Newlines
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, column))
                continue
            
            # Strings
            if char == '"' or char == "'":
                value = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, value, line, column))
            
            # Numbers
            elif char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
            
            # Colors
            elif char == '#':
                hash_count, color_num = self.read_color()
                if hash_count == 1:
                    self.tokens.append(Token(TokenType.COLOR_TEXT, color_num, line, column))
                else:
                    self.tokens.append(Token(TokenType.COLOR_BG, color_num, line, column))
            
            # Identifiers and Keywords
            elif char.isalpha() or char == '_':
                ident = self.read_identifier()
                token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, ident, line, column))
            
            # Operators and Delimiters
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, '=', line, column))
            
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', line, column))
            
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', line, column))
            
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', line, column))
            
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, column))
            
            elif char == '?':
                self.advance()
                self.tokens.append(Token(TokenType.INPUT, '?', line, column))
            
            else:
                self.error(f"Unexpected character: {char}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
