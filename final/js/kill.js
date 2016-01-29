$(function() {
    var start="allServer"; 
    $("#selected_server").val(start);
    brushmove();
});

var svg = {};
var brush = {};
var circle = {};
var allServer = {};
var s1 = {};
var s2 = {};
var s3 = {};
var s4 = {};
var s5 = {};
var s6 = {};
var s7 = {};
var s8 = {};
var s9 = {};
var s10 = {};
var s11 = {};
var s12 = {};
var s13 = {};
var s14 = {};

var colors = {
  "1": "#5687d1",
  "2": "#ffcc66",
  "3": "#de783b",
  "4": "#6ab975",
  "5": "#993366", //a173d1 BlockBreak
  "6": "#bbbbbb",
  "7": "#960505",
  "9": "#eba2ff",
  "10": "#000066",
  "11": "#99cc00",
  "12": "#ffea1c", //ffff00
  "13": "#009999",
  "14": "#ff0066"
};

drawLegend();
d3.select("#togglelegend").on("click", toggleLegend);

//var data = d3.range(800).map(Math.random);
//console.log(data);
d3.csv("data/timekills.csv", type, function(error, data) {
  if (error) throw error;


rollup = d3.nest()
  //.key(function(d) {return d["server_id"];})
  .key(function(d) {return d["start_t"];})
  .rollup(function(d) {
  return d3.sum(d, function(g) {
    return g.count;
  });
}).entries(data);
  console.log(rollup);

var margin = {top: 41, right: 50, bottom: 100, left: 50}, //bottom: 214
    width = 960 - margin.left - margin.right,
    height = 1000 - margin.top - 214-50;

var lineData = [ {"x": -15, "y": -height/2}, {"x":-15, "y": height / 2},
                 {"x": 15, "y": height/2}, {"x":15, "y": -height / 2}];

var x = d3.scale.linear()
    .domain([d3.min(data, function(d) { return d.start_t; }), d3.max(data, function(d) { return d.start_t; })])
    .range([/*d3.min(rollup, function(d) { return +d.key / 100; })*/0, width/*d3.max(rollup, function(d) { return +d.key/ 100; })*/]);

//var y = d3.random.normal(height / 2, height / 8);
var y = d3.scale.linear()
    .domain([0,14])
    .range([0,height]);

/*var*/ brush = d3.svg.brush()
    .x(x)
    .extent([d3.min(data, function(d) { return d.start_t; }), d3.max(data, function(d) { return d.start_t; })])
    .on("brushstart", brushstart)
    .on("brush", brushmove)
    .on("brushend", brushend);

var arc = d3.svg.arc()
    .outerRadius(height / 2)
    .startAngle(0)
    .endAngle(function(d, i) { return i ? -Math.PI : Math.PI; });

var lineFunction = d3.svg.line()
    .x(function(d) { return d.x; })
    .y(function(d) { return d.y; })
    .interpolate("linear");

/*var*/ svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.svg.axis().scale(x).orient("bottom"));

/*var*/ circle = svg.append("g").selectAll("circle")
    .data(data)
  .enter().append("circle")
    .attr("transform", function(d) { 
      //var s = brush.extent();
      //if(+d.key/*d.start_t*/ >= s[0] && +d.key/*d.start_t*/ <= s[1]){
        return "translate(" + x(+d.start_t/*d.start_t*/) + "," + y(14 - d.server_id/*d.server_id*/) + ")";
      }
    /*}*/)
    .attr("r", function(d) {return (d.count / 30.0)})
    .style("fill", function(d) { return colors[d.server_id]; });

var brushg = svg.append("g")
    .attr("class", "brush")
    .call(brush);

brushg.selectAll(".resize").append("path")
    .attr("transform", "translate(0," +  height / 2 + ")")
    //.style("stroke", "indianred")
    //.style("stroke-width", 5)
    .attr("d", lineFunction(lineData));

brushg.selectAll("rect")
    .attr("height", height);

brushstart();
brushmove();
});

function brushstart() {
  svg.classed("selecting", true);
}

function brushmove() {
  var s = brush.extent();
  allServer = 0;
  s1 = 0;
  s2 = 0;
  s3 = 0;
  s4 = 0;
  s5 = 0;
  s6 = 0;
  s7 = 0;
  s8 = 0;
  s9 = 0;
  s10 = 0;
  s11 = 0;
  s12 = 0;
  s13 = 0;
  s14 = 0;
  
  circle.classed("selected", function(d) {
    if(s[0] <= +d.start_t && +d.start_t <= s[1]){
      allServer += d.count;
      switch(d.server_id){
        case 1:
          s1 += d.count;
          break;
        case 2:
          s2 += d.count;
          break;
        case 3:
          s3 += d.count;
          break;
        case 4:
          s4 += d.count;
          break;
        case 5:
          s5 += d.count;
          break;
        case 6:
          s6 += d.count;
          break;
        case 7:
          s7 += d.count;
          break;
        case 8:
          s8 += d.count;
          break;
        case 9:
          s9 += d.count;
          break;
        case 10:
          s10 += d.count;
          break;
        case 11:
          s11 += d.count;
          break;
        case 12:
          s12 += d.count;
          break;
        case 13:
          s13 += d.count;
          break;
        case 14:
          s14 += d.count;
          break;
        default:
          break;
      }
    }
   return s[0] <= +d.start_t && +d.start_t <= s[1]; });

  d3.select("#totalKills")
    .text("Total Kills: " + eval(d3.select('#selected_server').property('value')))
    .style("opacity", 0.7);

  /*d3.select("#totalKills")
    .text("Total Kills From Server 1: " + s1)
    .style("opacity", 0.7);*/
  /*function(d){
    if(s[0] <= +d.key && +d.key <= s[1]){
      allServer += d.values;
    }
  }*/
}

function drawLegend() {

  // Dimensions of legend item: width, height, spacing, radius of rounded rect.
  var li = {
    w: 75, h: 30, s: 3, r: 3
  };

  var legend = d3.select("#legend").append("svg:svg")
      .attr("width", li.w)
      .attr("height", d3.keys(colors).length * (li.h + li.s));

  var g = legend.selectAll("g")
      .data(d3.entries(colors))
      .enter().append("svg:g")
      .attr("transform", function(d, i) {
              return "translate(0," + i * (li.h + li.s) + ")";
           });

  g.append("svg:rect")
      .attr("rx", li.r)
      .attr("ry", li.r)
      .attr("width", li.w)
      .attr("height", li.h)
      .style("fill", function(d) { return d.value; });

  g.append("svg:text")
      .attr("x", li.w / 2)
      .attr("y", li.h / 2)
      .attr("dy", "0.35em")
      .attr("font-size", "12px")
      .attr("font-family", "'Open Sans', sans-serif")
      .attr("text-anchor", "middle")
      .text(function(d) { return "Server ".concat(d.key); });
}

function toggleLegend() {
  var legend = d3.select("#legend");
  if (legend.style("visibility") == "hidden") {
    legend.style("visibility", "");
  } else {
    legend.style("visibility", "hidden");
  }
}

function brushend() {
  svg.classed("selecting", !d3.event.target.empty());
}

function type(d) {
  d.start_t = +d.start_t;
  d.count = +d.count;
  d.server_id = +d.server_id;
  return d;
}

/*d3.select("#totalKills")
  .text("Total Kills: " + allServer)
  .style("opacity", 0.7);*/

d3.select('#selected_server').on('change', function() {

    // erase old image
    //d3.select("svg").remove(); 
    d3.select("#totalKills")
    .text("Total Kills: " + eval(d3.select(this).property('value')))
    .style("opacity", 0.7);
    //var new_json = eval(d3.select(this).property('value'));
    //select_json(new_json);
});

