from EWTScraper import EWTScraper
import logging

class FFTodayScraper(EWTScraper):
    '''
    Obtains html content of NFL fantasy projections page of fantasycalculator.com

    Example:
        s = FFTodayScraper()
        content = s.get_projections()
        content = s.get_projections(positions=['qb','wr'])
        content = s.get_projections(positions=['qb','wr'], fn='ffpros.html')
    '''

    def __init__(self, **kwargs):
        '''
        Args:
            **kwargs: projections_urls (list)
        '''

        # see http://stackoverflow.com/questions/8134444/python-constructor-of-derived-class
        EWTScraper.__init__(self, **kwargs)

        if 'projections_urls' in 'kwargs':
            self.projections_urls = kwargs['projections_urls']
        else:
            self.projections_urls = {
                'qb': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=10&LeagueID=26955',
                'rb1': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=20&LeagueID=26955',
                'rb2': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=20&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=1',
                'wr1': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=30&LeagueID=26955',
                'wr2': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=30&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=1',
                'te': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=40&LeagueID=26955',
                'dst': 'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=99&LeagueID=26955',
            }

    def _fix_positions(self, positions):

        fixed_positions = []

        for position in positions:
            position = position.lower()

            if position == 'rb':
                fixed_positions = fixed_positions + ['rb1', 'rb2']

            elif position == 'wr':
                fixed_positions = fixed_positions + ['wr1', 'wr2']

            else:
                fixed_positions.append(position)

        return fixed_positions

    def get_projections(self, positions=None, fname=None):
        '''
        Fetch projections url, try cache, then file, then web
        Args:
            url (str): url for the fantasy football calculator projections page
        Returns:
            Str if successful, None otherwise.
        '''
        
        pages = []

        if positions:
            positions = self._fix_positions(positions)
            logging.debug(positions)
            urls = [self.projections_urls[x] for x in positions if x in self.projections_urls.keys()]
            logging.debug(urls)
        else:
            urls = self.projections_urls.values()

        for url in urls:
            page = self.get(url, fname)
            
            if page:
                pages.append(page)
            else:
                logging.debug('no page to append: %s' % url)

        return pages
                
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s = FFTodayScraper()
    s.get_projections(positions=['QB'])
    s.get_projections(positions=['QB', 'K'])