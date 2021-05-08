import React from "react";
import { connect } from "react-redux";
import { getMetricsData } from "../redux/example";
import Dashboard from "../components/Dashboard";


@connect(store => ({
    // linking the redux store with this component
    one_line_summary: store.summary.one_line_summary,
    one_paragraph_summary: store.summary.one_paragraph_summary,
    is_loading: store.summary.is_loading
}))
class LandingPage extends React.Component {

    componentDidMount() {
        this.props.dispatch(getMetricsData())
    }

    render() {
        return (
            <div> 
                <Dashboard/>
            </div>
        )
    }
}

export default LandingPage
