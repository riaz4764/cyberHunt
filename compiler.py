#!/usr/bin/env python3
"""
cyberHunt Compiler - Main entry point
Roman Urdu Programming Language Compiler
"""

import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <filename.ur>")
        print("\nExample:")
        print("  python compiler.py hello.ur")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    
    # Read the source code
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    try:
        # Lexical analysis
        print(f"[*] Lexing {filename}...", file=sys.stderr)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Parsing
        print(f"[*] Parsing...", file=sys.stderr)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpretation
        print(f"[*] Executing...", file=sys.stderr)
        interpreter = Interpreter()
        interpreter.execute(ast)
        
        print(f"[+] Done!", file=sys.stderr)
    
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NameError as e:
        print(f"Name Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Value Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
