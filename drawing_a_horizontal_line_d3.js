
// March 26-28th: How to draw a horizontal line between start and end points (D3)

// Full code: https://github.com/DallasMorningNews/embed_sales_tax_timeline/blob/master/src/js/scripts.js 

// Specify x1, x2, and y1, y2 but in your return function only call them x and y. 
// The lineOffset is just a variable Allan made that moves the lines down because they weren’t lining up properly with the text labels on the y-axis. 


g.selectAll(".line")
     .data(data)
   .enter().append("line")
   .attr("class", "line")
    .attr("x1", function(d) { return x(d.start); })
    .attr("y1", function(d) { return y(d.city) + lineOffset; })
    .attr("x2", function(d) { return x(d.end); })
    .attr("y2", function(d) { return y(d.city) + lineOffset; })





