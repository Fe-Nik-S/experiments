
import {
    ACTION_SET_YEAR,
    GET_PHOTOS_REQUEST,
    GET_PHOTOS_SUCCESS,
    GET_PHOTOS_FAIL,
    SPLASH_REQUEST_TEMPLATE
} from '../constants';


export function setYear(query) {
    return {
        type: ACTION_SET_YEAR,
        payload: query
    }
}

function getPhotosByQuery(query, dispatch) {
    fetch(SPLASH_REQUEST_TEMPLATE + '?query=' + query)
        .then(res => res.json())
        .then(
            (res) => {
                let photos = res.images.map((item) => item.url );
                dispatch({
                    type: GET_PHOTOS_SUCCESS,
                    payload: photos
                })
            },
            (error) => {
                dispatch({
                    type: GET_PHOTOS_FAIL,
                    error: true,
                    payload: new Error(error)
                })
            }
        )
}

export function getPhotos(query) {
    return (dispatch) => {
        dispatch({
            type: GET_PHOTOS_REQUEST,
            payload: query
        });

        getPhotosByQuery(query, dispatch);
    }
}
