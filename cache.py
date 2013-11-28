# coding: utf-8

import os, tools

'''
Path for cache files.
'''
PATH = 'cache'

def path(path='', create_dirs=True):
  '''
  Returns full path prepended with directory of cache files and creates parent
  directories when ``create_dirs`` flag is marked.
  '''
  return tools.path(os.path.join(PATH, path), create_dirs)
