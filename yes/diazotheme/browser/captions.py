from cgi import escape
import re

from ZODB.POSException import ConflictError
from Acquisition import aq_base, aq_acquire, aq_parent
from zExceptions import NotFound
from zope.publisher.interfaces import NotFound as ztkNotFound
from zope.component.hooks import getSite

from urllib import unquote
from urlparse import urljoin
from urlparse import urlsplit

from plone.outputfilters.filters.resolveuid_and_caption import \
    ResolveUIDAndCaptionFilter as base_filter

resolveuid_re = re.compile('^[./]*resolveuid/([^/]*)/?(.*)$')
singleton_tags = ["img", "area", "br", "hr", "input", "meta", "param", "col"]

class YesResolveUIDAndCaptionFilter(base_filter):
    """ Parser to convert UUID links and captioned images.  Handles custom
    Image fields in yes.content: caption, credit.
    """
    
    def resolve_image(self, src):
        description = ''
        caption = ''
        credit = ''
        if urlsplit(src)[0]:
            # We have a scheme
            return None, None, src, description, caption, credit

        base = self.context
        subpath = src
        appendix = ''

        def traversal_stack(base, path):
            """uncustomized"""
            if path.startswith('/'):
                base = getSite()
                path = path[1:]
            obj = base
            stack = [obj]
            components = path.split('/')
            while components:
                child_id = unquote(components.pop(0))
                try:
                    if hasattr(aq_base(obj), 'scale'):
                        if components:
                            child = obj.scale(child_id, components.pop())
                        else:
                            child = obj.scale(child_id)
                    else:
                        # Do not use restrictedTraverse here; the path to the
                        # image may lead over containers that lack the View
                        # permission for the current user!
                        # Also, if the image itself is not viewable, we rather
                        # show a broken image than hide it or raise
                        # unauthorized here (for the referring document).
                        child = obj.unrestrictedTraverse(child_id)
                except ConflictError:
                    raise
                except (AttributeError, KeyError, NotFound, ztkNotFound):
                    return
                obj = child
                stack.append(obj)
            return stack

        def traverse_path(base, path):
            """ uncustomized """
            stack = traversal_stack(base, path)
            if stack is None:
                return
            return stack[-1]

        obj, subpath, appendix = self.resolve_link(src)
        
        if obj is not None:
            # resolved uid
            fullimage = obj
            image = traverse_path(fullimage, subpath)
        elif '/@@' in subpath:
            # split on view
            pos = subpath.find('/@@')
            fullimage = traverse_path(base, subpath[:pos])
            if fullimage is None:
                return None, None, src, description, caption, credit
            image = traverse_path(fullimage, subpath[pos + 1:])
            if image is None:
                return None, None, src, description, caption, credit
        else:
            stack = traversal_stack(base, subpath)
            if stack is None:
                return None, None, src, description, caption, credit
            image = stack.pop()
            # if it's a scale, find the full image by traversing one less
            # actually, this won't always work because some types that aren't
            # images have image fields with scales, like Articles and Issues
            # so we have to check for Image type
            fullimage = image
            stack.reverse()
            for parent in stack:
                if parent.portal_type == 'Image':
                    fullimage = parent
                    break

        try:
            src = image.absolute_url() + appendix
            description = aq_acquire(fullimage, 'Description')()
            caption = aq_acquire(fullimage, 'getCaption')()
            credit = aq_acquire(fullimage, 'getCredit')()
            return image, fullimage, src, description, caption, credit
        except AttributeError:
            return None, None, src, description, caption, credit

    def handle_captioned_image(self, attributes, image, fullimage, caption, 
                               credit):
        """Handle captioned image.
        """
        klass = attributes['class']
        del attributes['class']
        del attributes['src']
        view = fullimage.restrictedTraverse('@@images', None)
        if view is not None:
            original_width, original_height = view.getImageSize()
        else:
            original_width, original_height = fullimage.width, fullimage.height
        if image is not fullimage:
            # image is a scale object
            tag = image.tag
            width = image.width
        else:
            if hasattr(aq_base(image), 'tag'):
                tag = image.tag
            else:
                tag = view.tag
            width = original_width
        options = {
            'class': klass,
            'originalwidth': attributes.get('width', None),
            'originalalt': attributes.get('alt', None),
            'url_path': fullimage.absolute_url_path(),
            'caption': caption, #no html quoting since this is rich text
            'credit': credit, #no html quoting since this is rich text
            'image': image,
            'fullimage': fullimage,
            'tag': tag(**attributes),
            'isfullsize': image is fullimage or (
                          image.width == original_width and
                          image.height == original_height),
            'width': attributes.get('width', width),
            }
        if self.in_link:
            # Must preserve original link, don't overwrite
            # with a link to the image
            options['isfullsize'] = True

        captioned_html = self.captioned_image_template(**options)
        if isinstance(captioned_html, unicode):
            captioned_html = captioned_html.encode('utf8')
        self.append_data(captioned_html)
        
    def unknown_starttag(self, tag, attrs):
        """Here we've got the actual conversion of links and images.

        Convert UUID's to absolute URLs, and process captioned images to HTML.
        """
        if tag in ['a', 'img', 'area']:
            # Only do something if tag is a link, image, or image map area.

            attributes = dict(attrs)
            if tag == 'a':
                self.in_link = True
            if (tag == 'a' or tag == 'area') and 'href' in attributes:
                href = attributes['href']
                scheme = urlsplit(href)[0]
                if not scheme and not href.startswith('/') \
                        and not href.startswith('mailto<') \
                        and not href.startswith('#'):
                    obj, subpath, appendix = self.resolve_link(href)
                    if obj is not None:
                        href = obj.absolute_url()
                        if subpath:
                            href += '/' + subpath
                        href += appendix
                    elif resolveuid_re.match(href) is None:
                        # absolutize relative URIs; this text isn't necessarily
                        # being rendered in the context where it was stored
                        relative_root = self.context
                        if not getattr(
                            self.context, 'isPrincipiaFolderish', False):
                            relative_root = aq_parent(self.context)
                        actual_url = relative_root.absolute_url()
                        href = urljoin(actual_url + '/', subpath) + appendix
                    attributes['href'] = href
                    attrs = attributes.iteritems()
            elif tag == 'img':
                src = attributes.get('src', '')
                image, fullimage, src, description, caption, credit = \
                    self.resolve_image(src)
                attributes["src"] = src
                caption = caption != '' and caption or ''
                credit = credit

                # Check if the image needs to be captioned
                if (self.captioned_images and image is not None and (caption
                    or credit) \
                    and 'captioned' in attributes.get('class', '').split(' ')):
                    self.handle_captioned_image(attributes, image, fullimage,
                                                caption, credit)
                    return True
                if fullimage is not None:
                    # Check to see if the alt / title tags need setting
                    title = aq_acquire(fullimage, 'Title')()
                    if 'alt' not in attributes:
                        attributes['alt'] = title
                    if 'title' not in attributes:
                        attributes['title'] = title
                    attrs = attributes.iteritems()

        # Add the tag to the result
        strattrs = "".join([' %s="%s"'
                               % (key, escape(value)) for key, value in attrs])
        if tag in singleton_tags:
            self.append_data("<%s%s />" % (tag, strattrs))
        else:
            self.append_data("<%s%s>" % (tag, strattrs))        