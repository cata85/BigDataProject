var createNodes = function (images, numNodes, radius) {
    function httpGet(theUrl) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
        xmlHttp.send( null );
        return JSON.parse(xmlHttp.responseText);
    }

    function getData(name) {
        for (var i=0; i<data.length; i++) {
            if (name == data[i].subreddit) {
                return data[i].data;
            }
        }
    }

    var url = 'http://localhost:5000/data/';
    var data = httpGet(url);
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
        var _data = getData(name);
        nodes.push({
            'id': name,
            'image': images[i], 
            'data': _data,
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
                    .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
        
    var setEvents1 = nodeEnter
                    .on('mouseenter', function () {
                        d3.select( this ).moveToFront();
                    })
                    .on('mouseleave', function() {
                        d3.select( this ).moveToBack();
                    });

    nodeEnter.append('svg:circle')
                    .attr('r', function (d) { return elementRadius / 2; })
                    .style('fill', '#eee');

    function getNode(nodes, id) {
        for (var i=0; i<nodes.length; i++) {
            if (nodes[i].id == id) {
                return nodes[i];
            }
        }
    }

    for (var i=0; i<nodes.length; i++) {
        var _node = nodes[i];
        var id = '#' + _node.id;
        var _data = _node.data;
        for (var key in _data) {
            var value = _data[key];
            value = value * 70.0;
            svg.select(id)
                .append('svg:path')
                .attr('class', 'paths')
                .attr('transform', function (d) { return 'translate(' + -1*d.x + ',' + -1*d.y + ')'; })
                .attr('d', function (d) {
                    var target = getNode(nodes, key)
                    var sx = _node.x, sy = _node.y,
                    tx = target.x, ty = target.y,
                    dx = tx - sx, dy = ty - sy,
                    dr = 30 * Math.sqrt(dx * dx + dy * dy);
                    // return "M" + sx + "," + sy + "A" + dr + "," + dr + " 0 0,1 " + tx + "," + ty;
                    return "M " + sx + " " + sy + " L " + tx + " " + ty;
                })
                .attr('stroke', 'grey')
                .attr('stroke-opacity', 0.1)
                .attr('stroke-width', 5);
        }
    }

    var images = nodeEnter.append('svg:image')
                    .attr('xlink:href', function (d) { return d.image; })
                    .attr('x', function (d) { return -1 * ((elementRadius * 2) / 2); })
                    .attr('y', function (d) { return -1 * ((elementRadius * 2) / 2); })
                    .attr('height', elementRadius * 2)
                    .attr('width', elementRadius * 2)
                    .attr('name', function (d) { return d.id; });

    var setEvents2 = images
                    .on('mouseenter', function () {
                        var name = this.getAttribute('name');
                        document.getElementById('name').textContent = name;
                        var id = '#' + name;
                        d3.select( id )
                          .selectAll ( '.paths' )
                          .transition()
                          .attr('stroke', 'blue')
                          .attr('stroke-opacity', 0.7)
                          .attr('stroke-width', 8);
                        d3.select( this )
                          .transition()
                          .attr('x', function (d) { return -1 * ((elementRadius * 8) / 2); })
                          .attr('y', function (d) { return -1 * ((elementRadius * 8) / 2); })
                          .attr('height', elementRadius * 8)
                          .attr('width', elementRadius * 8);
                    })
                    .on('mouseleave', function () {
                        var name = this.getAttribute('name');
                        document.getElementById('name').textContent = '';
                        var id = '#' + name;
                        d3.select( id )
                          .selectAll( '.paths' )
                          .transition()
                          .attr('stroke', 'grey')
                          .attr('stroke-opacity', 0.1)
                          .attr('stroke-width', 5);
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