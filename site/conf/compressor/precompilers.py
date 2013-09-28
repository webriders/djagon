import os
from compressor.filters.base import CompilerFilter
from compressor.filters.css_default import CssAbsoluteFilter
from django.conf import settings


class ScssFilter(CompilerFilter):
    def __init__(self, content, attrs, **kwargs):
        command = 'sass --scss --compass {infile} {outfile} --load-path=%s' % \
                  os.path.join(settings.SITE_ROOT, "source/common/static/common/css/")
        super(ScssFilter, self).__init__(content, command=command, **kwargs)

    def input(self, **kwargs):
        content = super(ScssFilter, self).input(**kwargs)
        return CssAbsoluteFilter(content).input(**kwargs)
