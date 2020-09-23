
import { createStore, applyMiddleware } from 'redux';
import rootReducer from '../reducers';
import { ping } from '../enhancers/ping'


export default function configureStore(initialState) {
    const store = createStore(rootReducer, initialState, applyMiddleware(ping));

    if (module.hot) {
        module.hot.accept('../reducers', () => {
            const nextRootReducer = require('../reducers')
            store.replaceReducer(nextRootReducer)
        })
    }

    return store
}
