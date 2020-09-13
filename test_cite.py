import unittest
from cite import Cite, Author, PageRange

class TestAuthor(unittest.TestCase):
    def test_author(self):
        a = Author('James Brown')
        self.assertEqual(str(a), 'James Brown')
        self.assertEqual(list(reversed(a)), ['Brown', 'James'])

        a.name = 'James Kitchener Brown'
        self.assertEqual(str(a), 'James Kitchener Brown')
        a.initials = True
        self.assertEqual(str(a), 'J. K. Brown')
        self.assertEqual(list(reversed(a)), ['Brown', 'J.', 'K.'])
        

# https://guides.lib.uw.edu/c.php?g=341448&p=4076094
class TestToMLA(unittest.TestCase):

    def test_basic_book(self):
        cite = Cite('The Bible (Authorized Version)')
        self.assertEqual(cite.to_mla(), 'The Bible (Authorized Version).')
        cite.authors.append(Author('King James'))
        self.assertEqual(cite.to_mla(), 'James, King. The Bible (Authorized Version).')
        cite.markup = Cite.MARKUP_MARKDOWN
        self.assertEqual(cite.to_mla(), 'James, King. *The Bible (Authorized Version).*')
        cite.markup = Cite.MARKUP_HTML
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible (Authorized Version).</em>')
        cite.city = 'London'
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible (Authorized Version).</em> London.')
        cite.year = 1611
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible (Authorized Version).</em> London, 1611.')
        cite.title = 'The Bible'
        cite.subtitle = 'Authorized Version'
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible: Authorized Version.</em> London, 1611.')
        

    def test_two_authors(self):
        cd = Author('Cynthia Davis')
        jb = Author('Jack Brown')
        cite = Cite('Landscape Gardening', authors=[cd, jb], publisher='Wiley & Sons', year=1994)
        self.assertEqual(cite.to_mla(), 'Davis, Cynthia, and Brown, Jack. Landscape Gardening. Wiley & Sons, 1994.');
        cite.year = None
        self.assertEqual(cite.to_mla(), 'Davis, Cynthia, and Brown, Jack. Landscape Gardening. Wiley & Sons.');
        cite.year = 1994
        cite.publisher = None
        self.assertEqual(cite.to_mla(), 'Davis, Cynthia, and Brown, Jack. Landscape Gardening. 1994.');
        cite.markup = Cite.MARKUP_MARKDOWN
        self.assertEqual(cite.to_mla(), 'Davis, Cynthia, and Brown, Jack. *Landscape Gardening.* 1994.');
        cite.publisher = 'Wiley & Sons'
        cite.markup = Cite.MARKUP_HTML
        self.assertEqual(cite.to_mla(), 'Davis, Cynthia, and Brown, Jack. <em>Landscape Gardening.</em> Wiley & Sons, 1994.');

    def test_edition(self):
        cite = Cite(title='17th Century Plays and Playwrights', authors=['William Shakespeare', 'Christopher Marlowe'], edition='98th', year=1620, city='London', publisher='The Globe Theatre Company')
        self.assertEqual(cite.to_mla(), 'Shakespeare, William, and Marlowe, Christopher. 17th Century Plays and Playwrights. 98th ed. London: The Globe Theatre Company, 1620.')


    def test_anthology(self):
        bs = Author('Bob Smith')
        sp = Author('Sheila Pearson')
        jm = Author('James McDonald')
        nt = Author('Neil Tavistock')
        cite = Cite(title='Incan Mythology', authors=[bs, sp, jm], publisher='Macmillan', year=2002, 
                    in_title='All the Worlds Mythology', in_authors=nt)
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. "Incan Mythology." All the Worlds Mythology. Neil Tavistock. Macmillan, 2002.')
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. "Incan Mythology." All the Worlds Mythology. Neil Tavistock. Macmillan, 2002.')

        cite.pages=PageRange(25, 31)
        cite.markup = Cite.MARKUP_HTML
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. &ldquo;Incan Mythology.&rdquo; <em>All the Worlds Mythology.</em> Neil Tavistock. Macmillan, 2002. pp. 25-31.')

        cite.pages=[PageRange(10, 20), '25-40', 96, '129 - 132']
        cite.markup = Cite.MARKUP_MARKDOWN
        cite.in_authors_role = 'Edited by'
        cite.subtitle = 'New Perspectives'
        cite.in_subtitle = 'Historical, Religious, and Ethnographical'
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. "Incan Mythology: New Perspectives." *All the Worlds Mythology: Historical, Religious, and Ethnographical.* Edited by Neil Tavistock. Macmillan, 2002. pp. 10-20, 25-40, 96, 129-132.')


# https://apastyle.apa.org/
class TestToAPA(unittest.TestCase):
    def test_book(self):
        cite = Cite('How to eat friends and barbecue people', authors='Hannibal Lecter', year=1989, 
                    publisher='Carne Press')
        self.assertEqual(cite.to_apa(), 'Lecter, H. (1989). How to eat friends and barbecue people. Carne Press.')
        cite.markup = Cite.MARKUP_HTML
        self.assertEqual(cite.to_apa(), 'Lecter, H. (1989). <em>How to eat friends and barbecue people.</em> Carne Press.')

    def test_book_many_authors(self):
        cite = Cite('Chainsaw Juggling for Beginners', 
                authors=[Author('James F. Fredrickson'), 'Bob Tweedle', Author('F. Maria Juanita Lopez')],
                year=2000, publisher='Inadvisable Press', city='Denmark', markup=Cite.MARKUP_MARKDOWN)
        self.assertEqual(cite.to_apa(), 'Fredrickson, J. F., Tweedle, B., & Lopez, F. M. J. (2000). *Chainsaw Juggling for Beginners.* Denmark: Inadvisable Press.')

    def test_journal(self):
        cite = Cite(title='Wigwams in Timbuktu: Dispersion data and comparisons with previous work',
                authors=Author('David Frederick Livingston'), in_title='Wigwam Studies', 
                    volume=10, issue=2, pages=PageRange(15,22), year=2011,
                    url='https://doi.org/12345.6789/ws0001234', markup=Cite.MARKUP_MARKDOWN)
        self.assertEqual(cite.to_apa(), 'Livingston, D. F. (2011). Wigwams in Timbuktu: Dispersion data and comparisons with previous work. *Wigwam Studies, 10*(2), 15-22. https://doi.org/12345.6789/ws0001234')


if __name__ == '__main__':
    unittest.main()
