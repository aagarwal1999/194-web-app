import React, {Component} from 'react';
var cloud = require('d3-cloud');
import * as d3 from 'd3';
import { Typography } from '@material-ui/core';
 

class WordCloud extends React.Component {

    constructor(props) {
      super(props);
      this.myRef = React.createRef(); 

    }
  
    componentDidMount() {
        const fill = d3.scale.category20();
        var svg = d3.select(this.myRef.current)
               .append('svg')
               .attr('width', 500)
               .attr('height', 200);
        var words = this.props.words
        var layout = cloud()
            .size([500, 200])
            .words(words.map(function(d) {
                return {text: d, size: 4 + Math.random() * 50, test: "haha"};
            }))
            .padding(5)
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", draw);

        layout.start();
        console.log(d3.version)

        function draw(words) {
            svg.attr("width", layout.size()[0])
            .attr("height", layout.size()[1])
            .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i)})
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
        }
    }

    render () {
        return (
            <div> 
            <Typography component="h3" variant="subtitle1" color="primary" gutterBottom > { this.props.title} </Typography>
            <div ref={this.myRef}></div>
            </div> 
        )
    }
  }
  
export default WordCloud;