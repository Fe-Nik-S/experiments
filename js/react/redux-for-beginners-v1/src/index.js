
import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import App from './controls/App'
import { Provider } from 'react-redux'
import configureStore from './store/configurator'

const store = configureStore()

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
)
