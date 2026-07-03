# cyberHunt - Roman Urdu Programming Language

A beginner-friendly programming language written entirely in Roman Urdu (Romanized Urdu script). Built with Python compiler for easy interpretation and execution.

## Features

- **Roman Urdu Syntax**: Write code in your native language
- **Simple & Intuitive**: Designed for beginners
- **Color Support**: Built-in color and background color support for text output
- **Python-based Compiler**: Fast and reliable execution
- **Easy to Learn**: No complex symbols, just clear Roman Urdu words

## Language Syntax

### Basic Structure

```roman urdu
shuro
  // Your code here
khatam
```

### Variables & Assignment

```roman urdu
naam = "Ahmed"
umar = 25
```

### Output (Print)

```roman urdu
likho "Hello World"
likho "#2 Green Text"
likho "##3 Blue Background"
likho "##2;#3 Green Background with Blue Text"
```

### Input

```roman urdu
naam = ?
naam = ? "Apka naam kya hai?"
```

### Conditions

```roman urdu
agar umar bara 18
  likho "Adult"
varna
  likho "Minor"
khatam
```

### Operators

- `=` : Assignment
- `bara` : Greater than (>)
- `chhota` : Less than (<)
- `barabar` : Equal to (==)
- `jodo` : Addition (+)
- `ghatao` : Subtraction (-)
- `gunaa` : Multiplication (*)
- `bhago` : Division (/)

### Color Codes

#### Text Colors
- `#1` : Red
- `#2` : Green
- `#3` : Blue
- `#4` : Yellow
- `#5` : Purple
- `#6` : Cyan
- `#7` : White
- `#0` : Default

#### Background Colors
- `##1` : Red background
- `##2` : Green background
- `##3` : Blue background
- `##4` : Yellow background
- `##5` : Purple background
- `##6` : Cyan background
- `##7` : White background
- `##0` : Default background

#### Combined Usage
```roman urdu
likho "#2 Green Text"
likho "##3 Blue Background"
likho "##2;#3 Green Background with Blue Text"
likho "#1;##7 Red Text on White Background"
```

## Example Programs

### Simple Program

```roman urdu
shuro
  likho "#2 Khush Amdeed cyberHunt mein!"
  naam = ? "Apka naam batao: "
  likho "Salam " naam
khatam
```

### With Conditions

```roman urdu
shuro
  likho "Apki umar batao: "
  umar = ?
  agar umar bara 18
    likho "#2 Aap adult hain"
  varna
    likho "#1 Aap bacha hain"
  khatam
khatam
```

### With Math

```roman urdu
shuro
  num1 = 10
  num2 = 5
  sum = num1 jodo num2
  likho "Total: " sum
khatam
```

## Installation

```bash
git clone https://github.com/riaz4764/cyberHunt.git
cd cyberHunt
python compiler.py your_file.ur
```

## Usage

Create a file with `.ur` extension:

```bash
python compiler.py hello.ur
```

## Project Structure

```
cyberHunt/
├── README.md
├── compiler.py
├── lexer.py
├── parser.py
├── interpreter.py
├── examples/
│   ├── hello_world.ur
│   ├── input_output.ur
│   └── conditions.ur
└── tests/
    └── test_compiler.py
```

## Author

**Riaz** (@riaz4764)

## License

MIT License - Free to use and modify

## Contributing

Contributions welcome! Fork the repo and submit pull requests.

---

**Made with ❤️ for Urdu-speaking programmers**
