# coding: utf-8

import os, tools, paths

COMMAND = 'jade -P %s -o %s'

def _build_update(updated):
  pre_size = len(paths.jade()) + 1
  html_path = paths.html()
  if '' == html_path:
    html_path = '.'
  for path in updated:
    dst_path = paths.html(path[:pre_size])
    if not os.path.exists(path) and os.path.exists(dst_path):
      os.remove(dst_path)
      print '%s removed' % dst_path
    else:
      os.system(COMMAND % (path, html_path))

def build(*src):
  if 1 > len(src):
    src = [paths.jade('*.jade')]
  tools.watch(src, _build_update, paths.cache('jade_build'))

def rebuild(*src):
  cache = paths.cache('jade_build')
  if os.path.exists(cache):
    os.remove(cache)
  build(*src)
