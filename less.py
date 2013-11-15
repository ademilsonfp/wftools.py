# coding: utf-8

import os, tools, paths

COMMAND = 'lessc --verbose --strict-imports %s %s'

def _build(updated):
  pre_size = len(paths.less()) + 1
  for path in updated:
    dst_path = paths.css(path[pre_size:path.rfind('.')] + '.css')
    if not os.path.exists(path) and os.path.exists(dst_path):
      os.remove(dst_path)
      print '%s removed' % dst_path
    else:
      code = os.system(COMMAND % (path, dst_path))
      if 0 != code:
        raise Exception('Error %d while building less file %s' % (code, path))

def build(*src):
  if 1 > len(src):
    src = [paths.less('*.less')]
  tools.watch(src, _build, paths.cache('less_build'))

def rebuild(*src):
  cache = paths.cache('less_build')
  if os.path.exists(cache):
    os.remove(cache)
  build(*src)
