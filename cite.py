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
    def __init__(self, title, subtitle=None, authors=None, author=None, page_ranges=None, pages=None,
                    city=None, publisher=None, year=None,
                    larger_title=None, larger_subtitle=None, larger_authors=None, 
                    larger_author=None, larger_authors_role=None, journal=None,
                    volume=None, issue=None, date=None, url=None, retrieved_date=None,
                    markup=MARKUP_NONE):
        # Careful when adding new attributes because of __setattr__()
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        if not authors and author:
            self.authors = [author]
        self.page_ranges = page_ranges
        self.city = city
        self.publisher = publisher
        self.year = year

        # Part of a larger work - a journal, an edited book/anthology, a website
        self.larger_title = larger_title
        if not larger_title and journal:
            self.larger_title = journal
        self.larger_subtitle = larger_subtitle
        self.larger_authors = larger_authors
        if not larger_authors and larger_author:
            self.larger_authors = [larger_author]
        self.larger_authors_role = larger_authors_role

        self.volume = volume
        self.issue = issue
        self.date = date
        self.url = url
        self.retrieved_date = retrieved_date

        self.markup = markup

    def __setattr__(self, name, value):
        supported    = ['title', 'subtitle', 'authors', 'page_ranges', 'city', 'publisher', 'year', 
                        'larger_title', 'larger_subtitle', 'larger_authors', 'larger_authors_role', 
                        'volume', 'issue', 'date', 'url', 'retrieved_date', 
                        'markup']
        if name not in supported:
            raise AttributeError("The property '{}' is unsupported. Supported properties: {}".format(
                name, ' '.join(supported)))
        if name[-1] == 's':
            if value is None:
                value = []
            if type(value) is not list:
                value = [value]
        if name == 'authors' or name == 'larger_authors':
            for a in value:
                if type(a) is str:
                    a = Author(a)
        if name == 'page_ranges':
            for idx, elem in enumerate(value):
                if type(elem) is not PageRange:
                    pr = PageRange(elem)
                    value[idx] = pr
        super().__setattr__(name, value)

    def to_mla(self):
        in_larger = bool(self.larger_title or self.larger_subtitle 
                         or self.larger_authors or self.larger_authors_role)
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
            output += self.larger_title
            if self.larger_subtitle:
                output += ': ' + self.larger_subtitle
            output += '.'
            output += self.CLOSING_ITALICS[self.markup]

        if self.larger_authors_role and self.larger_authors:
            output += ' '
            output += self.larger_authors_role
        if self.larger_authors:
            output += ' '
            except_final_authors = self.larger_authors[:-1]
            efa_len = len(except_final_authors)
            for idx, author in enumerate(except_final_authors):
                output += str(author)
                if idx < efa_len - 2:
                    output += ', '
                elif idx < efa_len - 1:
                    output += ', and '
            output += str(self.larger_authors[-1])
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

        if self.page_ranges:
            output += ' '
            pr_len = len(self.page_ranges)
            if pr_len == 1 and len(self.page_ranges[0]) == 1:
                output += self.PAGE_ABBREV + '. '
            else:
                output += self.PAGES_ABBREV + '. '
            for idx, pr in enumerate(self.page_ranges):
                if idx < pr_len - 1:
                    output += str(pr) + ', '
                else:
                    output += str(pr)
            output += '.'

        return output


    def to_apa():
        output = ''
        
        return output 


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

    def __reversed__(self):
        chunks = self.name.split()
        tmp = [chunks[-1]]
        if self.initials:
            for chunk in chunks[:-1]:
                tmp.append(self._to_initials(chunk))
        else:
            tmp.extend(chunks[:-1])
        return iter(tmp)

    def _to_initials(self, components):
        if type(components) is not list:
            components = [components]
        tmp = [x[0].upper() + '.' for x in components]
        return ' '.join(tmp) 


class PageRange:
    """A 'range' analogue that support ordering (by .start), and has [start,stop] semantics
       (includes 'stop' value)"""

    def __init__(self, start, stop=None, step=1):
        if type(start) is str:
            tmp = start.split('-')
            if len(tmp) < 2:
                raise TypeError("Bad string argument to PageRange(): Needs form 'x - y'")
            start = int(tmp[0])
            stop = int(tmp[1])
        if stop is None:
            stop = start
        self.r = range(start, stop + 1, step)

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

    def __len__(self):
        return len(self.r)

    def __contains__(self, item):
        return item in self.r

    def __iter__(self):
        return self.r.__iter__()

    def __lt__(self, other):
        return self.r.start < other.r.start

    def __le__(self, other):
        return self.r.start <= other.r.start

    def __eq__(self, other):
        return self.r.start == other.r.start

