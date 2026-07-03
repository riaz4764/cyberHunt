"""
cyberHunt Language Specification
Roman Urdu Programming Language
"""

# LANGUAGE OVERVIEW
cyberHunt is a Roman Urdu programming language designed for beginners.
It uses simple Roman Urdu words instead of complex English keywords.

# BASIC SYNTAX

## Program Structure
shuro
  // code here
khatam

## Keywords

| Roman Urdu | English | Purpose |
|-----------|---------|---------|
| shuro | start | Begin program |
| khatam | end | End program/block |
| agar | if | Conditional statement |
| varna | else | Else clause |
| jabbtak | while | Loop statement |
| likho | print | Output |
| ? | input | Input |
| func | function | Function definition |
| return | return | Return value |

## Variables

Assignment:
  naam = "Ahmed"
  umar = 25
  price = 100.50

## Data Types

- Strings: "text" or 'text'
- Numbers: 10, 20, 3.14
- Booleans: True/False (from conditions)

## Operators

### Arithmetic
- jodo : Addition (+)
- ghatao : Subtraction (-)
- gunaa : Multiplication (*)
- bhago : Division (/)

### Comparison
- bara : Greater than (>)
- chhota : Less than (<)
- barabar : Equal to (==)

### Assignment
- = : Assign value

## Color System

### Text Colors (Single #)
#0 : Default
#1 : Red
#2 : Green
#3 : Blue
#4 : Yellow
#5 : Purple
#6 : Cyan
#7 : White

### Background Colors (Double ##)
##0 : Default
##1 : Red background
##2 : Green background
##3 : Blue background
##4 : Yellow background
##5 : Purple background
##6 : Cyan background
##7 : White background

### Combined Format
"##background;#textcolor Text"
Example: "##2;#3 Green Background with Blue Text"

## Conditional Statements

agar condition
  // true block
varna
  // false block
khatam

## Loops

jabbtak condition
  // loop body
khatam

## Input/Output

Print:
  likho "message"
  likho "#2 green message"
  likho "##3 text with blue background"

Input:
  naam = ?
  naam = ? "Prompt message here?"

## Comments

// This is a comment

## Examples

### Hello World
shuro
  likho "#2 Hello, World!"
khatam

### Simple Math
shuro
  a = 5
  b = 10
  sum = a jodo b
  likho "Result: " sum
khatam

### User Input
shuro
  likho "Your name: "
  naam = ?
  likho "#3 Shukriya " naam
khatam

### Conditions
shuro
  age = 20
  agar age bara 18
    likho "#2 Adult"
  varna
    likho "#1 Minor"
  khatam
khatam

## Execution

Command:
  python compiler.py program.ur

Output:
  Lexer tokenizes the code
  Parser builds AST
  Interpreter executes AST

## Error Handling

- SyntaxError: Invalid syntax
- NameError: Undefined variable
- ValueError: Invalid value
- ZeroDivisionError: Division by zero

## Best Practices

1. Use meaningful variable names
2. Add comments for clarity
3. Use proper indentation
4. Test with simple examples first
5. Use colors for better UI

---

Version: 1.0
Author: Riaz Ali (@riaz4764)
License: MIT
