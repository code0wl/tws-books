import { TwsLibraryPage } from './app.po';

describe('tws-library App', function() {
  let page: TwsLibraryPage;

  beforeEach(() => {
    page = new TwsLibraryPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('twsl works!');
  });
});
