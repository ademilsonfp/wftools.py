# coding: utf-8

import urllib2

def download(url, path):
  print 'downloading %s...' % url

  urlopener = urllib2.build_opener()
  urlopener.addheaders = [('User-agent', 'frontend tools')]

  response = urlopener.open(url)
  content = response.read()
  with open(path, 'w') as f:
    f.write(content)

  print 'download saved %s' % path
