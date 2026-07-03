"""
cyberHunt Web Framework - Static Site Generator
Convert Roman Urdu code to HTML websites
"""

from typing import Dict, List, Optional
import os
import json

class WebElement:
    """Base class for HTML elements"""
    def __init__(self, tag: str, content: str = "", attributes: Dict = None):
        self.tag = tag
        self.content = content
        self.attributes = attributes or {}
        self.children = []
    
    def add_child(self, element):
        """Add child element"""
        self.children.append(element)
        return self
    
    def add_attribute(self, key: str, value: str):
        """Add HTML attribute"""
        self.attributes[key] = value
        return self
    
    def to_html(self) -> str:
        """Convert to HTML string"""
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        attrs = f" {attrs}" if attrs else ""
        
        if self.children:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{attrs}>\n{children_html}\n</{self.tag}>"
        elif self.content:
            return f"<{self.tag}{attrs}>{self.content}</{self.tag}>"
        else:
            return f"<{self.tag}{attrs}>"

class WebPage:
    """Represents a single web page"""
    def __init__(self, name: str, title: str = ""):
        self.name = name
        self.title = title
        self.head = WebElement("head")
        self.body = WebElement("body")
        self.styles = {}
        self.meta_tags = []
    
    def add_style(self, css_code: str):
        """Add CSS to page"""
        style_tag = WebElement("style", css_code)
        self.head.add_child(style_tag)
        return self
    
    def add_meta(self, name: str, content: str):
        """Add meta tag"""
        meta = WebElement("meta")
        meta.add_attribute("name", name)
        meta.add_attribute("content", content)
        self.head.add_child(meta)
        return self
    
    def add_heading(self, text: str, level: int = 1, style: Dict = None):
        """Add heading"""
        heading = WebElement(f"h{level}", text)
        if style:
            heading.add_attribute("style", self._dict_to_style(style))
        self.body.add_child(heading)
        return self
    
    def add_paragraph(self, text: str, style: Dict = None):
        """Add paragraph"""
        para = WebElement("p", text)
        if style:
            para.add_attribute("style", self._dict_to_style(style))
        self.body.add_child(para)
        return self
    
    def add_button(self, text: str, onclick: str = "", style: Dict = None):
        """Add button"""
        button = WebElement("button", text)
        if onclick:
            button.add_attribute("onclick", onclick)
        if style:
            button.add_attribute("style", self._dict_to_style(style))
        self.body.add_child(button)
        return self
    
    def add_link(self, text: str, href: str, style: Dict = None):
        """Add link"""
        link = WebElement("a", text)
        link.add_attribute("href", href)
        if style:
            link.add_attribute("style", self._dict_to_style(style))
        self.body.add_child(link)
        return self
    
    def add_image(self, src: str, alt: str = "", style: Dict = None):
        """Add image"""
        img = WebElement("img")
        img.add_attribute("src", src)
        img.add_attribute("alt", alt)
        if style:
            img.add_attribute("style", self._dict_to_style(style))
        self.body.add_child(img)
        return self
    
    def add_list(self, items: List[str], ordered: bool = False):
        """Add list"""
        list_tag = "ol" if ordered else "ul"
        list_elem = WebElement(list_tag)
        for item in items:
            li = WebElement("li", item)
            list_elem.add_child(li)
        self.body.add_child(list_elem)
        return self
    
    def add_html(self, html_content: str):
        """Add raw HTML"""
        # For custom HTML
        self.body.children.append(html_content)
        return self
    
    def _dict_to_style(self, style_dict: Dict) -> str:
        """Convert style dictionary to CSS string"""
        return "; ".join(f"{k}: {v}" for k, v in style_dict.items())
    
    def to_html(self) -> str:
        """Generate complete HTML document"""
        # Add title to head
        if self.title:
            title_tag = WebElement("title", self.title)
            self.head.add_child(title_tag)
        
        # Add meta charset
        meta_charset = WebElement("meta")
        meta_charset.add_attribute("charset", "UTF-8")
        self.head.add_child(meta_charset)
        
        # Create html element
        html = WebElement("html")
        html.add_child(self.head)
        html.add_child(self.body)
        
        return f"<!DOCTYPE html>\n{html.to_html()}"

class WebsiteGenerator:
    """Generate complete website from pages"""
    def __init__(self, name: str, output_dir: str = "website_output"):
        self.name = name
        self.output_dir = output_dir
        self.pages = {}
        self.global_style = ""
    
    def create_page(self, page_name: str, title: str = "") -> WebPage:
        """Create a new page"""
        page = WebPage(page_name, title or page_name.capitalize())
        self.pages[page_name] = page
        return page
    
    def add_global_style(self, css: str):
        """Add global CSS for all pages"""
        self.global_style = css
        return self
    
    def generate(self):
        """Generate all HTML files"""
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Generate each page
        for page_name, page in self.pages.items():
            # Add global style if exists
            if self.global_style:
                page.add_style(self.global_style)
            
            # Generate HTML
            html_content = page.to_html()
            
            # Write to file
            filename = f"{self.output_dir}/{page_name}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"[+] Created: {filename}")
        
        # Create index.html if index page exists
        if 'index' in self.pages:
            with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(self.pages['index'].to_html())
            print(f"[+] Website ready at: {self.output_dir}/index.html")
    
    def create_sitemap(self):
        """Create sitemap"""
        sitemap = {
            "name": self.name,
            "pages": list(self.pages.keys()),
            "generated": True
        }
        
        with open(f"{self.output_dir}/sitemap.json", 'w') as f:
            json.dump(sitemap, f, indent=2)
        
        print(f"[+] Sitemap created")

# Global website instance
current_website = None

def website_banao(name: str, output_dir: str = "website_output") -> WebsiteGenerator:
    """Create a new website (website banao)"""
    global current_website
    current_website = WebsiteGenerator(name, output_dir)
    print(f"[*] Website '{name}' created")
    return current_website

def page_banao(website: WebsiteGenerator, page_name: str, title: str = "") -> WebPage:
    """Create a new page (page banao)"""
    page = website.create_page(page_name, title)
    print(f"[*] Page '{page_name}' created")
    return page

def generate_html(website: WebsiteGenerator):
    """Generate HTML files (generate_html)"""
    print(f"[*] Generating website...")
    website.generate()
    print(f"[+] Website generation complete!")
