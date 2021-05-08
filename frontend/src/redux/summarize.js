import Alert from "react-s-alert"
import util from "../util"

const summaryActions = {
    GET_SUMMARY: "GET_SUMMARY",
}

export const getSummary = (text) => ({
    type: summaryActions.GET_SUMMARY,
    payload: fetch("/api/summarize", {
        headers: util.getJsonHeader(),
        method: 'POST',
        body: JSON.stringify(text),
    }).then(util.restHandler),
})

const initialState = {
    one_paragraph_summary: "",
    one_line_summary: "",
    loading: false
}
// reducer

export const SummaryReducer = (state = initialState, action) => {
    switch (action.type) {
        case `${summaryActions.GET_SUMMARY}${util.actionTypeSuffixes.fulfilled}`: {
            return {
                ...state,
                one_line_summary: action.payload["one_line_summary"],
                one_paragraph_summary: action.payload["one_paragraph_summary"],
                is_loading: false
            }
        }
        case `${summaryActions.GET_SUMMARY}${util.actionTypeSuffixes.pending}`: {

            return {
                ...state,
                is_loading: true
            }
        }
        case `${summaryActions.GET_SUMMARY}${util.actionTypeSuffixes.rejected}`: {

            return {
                ...state,
                one_line_summary: "ERROR",
                one_paragraph_summary: "ERROR",
                is_loading: false
            }
        }
        default:
            return state
    }
}
