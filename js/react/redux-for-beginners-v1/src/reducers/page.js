
import {
    ACTION_SET_YEAR,
    GET_PHOTOS_SUCCESS,
    GET_PHOTOS_REQUEST,
    GET_PHOTOS_FAIL
} from '../constants';

const initialState = {
    query: 'Laptop',
    photos: [],
    fetching: false,
    error: ''
}

export default function page(state = initialState, action) {

    switch (action.type) {

        case ACTION_SET_YEAR:
            return { ...state, query: action.payload }

        case GET_PHOTOS_REQUEST:
            return { ...state, query: action.payload, fetching: true, error: '' }
        case GET_PHOTOS_SUCCESS:
            return { ...state, photos: action.payload, fetching: false, error: '' }
        case GET_PHOTOS_FAIL:
            return { ...state, error: action.payload.message, fetching: false }

        default:
            return state
    }

}
