# cyberHunt - Roman Urdu Programming Language

A beginner-friendly programming language written entirely in Roman Urdu (Romanized Urdu script). Build console apps AND static websites!

## Features

- ✅ **Roman Urdu Syntax**: Write code in your native language
- ✅ **Simple & Intuitive**: Designed for beginners
- ✅ **Color Support**: Built-in color and background color support
- ✅ **Web Framework**: Build static HTML websites in Urdu
- ✅ **Python-based Compiler**: Fast and reliable execution
- ✅ **Easy to Learn**: No complex symbols, just clear Roman Urdu words

## What's New? 🚀

### Web Framework (Static Site Generator)
Now you can build websites completely in Roman Urdu!

```roman urdu
website = website_banao("Mera Blog")

home = page_banao(website, "index", "Home")
home.add_heading("Khush Amdeed!")
home.add_paragraph("Ye mera pehla website hai")
home.add_button("Learn More", onclick="alert('Hi!')")

about = page_banao(website, "about", "About Me")
about.add_heading("About Me")
about.add_paragraph("Main Riaz hoon")
about.add_link("Back to Home", "index.html")

generate_html(website)
```

Output: Beautiful HTML files in `website_output/` folder!

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

### Loops

```roman urdu
counter = 1
jabbtak counter chhota 10
  likho counter
  counter = counter jodo 1
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

## Web Framework - Building Websites

### Web Elements Available

```roman urdu
page.add_heading("Title")
page.add_paragraph("Some text")
page.add_button("Click Me", "action")
page.add_link("Link Text", "url.html")
page.add_image("image.jpg", "Alt Text")
page.add_list(["Item 1", "Item 2", "Item 3"])
```

### Complete Website Example

```roman urdu
website = website_banao("MyAwesomeSite")

home = page_banao(website, "index", "Home")
home.add_heading("Mera Website")
home.add_paragraph("Ye mera pehla website hai")
home.add_link("About", "about.html")

about = page_banao(website, "about", "About")
about.add_heading("About Me")
about.add_paragraph("Main Riaz hoon")

generate_html(website)
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

### With Loops

```roman urdu
shuro
  counter = 1
  jabbtak counter chhota 6
    likho "#3 Count: " counter
    counter = counter jodo 1
  khatam
khatam
```

## Installation

```bash
git clone https://github.com/riaz4764/cyberHunt.git
cd cyberHunt
python compiler.py your_file.ur
```

## Usage

### Console Programs

Create a file with `.ur` extension:

```bash
python compiler.py hello.ur
```

### Websites

Create a website builder file:

```bash
python web_framework.py
# Or import in your program
```

## Project Structure

```
cyberHunt/
├── README.md
├── LANGUAGE_SPEC.md
├── LICENSE
├── compiler.py
├── lexer.py
├── parser.py
├── interpreter.py
├── web_framework.py          # NEW!
├── .gitignore
├── examples/
│   ├── hello_world.ur
│   ├── input_output.ur
│   ├── conditions.ur
│   ├── math.ur
│   ├── colors.ur
│   └── loops.ur
└── tests/
    └── test_compiler.py
```

## Quick Start

### 1. Console Program
```bash
python compiler.py examples/hello_world.ur
```

### 2. Website
```python
from web_framework import *

website = website_banao("MyBlog")
page = page_banao(website, "index", "Home")
page.add_heading("Khush Amdeed!")
page.add_paragraph("Welcome to my site")
generate_html(website)
```

## Documentation

- **LANGUAGE_SPEC.md** - Complete language specification
- **examples/** - Sample programs
- **LICENSE** - MIT License

## Roadmap 🗺️

- ✅ Console Programs
- ✅ Web Framework (Static Sites)
- 🔄 Functions & Advanced Features
- 🔄 Database Support
- 🔄 Dynamic Web Apps
- 🔄 Mobile Apps

## Author

**Riaz Ali** (@riaz4764)

## License

MIT License - Free to use and modify

## Contributing

Contributions welcome! Fork the repo and submit pull requests.

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Contact: riaz.ai.studio@gmail.com

---

**Made with ❤️ for Urdu-speaking programmers**

**Urdu mein code likho. Apni language main soch. Duniya ko apne ideas de!**
