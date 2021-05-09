import React from 'react';
import { withTheme } from '@material-ui/core/styles';
import { connect } from "react-redux";
import { TextField, Button, Typography, Grid, Box, CircularProgress} from '@material-ui/core';

import Title from './Title';
import { getSummary } from '../redux/summarize';




@connect(store => ({
  // linking the redux store with this component
  is_loading: store.summary.is_loading,
  one_line_summary: store.summary.one_line_summary,
  one_paragraph_summary: store.summary.one_paragraph_summary  
}))
class APICallBox extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      api_call_text: ""
    };
    
  }

  renderAPICallButton() {

    if(!this.props.is_loading){
      return (
        <Button variant="contained" color="primary" onClick={() => {
          if(this.state.api_call_text === ""){
            return
          }
          this.props.dispatch(getSummary(this.state.api_call_text))
        }}> Call API </Button>
      )
    }
    return (
      <Button disabled variant="contained" color="primary" > <CircularProgress size={20} /> </Button>
    )
    

  }

  render(){

    return (
      <React.Fragment>
        <Title> Try the Summary API </Title>
        <Box m={1}>
          <Grid container direction="row" justify="space-between" alignItems="stretch" > 
            <Grid item xs={4}>
            <TextField
              id="outlined-textarea"
              label="Enter Text Here"
              multiline
              variant="outlined"
              fullWidth
              rows={3}
              onChange={(event) => this.setState({api_call_text: event.target.value})                  }
            /> 
            </Grid>
            <Grid item xs={8}> 
            <Box ml={2}> 
              <Typography component="h4" fontWeight="fontWeightBold"> { `One Line Summary: ${this.props.one_line_summary}` } </Typography>
              <Typography component="h4" fontWeight="fontWeightBold"> { `One Paragraph Summary: ${this.props.one_paragraph_summary}` }</Typography>
            </Box>
            </Grid>
          </Grid>
        </Box>
        <Box m={1}>
          {this.renderAPICallButton()}
        </Box>
      </React.Fragment>
    );

  }

}

export default withTheme(APICallBox)