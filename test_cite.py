import unittest
from cite import Cite, Author, PageRange

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
        cite.authors = []
        cite.authors.append(Author(firstname='King', lastname='James'))
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible (Authorized Version).</em>')
        cite.city = 'London'
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible (Authorized Version).</em> London.')
        cite.year = 1611
        self.assertEqual(cite.to_mla(), 'James, King. <em>The Bible (Authorized Version).</em> London, 1611.')
        

    def test_two_authors(self):
        cd = Author(firstname='Cynthia', lastname='Davis')
        jb = Author(firstname='Jack', lastname='Brown')
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


    def test_larger_anthology(self):
        bs = Author(name='Bob Smith')
        sp = Author(name='Sheila Pearson')
        jm = Author(name='James McDonald')
        nt = Author(firstname='Neil', lastname='Tavistock')
        cite = Cite(title='Incan Mythology', authors=[bs, sp, jm], publisher='Macmillan', year=2002, 
                    larger_title='All the Worlds Mythology', larger_authors=nt)
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. "Incan Mythology." All the Worlds Mythology. Neil Tavistock. Macmillan, 2002.')

        cite.page_ranges=PageRange(25, 31)
        cite.markup = Cite.MARKUP_HTML
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. &ldquo;Incan Mythology.&rdquo; <em>All the Worlds Mythology.</em> Neil Tavistock. Macmillan, 2002. pp. 25-31.')

        cite.page_ranges=[PageRange(10, 20), '25-40', 96, '129 - 132']
        cite.markup = Cite.MARKUP_MARKDOWN
        cite.larger_authors_role = 'Edited by'
        self.assertEqual(cite.to_mla(), 'Smith, Bob, Pearson, Sheila, and McDonald, James. "Incan Mythology." *All the Worlds Mythology.* Edited by Neil Tavistock. Macmillan, 2002. pp. 10-20, 25-40, 96, 129-132.')


# https://apastyle.apa.org/
# class TestToAPA(unittest.TestCase)


if __name__ == '__main__':
    unittest.main()
