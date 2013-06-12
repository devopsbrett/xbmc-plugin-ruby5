'''
    Ruby5 XBMC Addon
    -------------------

    Listen to podcasts from http://ruby5.envylabs.com in XBMC.

    :copyright: (c) 2013 by Brett Mack
    :license: GPLv3, see LICENSE.txt for more details.
'''

from xbmcswift2 import Plugin
from urllib2 import urlopen
from xml.dom import minidom

plugin = Plugin()

def get_tag(item, tag_name):
    return item.getElementsByTagName(tag_name)[0]

def get_tag_value(item, tag_name):
    return get_tag(item, tag_name).childNodes[0].toxml()

def get_tag_attribute(tag, attr_name):
    return tag.getAttribute(attr_name)


def get_feed():
	'''Gets the rss feed from feedburner'''
	rss = urlopen('http://feeds.feedburner.com/Ruby5?format=xml')
	return rss

def get_episodes():
	'''Grabs each of the episodes listed in the rss feed'''
	feed = get_feed()

	xmldom = minidom.parse(feed)
	channel_node = xmldom.childNodes[2]

	episodes = []

	_items = channel_node.getElementsByTagName('item')

	for i in range(0, _items.length):
		episodes.append({
            'title': get_tag_value(_items[i], 'title') + ' (' + get_tag_value(_items[i], 'itunes:duration') + ')',
            'description': get_tag_value(_items[i], 'description'),
            'url': get_tag_attribute(get_tag(_items[i], 'enclosure'), 'url')
        })

    	return episodes


@plugin.route('/')
def index():
    items = [{
        'label': episode['title'],
        'path': episode['url'],
        'info': {
        	'plot': episode['description']
        },
        'is_playable': True,
    } for episode in get_episodes()]

    return items


if __name__ == '__main__':
    plugin.run()
