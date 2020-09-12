import datetime

# Types of referencing:
# Chicago
# - Author-Date
# - Notes-Bibliography
#
# MLA
# 
# APA
#
# IEEE
#
# ASA

# Distinctions: Version (e.g. APA 6th vs 7th), Subtype (Chicago Author-Date vs Notes-Bibliography),
#  In-text vs page footnote vs end-of-document reference list, 
# 

class Cite:
    """Class for any type of citation."""
    SUPPORTED_ATTRS = ('title', 'subtitle', 'authors', 'pages',
                    'city', 'publisher', 'year', 
                    'in_title', 'in_subtitle', 'in_authors', 'in_authors_role', 
                    'journal', 'volume', 'issue', 'date', 'url', 'retrieved_date', 
                    'markup')

    MARKUP_NONE = 0
    MARKUP_MARKDOWN = 1
    MARKUP_HTML = 2

    PAGE_ABBREV = 'p'
    PAGES_ABBREV = 'pp'

    OPENING_ITALICS = {
        MARKUP_NONE: '',
        MARKUP_MARKDOWN: '*',
        MARKUP_HTML: '<em>'
    }
    CLOSING_ITALICS = {
        MARKUP_NONE: '',
        MARKUP_MARKDOWN: '*',
        MARKUP_HTML: '</em>'
    }

    # Plural properties are lists
    def __init__(self, title, subtitle=None, authors=None, pages=None,
                    city=None, publisher=None, year=None,
                    in_title=None, in_subtitle=None, in_authors=None, in_authors_role=None, 
                    volume=None, issue=None, date=None, url=None, retrieved_date=None,
                    markup=MARKUP_NONE):
        # Careful when adding new attributes because of __setattr__()
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.pages = pages
        self.city = city
        self.publisher = publisher
        self.year = year

        # Whatever contains this work - a newspaper, journal, an edited book/anthology, a website
        self.in_title = in_title
        self.in_subtitle = in_subtitle
        self.in_authors = in_authors
        self.in_authors_role = in_authors_role

        self.volume = volume
        self.issue = issue
        self.date = date
        self.url = url
        self.retrieved_date = retrieved_date

        self.markup = markup

    def __setattr__(self, name, value):
        if name not in self.SUPPORTED_ATTRS:
            raise AttributeError("The attribute '{}' is unsupported. Supported attributes: {}".format(
                name, ' '.join(self.SUPPORTED_ATTRS)))
        if name[-1] == 's':
            if value is None:
                value = []
            if type(value) is not list:
                value = [value]
        if name == 'authors':
            for a in value:
                if type(a) is str:
                    a = Author(a)
        if name == 'pages':
            for idx, elem in enumerate(value):
                if type(elem) is not PageRange:
                    pr = PageRange(elem)
                    value[idx] = pr
        super().__setattr__(name, value)


    def to_mla(self):
        in_larger = bool(self.in_title or self.in_subtitle or self.in_authors)
        output = ''
        if self.authors:
            except_final_authors = self.authors[:-1]
            efa_len = len(except_final_authors)
            for idx, author in enumerate(except_final_authors):
                if author.name == '' and author.lastname == '': 
                    continue
                tmp = list(reversed(author))
                output += tmp[0] + ', ' + ' '.join(tmp[1:])
                if efa_len > 1 and idx < efa_len - 1:
                    output += ', '
            if len(self.authors) > 1:
                output += ', and '
            last_author = self.authors[-1]
            if not (last_author.name == '' and last_author.lastname == ''):
                tmp = list(reversed(last_author))
                output += tmp[0] + ', ' + ' '.join(tmp[1:])
            output += '. '

        if not in_larger:
            output += self.OPENING_ITALICS[self.markup]
        if in_larger:
            if self.markup == self.MARKUP_HTML:
                output += '&ldquo;'
            else:
                output += '"'
        output += self.title
        if self.subtitle:
            output += ': ' + self.subtitle
        output += '.'
        if not in_larger:
            output += self.CLOSING_ITALICS[self.markup]
        if in_larger:
            if self.markup == self.MARKUP_HTML:
                output += '&rdquo;'
            else:
                output += '"'

        if in_larger:
            output += ' '
            output += self.OPENING_ITALICS[self.markup]
            output += self.in_title
            if self.in_subtitle:
                output += ': ' + self.in_subtitle
            output += '.'
            output += self.CLOSING_ITALICS[self.markup]

        if self.in_authors_role and self.in_authors:
            output += ' '
            output += self.in_authors_role
        if self.in_authors:
            output += ' '
            except_final_authors = self.in_authors[:-1]
            efa_len = len(except_final_authors)
            for idx, author in enumerate(except_final_authors):
                output += str(author)
                if idx < efa_len - 2:
                    output += ', '
                elif idx < efa_len - 1:
                    output += ', and '
            output += str(self.in_authors[-1])
            output += '.'

        if self.city:
            output += ' ' + self.city
        if self.city and self.publisher:
            output += ':'
        elif self.city and self.year:
            output += ','
        elif self.city:
            output += '.'
        if self.publisher:
            output += ' ' + self.publisher
        if self.year and self.publisher:
            output += ','
        elif self.publisher:
            output += '.'
        if self.year:
            output += ' ' + str(self.year) + '.'
        elif self.date:
            output += ' ' + str(self.date.year) + '.'

        if self.pages:
            output += ' '
            pages_len = len(self.pages)
            if pages_len == 1 and len(self.pages[0]) == 1:
                output += self.PAGE_ABBREV + '. '
            else:
                output += self.PAGES_ABBREV + '. '
            for idx, pr in enumerate(self.pages):
                if idx < pages_len - 1:
                    output += str(pr) + ', '
                else:
                    output += str(pr)
            output += '.'

        return output


    def to_apa(self):
        output = ''
        
        if self.authors:
            authors_copy = [reversed(x) for x in self.authors]
            for idx, a in authors_copy:
                authors_copy[idx].initials = True
            output += ', '.join(authors_copy)

        return output 


class AuthorIterator:
    def __init__(self, author):
        self.i = 0
        self.chunks = author.name.split()
        if author.initials:
            tmp = []
            for chunk in self.chunks[:-1]:
                tmp.append(author._to_initials(chunk))
            tmp.append(self.chunks[-1])
            self.chunks = tmp
        self.chunks_len = len(self.chunks)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.chunks_len:
            self.i += 1
            return self.chunks[self.i - 1]
        else:
            raise StopIteration()

    def __str__(self):
        return ' '.join(self.chunks)
    
class AuthorReverseIterator:
    def __init__(self, author):
        self.author = author
        self.chunks = author.name.split()
        tmp = [self.chunks[-1]]
        for chunk in self.chunks[:-1]:
            if author.initials:
                tmp.append(author._to_initials(chunk))
            else:
                tmp.append(chunk)
        self.chunks = tmp
        self.chunks_len = len(self.chunks)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.chunks_len:
            self.i += 1
            return self.chunks[self.i - 1]
        else:
            raise StopIteration()

    def __str__(self):
        if self.chunks_len < 1:
            return ''
        s = self.chunks[0]
        if self.chunks_len > 1:
            s += ', '
            s += ' '.join(self.chunks[1:]) 
        return s

# https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
class Author:
    """Class for an author"""

    def __init__(self, name, initials=False):
        self.name = name
        self.initials = initials

    def __repr__(self):
        return "Author(name='{}'{})".format(
            self.name,
            ', initials=True' if self.initials else ''
        )

    def __str__(self):
        if self.initials:
            tmp = self.name.split()
            initials = [self._to_initials(x) for x in tmp[:-1]]
            return ' '.join(initials) + ' ' + tmp[-1]
        else:
            return self.name

    def __iter__(self):
        return AuthorIterator(self)

    def __reversed__(self):
        return AuthorReverseIterator(self)

    def _to_initials(self, components):
        if type(components) is not list:
            components = [components]
        tmp = [x[0].upper() + '.' for x in components]
        return ' '.join(tmp) 


class PageRange:
    """A 'range' analogue that support ordering (by .begin), and has [begin,end] semantics
       (includes 'end' value).

       Differences to range():
        * no 'step'
        * 'begin' and 'end' to make clear the difference from range()
        * [begin, end] semantics, not [start, stop) semantics ('end' value included)
        * len(PageRange(x)) == 1
        * PageRanges are comparable to each other and to integers based on .begin
    """

    def __init__(self, begin, end=None):
        # Handle various string formats
        if type(begin) is str:
            if '-' in begin:
                tmp = begin.split('-')
                if len(tmp) < 2:
                    raise TypeError("Bad string argument to PageRange(): Needs form 'x - y'")
                begin = int(tmp[0])
                end = int(tmp[1])
        if end is None:
            end = begin
        self.r = range(begin, end + 1)

    def __repr__(self):
        if self.r.step != 1:
            tmp = ', ' + self.r.step
        else:
            tmp = ''
        if abs(self.r.stop - self.r.start) > 1:
            return 'PageRange({}, {}{})'.format(self.r.start, self.r.stop - 1, tmp)
        else:
            return 'PageRange({})'.format(self.r.start)

    def __str__(self):
        if abs(self.r.stop - self.r.start) > 1:
            return str(self.r.start) + '-' + str(self.r.stop - 1)
        else:
            return str(self.r.start)

    def __getattr__(self, name):
        if name == 'begin':
            return self.r.start
        if name == 'end':
            return self.r.stop - 1
        raise AttributeError("PageRange supports 'begin' and 'end' attributes")

    def __len__(self):
        return len(self.r)

    def __contains__(self, item):
        return item in self.r

    def __iter__(self):
        return self.r.__iter__()

    def __lt__(self, other):
        if type(other) is not PageRange:
            return self.r.start < int(other)
        return self.r.start < other.r.start

    def __le__(self, other):
        if type(other) is not PageRange:
            return self.r.start <= int(other)
        return self.r.start <= other.r.start

    def __eq__(self, other):
        if type(other) is not PageRange:
            return self.r.start == int(other)
        return self.r.start == other.r.start

