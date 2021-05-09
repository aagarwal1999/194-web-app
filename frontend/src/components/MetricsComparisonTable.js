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
import { refreshProdMetrics } from "../redux/summarize"


function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles((theme) => ({
  seeMore: {
    marginTop: theme.spacing(3),
  },
}));

function renderAPICallButton() {
  const is_loading = useSelector(state => state.data.refresh_metrics_loading)
  const dispatch = useDispatch()
  if(!is_loading){
    return (
      <Button variant="contained" color="primary" onClick={() => dispatch(refreshProdMetrics())}> Refresh </Button>
    )
  }

  return (
    <Button disabled variant="contained" color="primary"> <CircularProgress size={20} /> </Button>
  )
}

export default function MetricsComparisonTable() {
  const classes = useStyles();
  const rows = useSelector(state => state.data.metric_data)
  return (
    <React.Fragment>
      <Grid container direction="row" justify="space-between" alignItems="stretch" > 
        <Grid item xs={10}> 
          <Title> Metrics </Title>
        </Grid>
        <Grid item xs={2}> 
          { renderAPICallButton() }
        </Grid>
      </Grid> 
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Metric</TableCell>
            <TableCell>Production</TableCell>
            <TableCell> Training </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.filter((row) => !isNaN(row.training) && !isNaN(row.production)).map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.training}</TableCell>
              <TableCell>{row.production}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}