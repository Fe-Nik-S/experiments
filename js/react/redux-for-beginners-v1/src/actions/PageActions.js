
import {
    ACTION_SET_YEAR,
    GET_PHOTOS_REQUEST,
    GET_PHOTOS_SUCCESS
} from '../constants';


export function setYear(year) {
    return {
        type: ACTION_SET_YEAR,
        payload: year
    }
}


export function getPhotos(year) {
    return (dispatch) => {
        dispatch({
            type: GET_PHOTOS_REQUEST,
            payload: year
        });

        setTimeout(() => {
            dispatch({
                type: GET_PHOTOS_SUCCESS,
                payload: [1, 2, 3, 4, 5]
            })
        }, 1000)
    }
}
