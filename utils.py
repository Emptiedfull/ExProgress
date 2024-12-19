from jinja2 import Template

class htmx_templates():
    def __init__(self,path:str="templates"):
        self.path:str = path
    
    def render(self,filename:str,mappings:object):
        template = Template(open(f'{self.path}/{filename}').read())
        return template.render(mappings)
        

