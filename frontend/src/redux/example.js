import Alert from "react-s-alert"
import util from "../util"

const exampleActions = {
    GET_EXAMPLES: "GET_EXAMPLES",
    CREATE_EXAMPLE: "CREATE_EXAMPLE",
}

export const getMetricsData = () => ({
    type: exampleActions.GET_EXAMPLES,
    payload: fetch("/api/examples", {
        headers: util.getJsonHeader(),
    }).then(util.restHandler),
})

const initialState = {
    one_paragraph_summary: "",
    one_line_summary: "",
    loading: false
}

// reducer

export const ExampleReducer = (state = initialState, action) => {
    switch (action.type) {
        case `${exampleActions.GET_EXAMPLES}${util.actionTypeSuffixes.fulfilled}`: {
            return {
                ...state,
                exampleList: action.payload,
            }
        }
        case `${exampleActions.CREATE_EXAMPLE}${util.actionTypeSuffixes.fulfilled}`: {
            Alert.success("Successfully created example")
            return state
        }
        default:
            return state
    }
}
