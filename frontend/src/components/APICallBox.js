import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import { TextField, Button, Typography, Grid, Box} from '@material-ui/core';

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
          /> 
          </Grid>
          <Grid item xs={8}> 
          <Box ml={2}> 
            <Typography component="h4" fontWeight="fontWeightBold"> One Line Summary: </Typography>
            <Typography component="h4" fontWeight="fontWeightBold"> One Paragraph Summary: </Typography>
          </Box>
          </Grid>
        </Grid>
      </Box>
      <Box m={1}>
        <Button variant="contained" color="primary"> Call API </Button>
      </Box>
    </React.Fragment>
  );
}