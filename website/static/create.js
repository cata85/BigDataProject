var createNodes = function (images, numNodes, radius) {
    var nodes = [],
        width = (radius * 2) + 50,
        height = (radius * 2) + 50,
        angle,
        x,
        y,
        i;
    for (i=0; i<numNodes; i++) {
        angle = (i / (numNodes/2)) * Math.PI;
        x = (radius * Math.cos(angle)) + (width/2);
        y = (radius * Math.sin(angle)) + (width/2);
        dirt_name = images[i].replace('.png', '');
        name = dirt_name.replace('static/images/', '');
        nodes.push({
            'id': 'c' + i, 
            'name': name,
            'image': images[i], 
            'x': x, 
            'y': y
        });
    }
    return nodes;
}

var createSvg = function (radius, callback) {
    d3.selectAll('svg').remove();
    var svg = d3.select('#canvas').append('svg:svg')
                 .attr('width', (radius * 2) + 50)
                 .attr('height', (radius * 2) + 50);
    callback(svg);
}

// function readTextFile(file, callback) {
//     var rawFile = new XMLHttpRequest();
//     rawFile.overrideMimeType("application/json");
//     rawFile.open("GET", file, true);
//     rawFile.onreadystatechange = function() {
//         if (rawFile.readyState === 4 && rawFile.status == "200") {
//             callback(rawFile.responseText);
//         }
//     }
//     rawFile.send(null);
// }

var createElements = function (svg, nodes, elementRadius) {
    'use strict';

    d3.selection.prototype.moveToFront = function() {  
        return this.each(function(){
          this.parentNode.appendChild(this);
        });
      };
      d3.selection.prototype.moveToBack = function() {  
          return this.each(function() { 
              var firstChild = this.parentNode.firstChild; 
              if (firstChild) { 
                  this.parentNode.insertBefore(this, firstChild); 
              } 
          });
      };

    var node = svg.selectAll('g.node')
                    .data(nodes, function (d) { return d.id; 
                    });

    var nodeEnter = node.enter().append('svg:g')
                    .attr('class', 'node')
                    .attr('id', function (d) { return d.id; })
                    .attr('name', function (d) { return d.name; })
                    .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
        
    var setEvents1 = nodeEnter
                    .on('mouseenter', function () {
                        d3.select( this ).moveToFront();
                        var name = this.getAttribute('name');
                        document.getElementById('name').textContent = name;
                    })
                    .on('mouseleave', function() {
                        d3.select( this ).moveToBack();
                        document.getElementById('name').textContent = '';
                    });

    nodeEnter.append('svg:circle')
                    .attr('r', function (d) { return elementRadius / 2; })
                    .attr('name', function (d) { return d.name; })
                    .style('fill', '#eee');

    svg.selectAll('g.node')
                    .append('path')
                    .attr('d', function (d) { 
                        var sx = d.source.x, sy = d.source.y,
                        tx = d.target.x, ty = d.target.y,
                        dx = tx - sx, dy = ty - sy,
                        dr = 2 * Math.sqrt(dx * dx + dy * dy);
                        return "M" + sx + "," + sy + "A" + dr + "," + dr + " 0 0,1 " + tx + "," + ty;
                    });

    // readTextFile("static/data.json", function(text){
    //     var data = JSON.parse(text);
    //     console.log(data);
    // });

    var images = nodeEnter.append('svg:image')
                    .attr('xlink:href', function (d) { return d.image; })
                    // .attr('id', function (d) { return d.id; })
                    .attr('x', function (d) { return -1 * ((elementRadius * 2) / 2); })
                    .attr('y', function (d) { return -1 * ((elementRadius * 2) / 2); })
                    .attr('height', elementRadius * 2)
                    .attr('width', elementRadius * 2);

    var setEvents2 = images
                    .on('mouseenter', function () {
                        d3.select( this )
                          .transition()
                          .attr('x', function (d) { return -1 * ((elementRadius * 8) / 2); })
                          .attr('y', function (d) { return -1 * ((elementRadius * 8) / 2); })
                          .attr('height', elementRadius * 8)
                          .attr('width', elementRadius * 8);
                    })
                    .on('mouseleave', function () {
                        d3.select( this )
                          .transition()
                          .attr('x', function (d) { return -1 * ((elementRadius * 2) / 2); })
                          .attr('y', function (d) { return -1 * ((elementRadius * 2) / 2); })
                          .attr('height', elementRadius * 2)
                          .attr('width', elementRadius * 2);
                    });
}

function draw (images, numNodes, radius) {
    numNodes = numNodes || 100;
    radius = radius || 200;
    var nodes = createNodes(images, numNodes, radius);
    createSvg(radius, function (svg) {
        createElements(svg, nodes, 10);
    });
}