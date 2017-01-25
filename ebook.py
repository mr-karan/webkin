import mimetypes
import os.path
import time
import zipfile

html_files = ['blog.html']

if __name__ == '__main__':
    # TODO Add Image URL
    cover = ''
    cpath = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
    ctype = 'image/gif'
    if cover is not None:
        cpath = 'images/cover' + os.path.splitext(os.path.abspath(cover))[1]
        ctype = mimetypes.guess_type(os.path.basename(os.path.abspath(cover)))[0]

    epub = zipfile.ZipFile('test.epub', 'w')

    # Metadata about the book
    info = dict(title='Title',
                author='Author',
                rights='Copyright respective page authors',
                publisher='',
                ISBN='',
                subject='',
                description='',
                date=time.strftime('%Y-%m-%d'),
                front_cover=cpath,
                front_cover_type=ctype
                )

    # The first file must be named "mimetype"
    epub.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
    # We need an index file, that lists all other HTML files
    # This index file itself is referenced in the META_INF/container.xml file
    epub.writestr("META-INF/container.xml", '''<container version="1.0"
        xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
        <rootfiles>
            <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
        </rootfiles>
        </container>''')

    # The index file is another XML file, living per convention
    # in OEBPS/content.opf
    index_tpl = '''<package version="2.0"
        xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>%(title)s</dc:title>
        <dc:creator>%(author)s</dc:creator>
        <dc:language>en</dc:language>
        <dc:rights>%(rights)s</dc:rights>
        <dc:publisher>%(publisher)s</dc:publisher>
        <dc:subject>%(subject)s</dc:subject>
        <dc:description>%(description)s</dc:description>
        <dc:date>%(date)s</dc:date>
        <dc:identifier id="bookid">%(ISBN)s</dc:identifier>
        <meta name="cover" content="cover-image" />
        </metadata>
        <manifest>
          <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
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
        </package>'''

    toc_tpl = '''<?xml version='1.0' encoding='utf-8'?>
        <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
        <head>
        <meta name="dtb:uid" content="%(ISBN)s"/>
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
    </ncx>'''

    cover_tpl = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
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
        </html>'''

    stylesheet_tpl = '''
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

    manifest = ""
    spine = ""
    toc = ""

    epub.writestr('OEBPS/cover.html', cover_tpl % info)
    if cover is not None:
        epub.write(os.path.abspath(cover), 'OEBPS/images/cover' + os.path.splitext(cover)[1], zipfile.ZIP_DEFLATED)

    # Write each HTML file to the ebook, collect information for the index
    for i, html in enumerate(html_files):
        basename = os.path.basename(html)
        manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
            i + 1, basename)
        spine += '<itemref idref="file_%s" />' % (i + 1)
        epub.write(html, 'OEBPS/' + basename)

    info['manifest'] = manifest
    info['spine'] = spine
    info['toc'] = toc

    # Finally, write the index and toc
    epub.writestr('OEBPS/stylesheet.css', stylesheet_tpl)
    epub.writestr('OEBPS/Content.opf', index_tpl % info)
    epub.writestr('OEBPS/toc.ncx', toc_tpl % info)
