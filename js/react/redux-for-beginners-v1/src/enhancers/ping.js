
/*eslint-disable */
export const ping = store => next => action => {
    console.log(`EventType: ${action.type}, Data: ${action.payload}`);
    return next(action);
}
/*eslint-enable */

/*
var ping = function ping(store) {
    return function (next) {
        return function (action) {
            console.log('ping');
            return next(action);
        };
    };
};
 */
