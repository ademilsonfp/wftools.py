# coding: utf-8

import sys, traceback, jquery, underscore, backbone, bootstrap, jade, less, \
    qunit

tools = {
  'jquery': jquery,
  'underscore': underscore,
  'backbone': backbone,
  'bootstrap': bootstrap,
  'jade': jade,
  'less': less,
  'qunit': qunit
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
      if '_' == fn[:1]:
        error()
      else:
        getattr(tools[tool], fn, error)(*sys.argv[3:])
    except:
      title = 'ERROR: function %s on tool %s' % (fn, tool)
      print title
      print '-' * len(title)
      traceback.print_exc()
