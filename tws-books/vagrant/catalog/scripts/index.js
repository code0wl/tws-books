import { Books } from './books';


new BookService();

class BookService {

    constructor()  {
        const xhr = new XMLHttpRequest();

        xhr.open('GET', 'http://localhost:5333/tws/books/JSON/');
        xhr.send();

        xhr.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                JSON.parse(this.responseText);
            }
        };
    }
}