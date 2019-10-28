#!/usr/bin/python2
import bencode, hashlib, base64, urllib
torrent = open('ubuntu-12.04.2-server-amd64.iso.torrent', 'rb').read()
metadata = bencode.bdecode(torrent)
hashcontents = bencode.bencode(metadata['info'])
digest = hashlib.sha1(hashcontents).digest()
b32hash = base64.b32encode(digest)
params = {'xt': 'urn:btih:%s' % b32hash,
      'dn': metadata['info']['name'],
      'tr': metadata['announce'],
      'xl': metadata['info']['length']}
paramstr = urllib.urlencode(params)
magneturi = 'magnet:?%s' % paramstr
print magneturi
