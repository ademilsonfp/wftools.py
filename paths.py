# coding: utf-8

import os, settings

def require(path=None):
  if None is path or 1 > len(path):
    return ''

  dname = os.path.dirname(path)
  if not os.path.exists(dname):
    os.makedirs(dname)

  if '/' == path[-1]:
    return path[:-1]
  return path

def requirec(pre, suf=None):
  if None is suf:
    return pre

  sep = '' if '/' == pre[-1] or None is pre or 1 > len(pre) else '/'
  return require(sep.join((pre, suf)))

def html(path=None):
  return requirec(getattr(settings, 'HTML_PATH', ''), path)

def js(path=None):
  return requirec(getattr(settings, 'JS_PATH', 'js'), path)

def css(path=None):
  return requirec(getattr(settings, 'CSS_PATH', 'css'), path)

def font(path=None):
  return requirec(getattr(settings, 'FONT_PATH', 'font'), path)

def jade(path=None):
  return requirec(getattr(settings, 'JADE_PATH', 'jade'), path)

def less(path=None):
  return requirec(getattr(settings, 'LESS_PATH', 'less'), path)

def cache(path=None):
  return requirec(getattr(settings, 'CACHE_PATH', 'cache'), path)
