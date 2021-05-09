import React from "react";
import { connect } from "react-redux";
import { getInitialData } from "../redux/summarize";
import Dashboard from "../components/Dashboard";


@connect(store => ({
    // linking the redux store with this component
    summary:  store.summary,
}))
class LandingPage extends React.Component {

    componentDidMount() {
        this.props.dispatch(getInitialData())
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
