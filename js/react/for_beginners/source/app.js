
let newsData = [
    {
        author: 'James Bond',
        text: 'Texts in retro style...',
        fullText: 'Texts in retro style can take you or your audience to the good old memories. Retro fonts can be used when...'
    },
    {
        author: 'Frodo Baggins',
        text: 'Retro style fonts are outdated...',
        fullText: 'Retro style fonts are outdated or aged style fonts that imply a vintage of at least 15 or 20 years...'
    },
    {
        author: 'Guest',
        text: 'The word “Retro” comes...',
        fullText: 'The word “Retro” comes from Latin word retro, meaning backward or past times...'
    }
];

let Article = React.createClass({
    propTypes: {
        attributes: React.PropTypes.shape({
            author: React.PropTypes.string.isRequired,
            text: React.PropTypes.string.isRequired,
            fullText: React.PropTypes.string.isRequired
        })
    },
    getInitialState: function() {
        return {
            isVisible: false
        };
    },
    showDetailsOnClick: function(e) {
        e.preventDefault();
        this.setState({isVisible: true});
    },
    render: function() {
        let author = this.props.attributes.author,
            text = this.props.attributes.text,
            fullText = this.props.attributes.fullText,
            isVisible = this.state.isVisible;

        console.log('Rendered: ',this);

        return (
            <div className="article">
                <p className="news__author">{author}</p>
                <p className="news__text">{text}</p>
                <a href="#"
                   onClick={this.showDetailsOnClick}
                   className={'news__details ' + (isVisible ? 'none': '')} >
                    Details...
                </a>
                <p className={'news__full-text ' + (isVisible ? '': 'none')}>{fullText}</p>
            </div>
        )
    }
});

let News = React.createClass({
    propTypes: {
        latestNews: React.PropTypes.array.isRequired
    },
    getInitialState: function() {
        return {
            counter: 0
        }
    },
    onTotalNewsClick: function() {
        this.setState({ counter: ++this.state.counter });
    },
    render: function() {
        let latestNews = this.props.latestNews;
        let newsTemplate = <p>No news</p>;
        let needShowNews = latestNews.length > 0

        if (needShowNews) {
            newsTemplate = latestNews.map( function(item, index) {
                return (
                    <div key={index}>
                        <Article attributes={item} />
                    </div>
                )
            })
        }

        return (
            <div className="news">
                {newsTemplate}
                <strong onClick={this.onTotalNewsClick} className={'news__count ' + (needShowNews ? '': 'none') }>All news: {latestNews.length}</strong>
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

var TestInput = React.createClass({
    getInitialState: function() {
        return {
            controlValue: ''
        };
    },
    onChangeHandler: function(e) {
        this.setState({controlValue: e.target.value})
    },
    onBtnClickHandler: function() {
        alert(this.state.controlValue);
    },
    render: function() {
        return (
            <div>
                <input
                    className='test-input'
                    value={this.state.controlValue}
                    onChange={this.onChangeHandler}
                    placeholder='Enter value...'
                />
                <button onClick={this.onBtnClickHandler}>Show alert</button>
            </div>
        );
    }
});

let App = React.createClass({
    render: function() {
        return (
            <div className="app">
                <p>This page demonstrates using React with no build tooling.</p>
                <p/>
                <h3>News:</h3>
                <TestInput />
                <News latestNews={newsData}/>
            </div>
        );
    }
});

ReactDOM.render(
    <App />,
    document.getElementById('root')
);
