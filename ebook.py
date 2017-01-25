import mimetypes
import os.path
import zipfile

from template import templates

html_files = ['blog.html']

if __name__ == '__main__':
    # TODO Add Image URL
    index_tpl = templates['index_tpl']
    cover_tpl = templates['cover_tpl']
    stylesheet_tpl = templates['stylesheet_tpl']
    toc_tpl = templates['toc_tpl']
    cover = 'cover.png'
    cpath = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
    ctype = 'image/gif'
    if cover is not None:
        cpath = 'images/cover' + os.path.splitext(os.path.abspath(cover))[1]
        ctype = mimetypes.guess_type(os.path.basename(os.path.abspath(cover)))[0]

    epub = zipfile.ZipFile('test.epub', 'w')

    # Metadata about the book
    info = dict(title='Title',
                subject='',
                description='',
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
