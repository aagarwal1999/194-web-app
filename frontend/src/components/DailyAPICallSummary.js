import React from 'react';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
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
  return (
    <React.Fragment>
      <Title> Daily API Call Summary </Title>
      <Typography component="p" variant="h4">
        $3,024.00
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        { util.getCurrentDate() }
      </Typography>
    </React.Fragment>
  );
}