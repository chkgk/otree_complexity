function draw_rect(element, id, x, y, w, h, t, base_color) {
    let rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("id", `${id}_outer`);
    rect.setAttribute("x", x);
    rect.setAttribute("y", y);
    rect.setAttribute("width", w);
    rect.setAttribute("height", h);
    rect.setAttribute("stroke", "black");
    rect.setAttribute("stroke-width", "2");
    rect.setAttribute("shape-rendering", "crispEdges");
    rect.setAttribute("fill", base_color);
    
    let l_x = x;
    let l_y = y;
    let l_w = w / 4;
    let l_h = h;
    
    let r_x = x + 3/4 * w;
    let r_y = y;
    let r_w = w / 4;
    let r_h = h;
    
    let t_fs = 20;
    let t_x = x + w / 2;
    let t_y = y + h / 2 + t_fs/2 - 2;
    
    let leftRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    leftRect.setAttribute("id", `${id}_left`);
    leftRect.setAttribute("x", l_x);
    leftRect.setAttribute("y", l_y);
    leftRect.setAttribute("width", l_w);
    leftRect.setAttribute("height", l_h);
    leftRect.setAttribute("stroke", "black");
    leftRect.setAttribute("stroke-width", "2");
    leftRect.setAttribute("shape-rendering", "crispEdges");
    leftRect.setAttribute("fill", "white");
    
    let rightRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rightRect.setAttribute("id", `${id}_right`);
    rightRect.setAttribute("x", r_x);
    rightRect.setAttribute("y", r_y);
    rightRect.setAttribute("width", r_w);
    rightRect.setAttribute("height", r_h);
    rightRect.setAttribute("stroke", "black");
    rightRect.setAttribute("stroke-width", "2");
    rightRect.setAttribute("shape-rendering", "crispEdges");
    rightRect.setAttribute("fill", "white");
    
    let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("id", `${id}_text`);
    text.setAttribute("x", t_x);
    text.setAttribute("y", t_y);
    text.setAttribute("font-size", `${t_fs}px`);
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("fill", "black");
    text.textContent = t;
    
    element.appendChild(rect);
    element.appendChild(leftRect);
    element.appendChild(rightRect);
    element.appendChild(text);
}

function draw_connector(element, x, y, l) {
    let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x);
    line.setAttribute("y1", y);
    line.setAttribute("x2", x+l);
    line.setAttribute("y2", y);
    line.setAttribute("stroke", "black");
    line.setAttribute("stroke-width", "2");
    element.appendChild(line);
}

function draw_loop(element, x, y, l, box_height) {
    let long_line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    long_line.setAttribute("x1", x);
    long_line.setAttribute("y1", y);
    long_line.setAttribute("x2", x + l);
    long_line.setAttribute("y2", y);
    long_line.setAttribute("stroke", "black");
    long_line.setAttribute("stroke-width", "2");
    
    let vert1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vert1.setAttribute("x1", x);
    vert1.setAttribute("y1", y-box_height);
    vert1.setAttribute("x2", x);
    vert1.setAttribute("y2", y);
    vert1.setAttribute("stroke", "black");
    vert1.setAttribute("stroke-width", "2");
    
    let vert2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vert2.setAttribute("x1", x + l);
    vert2.setAttribute("y1", y-box_height);
    vert2.setAttribute("x2", x + l);
    vert2.setAttribute("y2", y);
    vert2.setAttribute("stroke", "black");
    vert2.setAttribute("stroke-width", "2");
    
    element.appendChild(long_line)
    element.appendChild(vert1);
    element.appendChild(vert2);
}

function draw_row_connector(element, x, y, l, box_height) {
    let long_line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    long_line.setAttribute("x1", x);
    long_line.setAttribute("y1", y);
    long_line.setAttribute("x2", x + l);
    long_line.setAttribute("y2", y);
    long_line.setAttribute("stroke", "black");
    long_line.setAttribute("stroke-width", "2");
    
    let vert1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vert1.setAttribute("x1", x);
    vert1.setAttribute("y1", y+box_height);
    vert1.setAttribute("x2", x);
    vert1.setAttribute("y2", y);
    vert1.setAttribute("stroke", "black");
    vert1.setAttribute("stroke-width", "2");
    
    let vert2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vert2.setAttribute("x1", x + l);
    vert2.setAttribute("y1", y-box_height);
    vert2.setAttribute("x2", x + l);
    vert2.setAttribute("y2", y);
    vert2.setAttribute("stroke", "black");
    vert2.setAttribute("stroke-width", "2");
    
    element.appendChild(long_line)
    element.appendChild(vert1);
    element.appendChild(vert2);
}

function draw_start_connector(element, x, y, l, n, box_height) {
    console.log(n);
    let long_line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    long_line.setAttribute("x1", x);
    long_line.setAttribute("y1", y);
    long_line.setAttribute("x2", x + l);
    long_line.setAttribute("y2", y);
    long_line.setAttribute("stroke", "black");
    long_line.setAttribute("stroke-width", "2");
    
    let vert1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vert1.setAttribute("x1", x);
    vert1.setAttribute("y1", y - n * box_height - (n-1) * box_height);
    vert1.setAttribute("x2", x);
    vert1.setAttribute("y2", y);
    vert1.setAttribute("stroke", "black");
    vert1.setAttribute("stroke-width", "2");
    
    let vert2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    vert2.setAttribute("x1", x + l);
    vert2.setAttribute("y1", y - box_height);
    vert2.setAttribute("x2", x + l);
    vert2.setAttribute("y2", y);
    vert2.setAttribute("stroke", "black");
    vert2.setAttribute("stroke-width", "2");
    
    let horz1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    horz1.setAttribute("x1", x);
    horz1.setAttribute("y1", y - n * box_height - (n-1) * box_height);
    horz1.setAttribute("x2", x + 30);
    horz1.setAttribute("y2", y - n * box_height - (n-1) * box_height);
    horz1.setAttribute("stroke", "black");
    horz1.setAttribute("stroke-width", "2");
    
    element.appendChild(long_line)
    element.appendChild(vert1);
    element.appendChild(vert2);
    element.appendChild(horz1);
}

    
function get_connector_length(num_elements, box_width) {
    // 860 is 1000 - 4x20 (spacing between connector lines) - 2x30 (spacing between svg borders and connectors)
    return (860 - box_width*num_elements)/(num_elements+1);
}


function draw_row(element, n, row_num, start_id, start_x, box_width, box_height, first_start_y, own_id) {
    let connector_length = get_connector_length(n, box_width);
    let start_y = first_start_y + row_num * 2 * box_height;
    for (let i = 0; i < n; i++) {
        let id = start_id + i + 1;
        let base_color = id == own_id ? "#DCDCDC" : "white";
        let x = start_x + connector_length + i * (connector_length + box_width);
        draw_rect(element, `p${id}`, x, start_y, box_width, box_height, id, base_color);
        draw_connector(element, start_x + i * (box_width + connector_length), start_y + box_height/2, connector_length, box_height);
    }
    // draw connectors between elements and at the end of items
    draw_connector(element, start_x + n * (box_width + connector_length), start_y + box_height/2, connector_length, box_height);
}

function draw_rows(element, n, own_id) {
    let box_height = 50;
    let box_width = 100;
    let base_x = 30;
    let first_start_y = 10;
    let start_x = base_x + 40;
    
    // equalize rows
    let num_rows = Math.ceil(n / 7);  // 20 = 3 rows
    let num_elements = Math.floor(n / num_rows); // 20 / 3 = 6
    let remainder = n % num_rows; // 20 % 3 = 2
    
    if (remainder > 0) {
        if (remainder < num_rows) {
            num_elements += 1;
            remainder = n - num_elements * (num_rows-1);
        } else {
            num_rows += 1;
        }
    }
    
    // determine required figure height:
    // box_height = 50 
    // spacing between boxes is 50
    // the lines need another 5 or so
    
    let figure_height = num_rows * box_height * 2;
    element.setAttribute("viewBox", `0 0 1000 ${figure_height}`);
    
    for (let i = 0; i < num_rows; i++) {
        let ne;
        let start = i * num_elements;
        let end = (i+1) * num_elements;
        ne = end - start;
        if (i === num_rows -1 && remainder > 0 && ne > remainder) {
            ne = remainder;
        }
        // draw row
        draw_row(element, ne, i, start, start_x, box_width, box_height, first_start_y, own_id);
        
        // draw connectors between rows
        let connector_length = get_connector_length(ne, box_width);
        let start_y = first_start_y + i * 2 * box_height;
        if (num_rows > 1 && i < num_rows - 1) {
            draw_row_connector(element, start_x, start_y + box_height * 1.5, (ne + 1) * connector_length + ne * box_width, box_height);
        } else {
            if (num_rows === 1) {
                draw_loop(element, start_x, start_y+box_height*1.5, (n+1)*connector_length + n * box_width, box_height);
            } else {
                let start_y = first_start_y + i * 2 * box_height;
                draw_start_connector(element, start_x - base_x, start_y + box_height * 1.5, (ne + 1) * connector_length + ne * box_width + base_x, num_rows, box_height);
            }
        }
    }
}