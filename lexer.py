"""
cyberHunt Lexer - Tokenizes Roman Urdu code
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Keywords
    SHURO = auto()          # Start
    KHATAM = auto()         # End
    AGAR = auto()           # If
    VARNA = auto()          # Else
    JABBTAK = auto()        # While
    FUNC = auto()           # Function
    RETURN = auto()         # Return
    
    # Operators
    BARABAR = auto()        # Assignment (=)
    BARA = auto()           # Greater than
    CHHOTA = auto()         # Less than
    JODO = auto()           # Addition
    GHATAO = auto()         # Subtraction
    GUNAA = auto()          # Multiplication
    BHAGO = auto()          # Division
    
    # I/O
    LIKHO = auto()          # Print
    INPUT = auto()          # Input (?)
    
    # Literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    QUOTE = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class Lexer:
    KEYWORDS = {
        'shuro': TokenType.SHURO,
        'khatam': TokenType.KHATAM,
        'agar': TokenType.AGAR,
        'varna': TokenType.VARNA,
        'jabbtak': TokenType.JABBTAK,
        'func': TokenType.FUNC,
        'return': TokenType.RETURN,
        'likho': TokenType.LIKHO,
    }
    
    OPERATORS = {
        'bara': TokenType.BARA,
        'chhota': TokenType.CHHOTA,
        'barabar': TokenType.BARABAR,
        'jodo': TokenType.JODO,
        'ghatao': TokenType.GHATAO,
        'gunaa': TokenType.GUNAA,
        'bhago': TokenType.BHAGO,
    }
    
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def error(self, msg: str):
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {msg}")
    
    def peek(self, offset=0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.code):
            return self.code[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.code):
            char = self.code[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_string(self) -> str:
        quote = self.advance()  # Skip opening quote
        value = ""
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                else:
                    value += next_char
            else:
                value += self.advance()
        
        if self.peek() == quote:
            self.advance()  # Skip closing quote
        else:
            self.error("Unclosed string")
        
        return value
    
    def read_number(self) -> int:
        num = ""
        while self.peek() and self.peek().isdigit():
            num += self.advance()
        return int(num) if num else 0
    
    def read_identifier(self) -> str:
        ident = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        return ident
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.code):
            self.skip_whitespace()
            
            if self.pos >= len(self.code):
                break
            
            # Skip comments
            if self.peek() == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            char = self.peek()
            line = self.line
            col = self.column
            
            # Newline
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, col))
                continue
            
            # String
            if char in '"\'':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, line, col))
                continue
            
            # Number
            if char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, col))
                continue
            
            # Input operator ?
            if char == '?':
                self.advance()
                self.tokens.append(Token(TokenType.INPUT, '?', line, col))
                continue
            
            # Assignment operator =
            if char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.BARABAR, '=', line, col))
                continue
            
            # Semicolon in color codes
            if char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, ';', line, col))
                continue
            
            # Identifier or Keyword
            if char.isalpha() or char == '_':
                ident = self.read_identifier()
                
                if ident in self.KEYWORDS:
                    self.tokens.append(Token(self.KEYWORDS[ident], ident, line, col))
                elif ident in self.OPERATORS:
                    self.tokens.append(Token(self.OPERATORS[ident], ident, line, col))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, ident, line, col))
                continue
            
            # Unknown character
            self.error(f"Unknown character: '{char}'")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
