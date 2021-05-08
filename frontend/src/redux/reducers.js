import { combineReducers } from "redux"
import { SummaryReducer } from "./summarize"

// register all reducers for the various store spaces
export const rootReducer = combineReducers({
    summary: SummaryReducer,
})

export default rootReducer
