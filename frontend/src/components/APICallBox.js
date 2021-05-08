import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import { ResponsiveContainer } from "recharts";
import { TextField, Button, Typography, Grid} from '@material-ui/core';

import Title from './Title';

// Generate Sales Data
function createData(time, amount) {
  return { time, amount };
}

export default function APICallBox() {
  const theme = useTheme();

  return (
    <React.Fragment>
      <Title> Try the Summary API </Title>
      <Grid container direction="row" justify="space-between" alignItems="stretch" > 
        <Grid item xs={6}>
        <TextField
          id="outlined-textarea"
          label="Enter Text Here"
          multiline
          variant="outlined"
        /> 
        </Grid>
        <Grid item xs={6}> 
        <div> 
          <Typography component="h4" color="primary"> Results: </Typography>
        </div>
        </Grid>
      </Grid>
      <Button variant="contained" color="primary"> Call API </Button>

    </React.Fragment>
  );
}