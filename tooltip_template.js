// here's how to make a tooltip

// make your tooltip var

var tooltip = d3.select("body").append("div").attr("class", "toolTip");


// add this to your element

    .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html("<p>" + (d.city) + "</p><p>" + (d.start_yr) + " to " + (d.end_yr) + "</p>");
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});


// as in:
g.selectAll("dot")
    .data(data)
  .enter().append("circle")
    .classed('circle-marker', true)
    .attr("r", 4)
    .attr("cx", function(d) { return x(d.start); })
    .attr("cy", function(d) { return y(d.city) + lineOffset; })
    .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html("<p>" + (d.city) + "</p><p>" + (d.start_yr) + " to " + (d.end_yr) + "</p>");
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});


// some good styles 

.toolTip {
  text-align: left;
  font-family: $sans;
  background-color: $black33;
  color: white;
  &:after {
    @include psuedoElement(10px, 10px, absolute);
    background-color: $black33;
    bottom: -5px;
    left: 50%;
    margin-left: -5px;
    @include rotate(45deg);
  }
  p {
    margin: 0 !important;
    &:first-of-type {
      font-weight: 700;
    }
  }
}


// and add a pointer cursor to whatever element you attach this to. Like so:

.circle-marker {
  fill: white;
  stroke-width: 2px;
  stroke: $dmnblue;
  cursor: pointer; <-- like this 
}