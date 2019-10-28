#!/usr/bin/python2
import libtorrent as bt
info = bt.torrent_info('test.torrent')
print "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
