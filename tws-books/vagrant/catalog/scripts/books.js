export class Books {

constructor (config) {

    this.template = `
    <section class="container">
        <header>
            <h1>${config.name} collection</h1>
        </header>
        <article>
            <ul>
                <li class="library-books__book">
                    <h3>
                        <span class="fa fa-{{i.medium}}"></span>
                        <a href="/{{f.name}}/books/{{config.id}}"> {{i.title}} </a>
                    </h3>
                    <p>
                        <img src="{{i.cover}}" /> {{i.description}}
                    </p>
                    <div class="meta-data">
                        <p>
                            <span class="fa fa-user"></span> Author: {{i.author}}
                            <div>
                                <img class="user-image" src="{{i.addedByImage}}" /> {{i.addedBy}}
                            </div>
                            {% endif %}
                        </p>
                        <aside class="row">
                            <div class="col-sm-5">
                                <a href="/{{f.name}}/books/{{i.id}}/edit">Edit</a>
                            </div>
                            <div class="col-sm-5">
                                <a href="/{{f.name}}/books/{{i.id}}/remove">Remove</a>
                            </div>
                        </aside>
                    </div>
                </li>
            </ul>
        </article>
    </section>`;

    }
}