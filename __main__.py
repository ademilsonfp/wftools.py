# coding: utf-8

import sys, traceback, jquery, bootstrap

tools = {
  'jquery': jquery,
  'bootstrap': bootstrap
}

if 3 > len(sys.argv):
  print 'invalid number of arguments'
else:
  tool, fn = sys.argv[1:3]
  if tool not in tools:
    print 'invalid tool %s' % tool
  else:
    try:
      def error(*a):
        print 'function %s not found on tool %s' % (fn, tool)
      getattr(tools[tool], fn, error)(*sys.argv[3:])
    except:
      title = 'ERROR: function %s on tool %s' % (fn, tool)
      print title
      print '-' * len(title)
      traceback.print_exc()
