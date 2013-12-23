# coding: utf-8

'''
Tools to build Jade templates.
'''

import os, re, tools, itertools, glob

'''
Jade command or path.
'''
CMD = 'jade'

'''
Path of source templates.
'''
TEMPLATE_PATH = 'jade'

'''
Path for built HTML documents.
'''
BUILD_PATH = ''

'''
Path for built Javascript files.
'''
JS_BUILD_PATH = 'js/template'

def path(path='', create_dirs=True):
  '''
  Returns full path prepended with directory of Jade templates and creates
  parent directories when ``create_dirs`` flag is marked.
  '''
  return tools.path(os.path.join(TEMPLATE_PATH, path), create_dirs)

def build_path(path='', create_dirs=True):
  '''
  Returns full path prepended with directory of built HTML templates and creates
  parent directories when ``create_dirs`` flag is marked.
  '''
  return tools.path(os.path.join(BUILD_PATH, path), create_dirs)

def js_build_path(path='', create_dirs=True):
  '''
  Returns full path prepended with directory of built Javascript templates and
  creates parent directories when ``create_dirs`` flag is marked.
  '''
  return tools.path(os.path.join(JS_BUILD_PATH, path), create_dirs)

def json_cmdarg(json):
  '''
  Flattens and escapes a multiline JSON document as command line argument.
  '''
  str_regex = r'\'(|([^\'\\]+|\\[^\']|\\\')*)\'|"(|([^"\\]+|\\[^"]|\\")*)"'
  def str_repl(match):
    return match.group().replace('\n', '\\x0a')
  json = re.sub(str_regex, str_repl, json)
  json = '"%s"' % json.replace('\n', ' ').replace('"', '\\"').strip()
  return json

def build(tpl_path, js_mode=False, debug=True):
  '''
  Compiles a single Jade template. If there is a JSON file with same name in
  the same directory, will be used as Javascript options object.

  You can compile the template passing the JSON path, in this case the function
  will look for *.jade* file.
  '''
  jade_path = json_path = path(tpl_path)
  tpl_path = tpl_path[:tpl_path.rfind('.')]
  final_path = None
  if js_mode:
    final_path = js_build_path(tpl_path + '.js')
  else:
    final_path = build_path(tpl_path + '.html')

  # check if template path is a JSON file
  dot = jade_path.rfind('.')
  if jade_path.endswith('.json'):
    jade_path = jade_path[:dot] + '.jade'
  else:
    json_path = jade_path[:dot] + '.json'

  # check if template does not exists
  if not os.path.exists(jade_path):
    # remove built file if exists
    if os.path.exists(final_path):
      os.remove(final_path)
      print '%s removed' % tools.subpath(final_path)

    # stop execution when template does not exist
    return
  else:
    # build command line
    arg_path = BUILD_PATH if not js_mode else JS_BUILD_PATH
    if 1 > len(arg_path):
      arg_path = '.'
    cmd = [CMD, '-P', '-o', arg_path]

    # add --client argument if in JS mode else pass existing JSON file as
    # Javascript options object
    if js_mode:
      cmd.append('-c')
    elif os.path.exists(json_path):
      json = open(json_path).read()
      cmd.append('-O', json_cmdarg(json))

    # if in JS mode, disable debug when flag is unmarked
    if js_mode and not debug:
      cmd.append('-D')

    # execute command
    cmd.append(tools.subpath(jade_path))
    code = os.system(' '.join(cmd))
    if 0 != code:
      raise Exception('Error %d while building jade file %s' % (code, path))

def build_all(patterns=None, js_mode=False, debug=True):
  '''
  Builds all specified templates, accepts glob patterns and does nothing if
  template does not exist.
  '''

  if None is patterns:
    patterns = ['*.jade']
  elif isinstance(patterns, str):
    patterns = [patterns]

  all = [glob.glob(path(pattern)) for pattern in patterns]
  all = itertools.chain(*all)
  lstrip = 1 + len(TEMPLATE_PATH)
  for src in all:
    src = tools.subpath(src)[lstrip:]
    if 0 < len(src):
      build(src, js_mode, debug)

def watch_build(watch=None, src=None, js_mode=False, debug=True):
  '''
  Watch paths inside jade directory for changes and builds specified templates.
  '''

  if None is watch:
    watch = ['*.jade', '*.json']
  elif isinstance(watch, str):
    watch = [watch]
  watch = [path(pattern) for pattern in watch]

  if None is src:
    src = ['*.jade']
  elif isinstance(src, str):
    src = [src]

  def wrap_build(updated):
    build_all(src, js_mode, debug)
  tools.watch(watch, wrap_build, 'jade')
