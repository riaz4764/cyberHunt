"""
cyberHunt Interpreter - Executes AST nodes
"""

from typing import Any, Dict, List
from lexer import Token, TokenType
import sys

class ColorCodes:
    """ANSI Color codes for terminal output"""
    
    TEXT_COLORS = {
        '0': '\033[0m',    # Default
        '1': '\033[91m',   # Red
        '2': '\033[92m',   # Green
        '3': '\033[94m',   # Blue
        '4': '\033[93m',   # Yellow
        '5': '\033[95m',   # Purple
        '6': '\033[96m',   # Cyan
        '7': '\033[97m',   # White
    }
    
    BG_COLORS = {
        '0': '\033[0m',    # Default
        '1': '\033[101m',  # Red BG
        '2': '\033[102m',  # Green BG
        '3': '\033[104m',  # Blue BG
        '4': '\033[103m',  # Yellow BG
        '5': '\033[105m',  # Purple BG
        '6': '\033[106m',  # Cyan BG
        '7': '\033[107m',  # White BG
    }

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.return_value = None
        self.is_returning = False
    
    def parse_color_code(self, text: str) -> tuple:
        """Parse color codes from string"""
        text_color = '7'  # Default white
        bg_color = '0'    # Default no background
        content = text
        
        # Check if string contains color codes
        if text.startswith('#'):
            # Format: "#color;##bgcolor text" or "##bgcolor text" or "#color text"
            parts = text.split(' ', 1)
            codes = parts[0]
            content = parts[1] if len(parts) > 1 else ''
            
            if ';' in codes:
                # Both text and background color
                color_parts = codes.split(';')
                text_part = color_parts[0].lstrip('#')
                bg_part = color_parts[1].lstrip('#')
                
                if text_part and text_part[0] != '#':
                    text_color = text_part
                if bg_part:
                    bg_color = bg_part
            else:
                # Either text or background color
                if codes.startswith('##'):
                    bg_color = codes[2:]
                else:
                    text_color = codes[1:]
        
        return text_color, bg_color, content
    
    def format_output(self, text: str) -> str:
        """Format text with color codes"""
        text_color, bg_color, content = self.parse_color_code(str(text))
        
        text_code = ColorCodes.TEXT_COLORS.get(text_color, ColorCodes.TEXT_COLORS['7'])
        bg_code = ColorCodes.BG_COLORS.get(bg_color, '')
        reset_code = '\033[0m'
        
        if bg_code:
            return f"{bg_code}{text_code}{content}{reset_code}"
        else:
            return f"{text_code}{content}{reset_code}"
    
    def get_variable(self, name: str) -> Any:
        if name not in self.variables:
            raise NameError(f"Variable '{name}' not defined")
        return self.variables[name]
    
    def set_variable(self, name: str, value: Any):
        self.variables[name] = value
    
    def execute_likho(self, args: List[Any]) -> None:
        """Print statement - likho"""
        output = ""
        for arg in args:
            if isinstance(arg, str):
                # Check for color codes in the string
                output += self.format_output(arg)
            else:
                output += str(arg)
        print(output)
    
    def execute_input(self, prompt: str = "") -> str:
        """Input statement - ?"""
        if prompt:
            print(self.format_output(prompt), end='')
        return input()
    
    def evaluate_expression(self, node: Any) -> Any:
        """Evaluate an expression node"""
        if isinstance(node, (int, float)):
            return node
        
        if isinstance(node, str):
            # Check if it's a variable reference
            if node in self.variables:
                return self.variables[node]
            return node
        
        if isinstance(node, dict):
            if node.get('type') == 'binop':
                left = self.evaluate_expression(node['left'])
                right = self.evaluate_expression(node['right'])
                op = node['op']
                
                if op == 'jodo':
                    return left + right
                elif op == 'ghatao':
                    return left - right
                elif op == 'gunaa':
                    return left * right
                elif op == 'bhago':
                    if right == 0:
                        raise ValueError("Division by zero")
                    return left / right
                elif op == 'bara':
                    return left > right
                elif op == 'chhota':
                    return left < right
                elif op == '==':
                    return left == right
            
            elif node.get('type') == 'variable':
                return self.get_variable(node['name'])
        
        return node
    
    def execute(self, ast: Dict) -> None:
        """Execute AST"""
        if ast['type'] == 'program':
            for statement in ast['statements']:
                if self.is_returning:
                    break
                self.execute_statement(statement)
    
    def execute_statement(self, stmt: Dict) -> None:
        """Execute a single statement"""
        if stmt['type'] == 'assignment':
            value = self.evaluate_expression(stmt['value'])
            self.set_variable(stmt['name'], value)
        
        elif stmt['type'] == 'likho':
            args = [self.evaluate_expression(arg) for arg in stmt['args']]
            self.execute_likho(args)
        
        elif stmt['type'] == 'input':
            prompt = stmt.get('prompt', '')
            if prompt:
                prompt = self.evaluate_expression(prompt)
            value = self.execute_input(str(prompt))
            self.set_variable(stmt['var'], value)
        
        elif stmt['type'] == 'if':
            condition = self.evaluate_expression(stmt['condition'])
            if condition:
                for s in stmt['then_body']:
                    if self.is_returning:
                        break
                    self.execute_statement(s)
            elif 'else_body' in stmt:
                for s in stmt['else_body']:
                    if self.is_returning:
                        break
                    self.execute_statement(s)
        
        elif stmt['type'] == 'while':
            while self.evaluate_expression(stmt['condition']):
                for s in stmt['body']:
                    if self.is_returning:
                        break
                    self.execute_statement(s)
                if self.is_returning:
                    break
        
        elif stmt['type'] == 'return':
            self.return_value = self.evaluate_expression(stmt['value'])
            self.is_returning = True
