
import {
    ACTION_SET_YEAR,
    GET_PHOTOS_SUCCESS,
    GET_PHOTOS_REQUEST
} from '../constants';

const initialState = {
    year: 2015,
    photos: [],
    fetching: false
}

export default function page(state = initialState, action) {

    switch (action.type) {

        case ACTION_SET_YEAR:
            return { ...state, year: action.payload }
        case GET_PHOTOS_REQUEST:
            return { ...state, year: action.payload, fetching: true }
        case GET_PHOTOS_SUCCESS:
            return { ...state, photos: action.payload, fetching: false }

        default:
            return state
    }

}
