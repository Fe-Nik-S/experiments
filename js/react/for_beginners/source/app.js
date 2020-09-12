
let newsData = [
    {
        author: 'James Bond',
        text: 'Texts in retro style can take you or your audience to the good old memories. Retro fonts can be used when...'
    },
    {
        author: 'Frodo Baggins',
        text: 'Retro style fonts are outdated or aged style fonts that imply a vintage of at least 15 or 20 years...'
    },
    {
        author: 'Guest',
        text: 'The word “Retro” comes from Latin word retro, meaning backward or past times...'
    }
];

let News = React.createClass({
    render: function() {
        let latestNews = this.props.latestNews;
        let newsTemplate = <p>No news</p>;
        let needShowNews = latestNews.length > 0

        if (needShowNews) {
            newsTemplate = latestNews.map( function(item, index) {
                return (
                    <div key={index}>
                        <p className="news__author">{item.author}:</p>
                        <p className="news__text">{item.text}</p>
                    </div>
                )
            })
        }

        return (
            <div className="news">
                {newsTemplate}
                <strong className={ needShowNews ? '': 'none' }>All news: {latestNews.length}</strong>
            </div>
        );
    }
});

let Comments = React.createClass({
    render: function() {
        return (
            <div className="comments">
                No news - nothing to comment
            </div>
        );
    }
});

let App = React.createClass({
    render: function() {
        return (
            <div className="app">
                <p>This page demonstrates using React with no build tooling.</p>
                <News latestNews={newsData}/>
                <Comments />
            </div>
        );
    }
});

ReactDOM.render(
    <App />,
    document.getElementById('root')
);
