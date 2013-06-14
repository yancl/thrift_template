import os
from paste.script import templates

class ThriftServiceTemplate(templates.Template):
    _template_dir = 'service'
    summary = "A Thrift Service project"


class ThriftServerTemplate(templates.Template):
    _template_dir = 'server'
    summary = "A Python Thrift Server project"

    def post(self, command, output_dir, vars):
        for filename in ['codegen']:
            os.chmod(os.path.join(output_dir, filename), 0755)
