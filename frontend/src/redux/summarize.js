import Alert from "react-s-alert"
import util from "../util"

const dashboardActions = {
    GET_SUMMARY: "GET_SUMMARY",
    GET_INITIAL_DATA: "GET_INITIAL_DATA",
    REFRESH_DATA: "REFRESH_DATA",
    REFRESH_PROD_METRICS: "REFRESH_PROD_METRICS",
}

export const getSummary = (text) => ({
    type: dashboardActions.GET_SUMMARY,
    payload: fetch("/api/summarize", {
        headers: util.getJsonHeader(),
        method: 'POST',
        body: JSON.stringify(text),
    }).then(util.restHandler),
})

export const getInitialData = () => ({
    type: dashboardActions.GET_INITIAL_DATA,
    payload: fetch("/api/get-data", {
        headers: util.getJsonHeader(),
        method: 'GET',
    }).then(util.restHandler),
})

export const refreshData = () => ({
    type: dashboardActions.REFRESH_DATA,
    payload: fetch("/api/refresh-prod-calls", {
        headers: util.getJsonHeader(),
        method: 'GET',
    }).then(util.restHandler),
})

export const refreshProdMetrics = () => ({
    type: dashboardActions.REFRESH_PROD_METRICS,
    payload: fetch("/api/refresh-prod-metrics", {
        headers: util.getJsonHeader(),
        method: 'GET',
    }).then(util.restHandler),
})

const initialState = {
    summary: {
        one_paragraph_summary: "",
        one_line_summary: "",
        loading: false
    },
    data: {
        num_daily_api_calls: 0,
        recent_api_calls: [],
        metric_data: [],
        refresh_loading: false,
        refresh_metrics_loading: false
    }
}
// reducer

export const DashboardReducer = (state = initialState, action) => {
    switch (action.type) {
        case `${dashboardActions.GET_SUMMARY}${util.actionTypeSuffixes.fulfilled}`: {
            return {
                ...state,
                summary: {
                    ...state.summary,
                    one_line_summary: action.payload["one_line_summary"],
                    one_paragraph_summary: action.payload["one_paragraph_summary"],
                    is_loading: false
                },
                data: {
                    ...state.data,
                    num_daily_api_calls: action.payload["num_daily_api_calls"],
                    recent_api_calls: action.payload["recent_api_calls"].map((payload) => {
                        return {
                            ...payload,
                            time: new Date(payload.time)
                        }    
                    })
                }
            }
        }
        case `${dashboardActions.GET_SUMMARY}${util.actionTypeSuffixes.pending}`: {

            return {
                ...state,
                summary: {
                    ...state.summary,
                    is_loading: true
                }
            }
        }
        case `${dashboardActions.GET_SUMMARY}${util.actionTypeSuffixes.rejected}`: {

            return {
                ...state,
                summary: {
                    ...state.summary,
                    one_line_summary: "ERROR",
                    one_paragraph_summary: "ERROR",
                    is_loading: false
                }
            }
        }
        case `${dashboardActions.GET_INITIAL_DATA}${util.actionTypeSuffixes.fulfilled}`: {
            return {
                ...state,
                data: {
                    ...state.data,
                    num_daily_api_calls: action.payload["num_daily_api_calls"],
                    recent_api_calls: action.payload["recent_api_calls"].map((payload) => {
                        return {
                            ...payload,
                            time: new Date(payload.time)
                        }    
                    }),
                    metric_data: action.payload["metric_data"]
                }
            }
        }
        case `${dashboardActions.REFRESH_DATA}${util.actionTypeSuffixes.fulfilled}`: {
            return {
                ...state,
                data: {
                    ...state.data,
                    num_daily_api_calls: action.payload["num_daily_api_calls"],
                    refresh_loading: false,
                    recent_api_calls: action.payload["recent_api_calls"].map((payload) => {
                        return {
                            ...payload,
                            time: new Date(payload.time)
                        }    
                    }),
                }
            }
        }
        case `${dashboardActions.REFRESH_DATA}${util.actionTypeSuffixes.pending}`: {

            return {
                ...state,
                data: {
                    ...state.data,
                    refresh_loading: true,
                }
            }
        }
        case `${dashboardActions.REFRESH_DATA}${util.actionTypeSuffixes.rejected}`: {

            return {
                ...state,
                data: {
                    ...state.data,
                    refresh_loading: false,
                }
                
            }
        }
        case `${dashboardActions.REFRESH_PROD_METRICS}${util.actionTypeSuffixes.fulfilled}`: {
            return {
                ...state,
                data: {
                    ...state.data,
                    refresh_metrics_loading: false,
                    metric_data: action.payload["metric_data"]
                }
            }
        }
        case `${dashboardActions.REFRESH_PROD_METRICS}${util.actionTypeSuffixes.pending}`: {

            return {
                ...state,
                data: {
                    ...state.data,
                    refresh_metrics_loading: true,
                }
            }
        }
        case `${dashboardActions.REFRESH_PROD_METRICS}${util.actionTypeSuffixes.rejected}`: {

            return {
                ...state,
                data: {
                    ...state.data,
                    refresh_metrics_loading: false,
                }
                
            }
        }
        default:
            return state
    }
}
