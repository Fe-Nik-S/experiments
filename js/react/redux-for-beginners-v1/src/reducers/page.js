
import { ACTION_SET_YEAR } from '../constants';

const initialState = {
    year: 2015,
    photos: []
}

export default function page(state = initialState, action) {

    switch (action.type) {

        case ACTION_SET_YEAR:
            return { ...state, year: action.payload }

        default:
            return state
    }

}
