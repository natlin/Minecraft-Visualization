if(!d3.chart) d3.chart = {};

d3.chart.table = function() {
  var div;
  var data;
  var width;
  var dispatch = d3.dispatch(chart, "hover");
  function chart(container) {
    div = container;

    var table = container.append("table")
    update();
  }
  chart.update = update;

  function update() {
    var table = div.select("table")
    var rows = table.selectAll("tr.row")
    .data(data, function(d) { return 5 })

    console.log("table data", data)

    rows.exit().remove();
    var rowsEnter = rows.enter()
    .append("tr").classed("row", true)

    rowsEnter.append("td")
    .text(function(d) { return d.count })

    rowsEnter.append("td")
    .append("a")
    .attr({
      href: function(d) { return d.count }
    })
    .append("img")
    .attr({
      src: function(d) { return d.count }
    })

    rowsEnter.append("td")
    .append("a")
    .attr({
      href: function(d) { return d.count }
    }).text(function(d) { return d.count })

    rowsEnter.append("td")
    .text(function(d) { return d.start_t })

    rowsEnter.append("td")
    .text(function(d) { return d.stop_t })

    

    rowsEnter.on("mouseover", function(d) {
      d3.select(this).style("background-color", "orange")
      dispatch.hover([d])
    })
    rowsEnter.on("mouseout", function(d) {
      d3.select(this).style("background-color", "")
      dispatch.hover([])
    })
  }

  chart.highlight = function(data) {
    var trs = div.selectAll("tr")
    .style("background-color", "")

    trs.data(data, function(d) { return 5 })
    .style("background-color", "orange")
  }

  chart.data = function(value) {
    if(!arguments.length) return data;
    data = value;
    return chart;
  }
  chart.width = function(value) {
    if(!arguments.length) return width;
    width = value;
    return chart;
  }

  return d3.rebind(chart, dispatch, "on");
}