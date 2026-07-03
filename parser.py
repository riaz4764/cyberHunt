"""
cyberHunt Parser - Converts tokens to AST
"""

from typing import List, Dict, Any, Optional
from lexer import Token, TokenType, Lexer

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current_token()
        raise SyntaxError(f"Line {token.line}, Col {token.column}: {msg}")
    
    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # Return EOF token
    
    def peek_token(self, offset=1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        return self.advance()
    
    def parse(self) -> Dict:
        """Parse tokens into AST"""
        statements = []
        
        self.skip_newlines()
        
        # Expect 'shuro' keyword
        self.expect(TokenType.SHURO)
        self.skip_newlines()
        
        # Parse statements until 'khatam'
        while self.current_token().type != TokenType.KHATAM:
            if self.current_token().type == TokenType.EOF:
                self.error("Expected 'khatam' but got EOF")
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        # Expect 'khatam' keyword
        self.expect(TokenType.KHATAM)
        
        return {
            'type': 'program',
            'statements': statements
        }
    
    def parse_statement(self) -> Optional[Dict]:
        """Parse a single statement"""
        self.skip_newlines()
        
        token = self.current_token()
        
        if token.type == TokenType.LIKHO:
            return self.parse_likho()
        
        elif token.type == TokenType.AGAR:
            return self.parse_if()
        
        elif token.type == TokenType.JABBTAK:
            return self.parse_while()
        
        elif token.type == TokenType.RETURN:
            return self.parse_return()
        
        elif token.type == TokenType.IDENTIFIER:
            # Could be assignment or input
            return self.parse_assignment_or_input()
        
        elif token.type in [TokenType.NEWLINE, TokenType.EOF, TokenType.KHATAM, TokenType.VARNA]:
            self.advance()
            return None
        
        else:
            self.error(f"Unexpected token: {token.type}")
    
    def parse_likho(self) -> Dict:
        """Parse likho (print) statement"""
        self.expect(TokenType.LIKHO)
        
        args = []
        
        # Parse arguments until newline
        while self.current_token().type not in [TokenType.NEWLINE, TokenType.EOF, TokenType.KHATAM, TokenType.VARNA]:
            arg = self.parse_expression()
            args.append(arg)
            
            # Check for more arguments (separated by space implicitly)
            if self.current_token().type in [TokenType.STRING, TokenType.NUMBER, TokenType.IDENTIFIER]:
                continue
            else:
                break
        
        return {
            'type': 'likho',
            'args': args
        }
    
    def parse_if(self) -> Dict:
        """Parse agar (if) statement"""
        self.expect(TokenType.AGAR)
        
        condition = self.parse_expression()
        self.skip_newlines()
        
        then_body = []
        while self.current_token().type not in [TokenType.VARNA, TokenType.KHATAM, TokenType.EOF]:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        
        else_body = []
        if self.current_token().type == TokenType.VARNA:
            self.advance()
            self.skip_newlines()
            
            while self.current_token().type not in [TokenType.KHATAM, TokenType.EOF]:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
        
        if self.current_token().type == TokenType.KHATAM:
            self.advance()
        
        return {
            'type': 'if',
            'condition': condition,
            'then_body': then_body,
            'else_body': else_body
        }
    
    def parse_while(self) -> Dict:
        """Parse jabbtak (while) statement"""
        self.expect(TokenType.JABBTAK)
        
        condition = self.parse_expression()
        self.skip_newlines()
        
        body = []
        while self.current_token().type not in [TokenType.KHATAM, TokenType.EOF]:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.KHATAM)
        
        return {
            'type': 'while',
            'condition': condition,
            'body': body
        }
    
    def parse_return(self) -> Dict:
        """Parse return statement"""
        self.expect(TokenType.RETURN)
        value = self.parse_expression()
        return {
            'type': 'return',
            'value': value
        }
    
    def parse_assignment_or_input(self) -> Dict:
        """Parse assignment or input statement"""
        var_name = self.expect(TokenType.IDENTIFIER).value
        
        if self.current_token().type == TokenType.BARABAR:
            # Assignment
            self.advance()
            
            if self.current_token().type == TokenType.INPUT:
                # Input assignment: naam = ?
                self.advance()
                prompt = None
                
                # Check if there's a prompt string
                if self.current_token().type == TokenType.STRING:
                    prompt = self.parse_expression()
                
                return {
                    'type': 'input',
                    'var': var_name,
                    'prompt': prompt
                }
            else:
                # Regular assignment
                value = self.parse_expression()
                return {
                    'type': 'assignment',
                    'name': var_name,
                    'value': value
                }
        
        elif self.current_token().type == TokenType.INPUT:
            # Input without assignment
            self.advance()
            prompt = None
            if self.current_token().type == TokenType.STRING:
                prompt = self.parse_expression()
            
            return {
                'type': 'input',
                'var': var_name,
                'prompt': prompt
            }
        
        else:
            self.error(f"Expected '=' or '?' after identifier")
    
    def parse_expression(self) -> Any:
        """Parse an expression"""
        return self.parse_comparison()
    
    def parse_comparison(self) -> Any:
        """Parse comparison operations"""
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.BARA, TokenType.CHHOTA]:
            op_token = self.advance()
            op = 'bara' if op_token.type == TokenType.BARA else 'chhota'
            right = self.parse_additive()
            
            left = {
                'type': 'binop',
                'op': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_additive(self) -> Any:
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.JODO, TokenType.GHATAO]:
            op_token = self.advance()
            op = 'jodo' if op_token.type == TokenType.JODO else 'ghatao'
            right = self.parse_multiplicative()
            
            left = {
                'type': 'binop',
                'op': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_multiplicative(self) -> Any:
        """Parse multiplication and division"""
        left = self.parse_primary()
        
        while self.current_token().type in [TokenType.GUNAA, TokenType.BHAGO]:
            op_token = self.advance()
            op = 'gunaa' if op_token.type == TokenType.GUNAA else 'bhago'
            right = self.parse_primary()
            
            left = {
                'type': 'binop',
                'op': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_primary(self) -> Any:
        """Parse primary expressions"""
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        
        elif token.type == TokenType.STRING:
            self.advance()
            return token.value
        
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            return {
                'type': 'variable',
                'name': name
            }
        
        else:
            self.error(f"Unexpected token in expression: {token.type}")
