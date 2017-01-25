# The index file is another XML file, living per convention
# in OEBPS/content.opf

templates = {
    'index_tpl': '''<package version="2.0"
xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>%(title)s</dc:title>
<dc:language>en</dc:language>
<dc:subject>%(subject)s</dc:subject>
<dc:description>%(description)s</dc:description>
<meta name="cover" content="cover-image" />
</metadata>
<manifest>
  <item id="cover" href="cover.html" media-type="application/xhtml+xml"/>
  <item id="cover-image" href="%(front_cover)s" media-type="%(front_cover_type)s"/>
  <item id="css" href="stylesheet.css" media-type="text/css"/>
    %(manifest)s
</manifest>
<spine toc="ncx">
    <itemref idref="cover" linear="no"/>
    %(spine)s
</spine>
<guide>
    <reference href="cover.html" type="cover" title="Cover"/>
</guide>
</package>''',
    'toc_tpl': '''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
         "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="dtb:depth" content="1"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle>
<text>%(title)s</text>
</docTitle>
<navMap>
<navPoint id="navpoint-1" playOrder="1"> <navLabel> <text>Cover</text> </navLabel> <content src="cover.html"/> </navPoint>
%(toc)s
</navMap>
</ncx>''',
    'cover_tpl': '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Cover</title>
<style type="text/css"> img { max-width: 100%%; } </style>
</head>
<body>
<h1>%(title)s</h1>
<div id="cover-image">
<img src="%(front_cover)s" alt="Cover image"/>
</div>
</body>
</html>''',
    'stylesheet_tpl': '''
p, body {
    font-weight: normal;
    font-style: normal;
    font-variant: normal;
    font-size: 1em;
    line-height: 2.0;
    text-align: left;
    margin: 0 0 1em 0;
    orphans: 2;
    widows: 2;
}
h2 {
    margin: 5px;
}
'''

}
