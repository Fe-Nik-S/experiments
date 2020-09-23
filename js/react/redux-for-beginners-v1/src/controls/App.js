
import React, { Component } from 'react'
import { connect } from 'react-redux'


class App extends Component {
    render() {
        return <div>
            <p>Redux tutorial</p>
        </div>
    }
}

function mapStateToProps (state) {
    return {
        user: state.user,
        page: state.page
    }
}

export default connect(mapStateToProps)(App)
