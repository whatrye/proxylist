#!/usr/bin/python2
#need python-libtorrent (apt install python-libtorrent)
import libtorrent as bt
info = bt.torrent_info('test.torrent')
print "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
