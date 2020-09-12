
let News = React.createClass({
    render: function() {
        return (
            <div className="news">
                No news now.
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
                <News />
                <Comments />
            </div>
        );
    }
});

ReactDOM.render(
    <App />,
    document.getElementById('root')
);
