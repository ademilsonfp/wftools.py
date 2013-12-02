# coding: utf-8

'''
Tools to build LESS styles.
'''

import os, tools

'''
LESS command or path.
'''
CMD = 'lessc'

def build(src_path, path):
  '''
  Builds a single LESS file to specified path.
  '''
  if not os.path.exists(src_path):
    if os.path.exists(path):
      os.unlink(path)
      print '%s removed' % tools.subpath(path)
    return

  cmd = [CMD, '--verbose', '--strict-imports', src_path, path]
  code = os.system(' '.join(cmd))
  if 0 != code:
    raise Exception('Error %d while building LESS file %s' % (code, src_path))
