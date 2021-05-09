import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import {Button, Grid, CircularProgress} from '@material-ui/core'
import { useSelector, useDispatch } from 'react-redux'
import Title from './Title';
import { refreshData } from "../redux/summarize"


function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles((theme) => ({
  seeMore: {
    marginTop: theme.spacing(3),
  },
}));

function renderAPICallButton() {
  const is_loading = useSelector(state => state.data.refresh_loading)
  const dispatch = useDispatch()
  if(!is_loading){
    return (
      <Button variant="contained" color="primary" onClick={() => dispatch(refreshData())}> Refresh </Button>
    )
  }

  return (
    <Button disabled variant="contained" color="primary"> <CircularProgress size={20} /> </Button>
  )
}

export default function APICalls() {
  const classes = useStyles();
  const rows = useSelector(state => state.data.recent_api_calls)

  return (
    <React.Fragment>
      <Grid container direction="row" justify="space-between" alignItems="stretch" > 
        <Grid item xs={10}> 
          <Title>Recent API Calls</Title>
        </Grid>
        <Grid item xs={2}> 
          { renderAPICallButton() }
        </Grid>
      </Grid> 
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Text</TableCell>
            <TableCell>One Line Prediction</TableCell>
            <TableCell align="right"> One Paragraph Prediction</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.time.toLocaleDateString()}</TableCell>
              <TableCell>{row.data}</TableCell>
              <TableCell>{row.one_line_summary}</TableCell>
              <TableCell align="right">{row.one_paragraph_summary}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}