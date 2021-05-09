import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useSelector } from 'react-redux'
import Typography from '@material-ui/core/Typography';
import Title from './Title';
import util from '../util'

function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles({
  depositContext: {
    flex: 1,
  },
});


export default function DailyAPICallSummary() {
  const classes = useStyles();
  const num_daily_api_calls = useSelector(state => state.data.num_daily_api_calls) 
  return (
    <React.Fragment>
      <Title> Daily API Call Summary </Title>
      <Typography component="p" variant="h4">
        {num_daily_api_calls}
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        { util.getCurrentDate() }
      </Typography>
    </React.Fragment>
  );
}