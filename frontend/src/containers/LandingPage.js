import React from "react";
import { connect } from "react-redux";
import { getMetricsData } from "../redux/example";
import Dashboard from "../components/Dashboard";


@connect(store => ({
    // linking the redux store with this component
    examples: store.example.exampleList,
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
