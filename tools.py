# coding: utf-8

import os, sys, pickle, time, urllib2, settings
from glob import glob

def download(url, path):
  print 'downloading %s...' % url

  urlopener = urllib2.build_opener()
  urlopener.addheaders = [('User-agent', 'frontend tools')]

  response = urlopener.open(url)
  size = int(response.headers.get('content-length', 0))
  bufsize = getattr(settings, 'DOWNLOAD_BUFFER', 1024)
  loaded = 0
  try:
    with open(path, 'w') as f:
      chunk = response.read(bufsize)
      while '' != chunk:
        f.write(chunk)
        if 0 < size:
          loaded += len(chunk)
          bs = 30
          pl = bs * loaded / size
          pr = bs * (size - loaded) / size
          per = str(100 * loaded / size)
          ls = bs + 4 + len(per)
          pout = ('\r' * ls, ':' * pl, ' ' * pr, per)
          sys.stdout.write('%s[%s%s] %s%%' % pout)
        chunk = response.read(bufsize)
      if 0 < size:
        sys.stdout.write(('\r' * 32) + '\n')
  except KeyboardInterrupt as e:
    os.remove(path)
    if 0 < size:
      print
    print 'download removed %s' % path
    raise e
  print 'download saved %s' % path

def watch(src, fn, cache_path):
  if not os.path.exists(cache_path):
    cache = {}
  else:
    with open(cache_path, 'r') as stored:
      cache = pickle.load(stored)

  fpaths = []
  for pattern in src:
    fpaths += glob(pattern)

  updated = []
  removed = fpaths[:]
  for path in fpaths:
    removed.remove(path)
    lmtime = cache.get(path, None)
    mtime = time.ctime(os.path.getmtime(path))
    if None is lmtime or lmtime < mtime:
      cache[path] = mtime
      updated.append(path)

  for path in removed:
    updated.append(path)
    del cache[path]

  if 0 < len(updated):
    fn(updated)
    with open(cache_path, 'w') as store:
      pickle.dump(cache, store)
