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

def html(path=None):
  return require('/'.join((settings.HTML_PATH, path)))

def js(path=None):
  return require('/'.join((settings.JS_PATH, path)))

def css(path=None):
  return require('/'.join((settings.CSS_PATH, path)))

def font(path=None):
  return require('/'.join((settings.FONT_PATH, path)))

def jade(path=None):
  return require('/'.join((settings.JADE_PATH, path)))

def less(path=None):
  return require('/'.join((settings.LESS_PATH, path)))

def cache(path=None):
  return require('/'.join((settings.CACHE_PATH, path)))
