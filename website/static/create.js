var createNodes = function (images, numNodes, radius) {
    console.log('third');
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
        nodes.push({'id': i, 'image': images[i], 'x': x, 'y': y});
    }
    return nodes;
}

var createSvg = function (radius, callback) {
    console.log('fouth');
    d3.selectAll('svg').remove();
    var svg = d3.select('#canvas').append('svg:svg')
                 .attr('width', (radius * 2) + 50)
                 .attr('height', (radius * 2) + 50);
    callback(svg);
}

var createElements = function (svg, nodes, elementRadius) {
    var node = svg.selectAll('g.node')
                    .data(nodes, function (d) { return d.id; 
                    });

    var nodeEnter = node.enter().append('svg:g')
                    .attr('class', 'node')
                    .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });

    nodeEnter.append('svg:circle')
                    .attr('r', elementRadius)
                    .style('fill', '#eee');

    var images = nodeEnter.append('svg:image')
                    .attr('xlink:href', function (d) { return d.image; })
                    .attr('x', function (d) { return -1 * ((elementRadius * 2) / 2); })
                    .attr('y', function (d) { return -1 * ((elementRadius * 2) / 2); })
                    .attr('height', elementRadius * 2)
                    .attr('width', elementRadius * 2);
}

function draw (images, numNodes, radius) {
    console.log('second');
    numNodes = numNodes || 100;
    radius = radius || 200;
    var nodes = createNodes(images, numNodes, radius);
    createSvg(radius, function (svg) {
        createElements(svg, nodes, 10);
    });
}