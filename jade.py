# coding: utf-8

import os, re, tools, paths

COMMAND = 'jade -P %s -o %s'

def _inline_json(json):
  def repl(match):
    return match.group().replace('\n', '\\x0a')
  json = re.sub(r'\'(|([^\'\\]+|\\[^\']|\\\')*)\'|"(|([^"\\]+|\\[^"]|\\")*)"',
      repl, json)
  json = json.replace('\n', ' ').replace('"', '\\"')
  return json

def _build_update(updated):
  pre_size = len(paths.jade()) + 1
  html_path = paths.html()
  if '' == html_path:
    html_path = '.'
  for path in updated:
    ext_start = path.rfind('.')
    ext = path[ext_start:]
    if '.json' == ext:
      path = path[:ext_start] + '.jade'
    dst_path = paths.html(path[:pre_size])
    json_path = path[:ext_start] + '.json'
    if not os.path.exists(path) and os.path.exists(dst_path):
      os.remove(dst_path)
      print '%s removed' % dst_path
    else:
      suf = html_path
      if os.path.exists(json_path):
        json = open(json_path).read()
        suf += ' -O "%s"' % _inline_json(json)
      code = os.system(COMMAND % (path, suf))
      if 0 != code:
        raise Exception('Error %d while building jade file %s' % (code, path))

def build(*src):
  if 1 > len(src):
    src = [paths.jade('*.jade'), paths.jade('*.json')]
  tools.watch(src, _build_update, paths.cache('jade_build'))

def rebuild(*src):
  cache = paths.cache('jade_build')
  if os.path.exists(cache):
    os.remove(cache)
  build(*src)
