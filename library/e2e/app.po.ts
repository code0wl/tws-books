import { browser, element, by } from 'protractor';

export class TwsLibraryPage {
  navigateTo() {
    return browser.get('/');
  }

  getParagraphText() {
    return element(by.css('twsl-root h1')).getText();
  }
}
