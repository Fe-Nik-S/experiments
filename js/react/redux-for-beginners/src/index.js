
import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import App from './controls/App';
import configureStore from './store/configurator';
import 'babel-polyfill';
import './custom.css';


const store = configureStore()


render(
    <Provider store={store}>
        <div className='app'>
            <App />
        </div>
    </Provider>,
    document.getElementById('root')
)
