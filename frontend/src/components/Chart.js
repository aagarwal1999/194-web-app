import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import { Grid } from '@material-ui/core'
import Title from './Title';
import WordCloud from './WordCloud';
import { useSelector } from 'react-redux'



export default function Chart() {
  const theme = useTheme();
  const metrics = useSelector(state => state.data.metric_data)

  const commonWords = metrics.filter(metric => metric.name === "Most Common Words")[0];
  return (
    <React.Fragment>
      <Title> Most Common Medical Words </Title>
      <Grid container> 
        <Grid item xs={6} md={6} lg={6}> 
          <WordCloud title={"Training"} words={commonWords.training.split(",")}  />
        </Grid>
        <Grid item xs={6} md={6} lg={6}> 
          <WordCloud title={"Production"} words={commonWords.production.split(",")}  />
        </Grid>
      </Grid>
      
    </React.Fragment>
  );
}