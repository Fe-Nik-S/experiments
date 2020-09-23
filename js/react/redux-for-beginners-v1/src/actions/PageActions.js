
import { ACTION_SET_YEAR} from '../constants';


export function setYear(year) {
    return {
        type: ACTION_SET_YEAR,
        payload: year
    }
}
