import yql
y = yql.Public()
query = 'SELECT * FROM meme.popular WHERE locale=\'pt\'';

result = y.execute(query)
result.rows

for row in result.rows:
    print 'category: %s' % row.get('category')
    print 'comment: %s' % row.get('comment')
    print 'via_guid: %s' % row.get('via_guid')
    print 'url: %s' % row.get('url')
    print 'timestamp: %s' % row.get('timestamp')
    print 'pubid: %s' % row.get('pubid')
    print 'repost_count: %s' % row.get('repost_count')
    print 'origin_guid: %s' % row.get('origin_guid')
    print 'content: %s' % row.get('content')
    print 'caption: %s' % row.get('caption')
    print 'origin_pubid: %s' % row.get('origin_pubid')
    print 'guid: %s' % row.get('guid')
    print 'type: %s' % row.get('type')
    print '------------------------------'