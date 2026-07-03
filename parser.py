"""
cyberHunt Parser - Complete AST builder
Converts tokens to Abstract Syntax Tree
"""

from typing import List, Dict, Any, Optional
from lexer import Token, TokenType

class ASTNode:
    """Base AST Node"""
    pass

class Parser:
    """Parse tokens into AST"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current_token()
        raise SyntaxError(f"Parse Error at line {token.line}, col {token.column}: {msg}")
    
    def current_token(self) -> Token:
        """Get current token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset: int = 1) -> Token:
        """Look ahead"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        """Move to next token"""
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect specific token type"""
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        return self.advance()
    
    def parse(self) -> Dict:
        """Parse entire program"""
        statements = []
        self.skip_newlines()
        
        # Start with 'shuro'
        self.expect(TokenType.SHURO)
        self.skip_newlines()
        
        # Parse statements until 'khatam'
        while self.current_token().type != TokenType.KHATAM:
            if self.current_token().type == TokenType.EOF:
                self.error("Expected 'khatam' but reached EOF")
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        # End with 'khatam'
        self.expect(TokenType.KHATAM)
        
        return {
            'type': 'program',
            'statements': statements
        }
    
    def parse_statement(self) -> Optional[Dict]:
        """Parse single statement"""
        self.skip_newlines()
        
        token = self.current_token()
        
        # Print statement
        if token.type == TokenType.LIKHO:
            return self.parse_likho()
        
        # If statement
        elif token.type == TokenType.AGAR:
            return self.parse_if()
        
        # While loop
        elif token.type == TokenType.JABBTAK:
            return self.parse_while()
        
        # Return statement
        elif token.type == TokenType.RETURN:
            return self.parse_return()
        
        # Assignment or input
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_assignment_or_input()
        
        # Skip newlines and empty statements
        elif token.type in [TokenType.NEWLINE, TokenType.EOF, TokenType.KHATAM, TokenType.VARNA]:
            self.advance()
            return None
        
        else:
            self.error(f"Unexpected token: {token.type.name}")
    
    def parse_likho(self) -> Dict:
        """Parse likho (print) statement: likho "text" or likho var"""
        self.expect(TokenType.LIKHO)
        
        args = []
        
        # Parse all arguments until end of line
        while self.current_token().type not in [TokenType.NEWLINE, TokenType.EOF, TokenType.KHATAM, TokenType.VARNA]:
            arg = self.parse_expression()
            args.append(arg)
            
            # Check if there are more arguments
            if self.current_token().type not in [TokenType.STRING, TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.COLOR_TEXT, TokenType.COLOR_BG]:
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
        
        # Parse then body
        then_body = []
        while self.current_token().type not in [TokenType.VARNA, TokenType.KHATAM, TokenType.EOF]:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        
        # Parse else body if exists
        else_body = []
        if self.current_token().type == TokenType.VARNA:
            self.advance()
            self.skip_newlines()
            
            while self.current_token().type not in [TokenType.KHATAM, TokenType.EOF]:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
        
        # End with khatam
        if self.current_token().type == TokenType.KHATAM:
            self.advance()
        
        return {
            'type': 'if',
            'condition': condition,
            'then_body': then_body,
            'else_body': else_body
        }
    
    def parse_while(self) -> Dict:
        """Parse jabbtak (while) loop"""
        self.expect(TokenType.JABBTAK)
        
        condition = self.parse_expression()
        self.skip_newlines()
        
        # Parse loop body
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
        """Parse assignment or input: var = value or var = ?"""
        var_name = self.expect(TokenType.IDENTIFIER).value
        
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            
            # Check for input
            if self.current_token().type == TokenType.INPUT:
                self.advance()
                prompt = None
                
                # Optional prompt string
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
            self.error(f"Expected '=' or '?' after identifier '{var_name}'")
    
    def parse_expression(self) -> Any:
        """Parse expression with operator precedence"""
        return self.parse_comparison()
    
    def parse_comparison(self) -> Any:
        """Parse comparison: bara (>), chhota (<)"""
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.GREATER, TokenType.LESS, TokenType.EQUAL]:
            op_token = self.advance()
            op = {
                TokenType.GREATER: 'bara',
                TokenType.LESS: 'chhota',
                TokenType.EQUAL: 'barabar'
            }[op_token.type]
            
            right = self.parse_additive()
            
            left = {
                'type': 'binop',
                'op': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_additive(self) -> Any:
        """Parse addition/subtraction: jodo, ghatao"""
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.advance()
            op = 'jodo' if op_token.type == TokenType.PLUS else 'ghatao'
            right = self.parse_multiplicative()
            
            left = {
                'type': 'binop',
                'op': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_multiplicative(self) -> Any:
        """Parse multiplication/division: gunaa, bhago"""
        left = self.parse_primary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op_token = self.advance()
            op = 'gunaa' if op_token.type == TokenType.MULTIPLY else 'bhago'
            right = self.parse_primary()
            
            left = {
                'type': 'binop',
                'op': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_primary(self) -> Any:
        """Parse primary values: numbers, strings, variables, colors"""
        token = self.current_token()
        
        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        
        # String literal
        elif token.type == TokenType.STRING:
            self.advance()
            return token.value
        
        # Color code
        elif token.type == TokenType.COLOR_TEXT:
            self.advance()
            return {
                'type': 'color_text',
                'value': token.value
            }
        
        elif token.type == TokenType.COLOR_BG:
            self.advance()
            return {
                'type': 'color_bg',
                'value': token.value
            }
        
        # Variable reference
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            return {
                'type': 'variable',
                'name': name
            }
        
        # Parenthesized expression
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Unexpected token in expression: {token.type.name}")
