# coding: utf-8

'''
Tools to build Jade templates.
'''

import os, re, tools

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
  Compiles a single Jade template. If there is a JSON file with same name in the
  same directory, will be used as Javascript options object.

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
  ext = jade_path[dot:]
  if '.json' == ext:
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
    cmd = [CMD, '-P', '-p', arg_path]

    # if not in JS mode, pass JSON file as Javascript options object
    if not js_mode and os.path.exists(json_path):
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
