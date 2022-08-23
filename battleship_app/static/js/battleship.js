//SOCKET, PLAYER, RESET_URL and CLIENT_RESET_URL are initialized in the base.html file


// Updating html for message receiver
SOCKET.on('message', function(message){
    [msg_type, msg, player] = message.split('@');

    if (msg_type == 'reload'){
        location.reload();
    } else if (msg_type == 'reset') {
        window.location = CLIENT_RESET_URL;
    } else if (msg_type == 'ready') {
        alert(`${player} is ready!`)
        location.reload();
    } else {
        if (player != PLAYER) {
            alert(msg);
            location.reload();
        }
    }
});


// Shortened document getters
function getId(id) {return document.getElementById(id);};

function dataDivId(id) {return document.querySelector(`[data-div_id='${id}']`);};

function dataInputId(id) {return document.querySelector(`[data-input_id='${id}']`);};


// Sets the player at index.html
function onPlayerSelect(player){
    var form = getId('battleship_player_form')
    var input = getId(player)
    input.value = '1'
    form.submit()
};


// Drag and drop functions
function allowDrop(ev) {ev.preventDefault();};

function drag(ev) {ev.dataTransfer.setData("text", ev.target.id);};

function drop(ev) {
    ev.preventDefault();
    // Set data was set as text and the boat div id
    var boat = ev.dataTransfer.getData("text");

    var from_p = getId(`p_${boat}`)
    var from_div = getId(boat);
    var len_from_div = from_div.children.length;

    var to_div = ev.srcElement;

    // Div and hidden input dataset.div_id or dataset.input_id are formatted as '<grid letter>|<grid number>|<boat name OR none>'
    var [chr, col, x] = to_div.dataset.div_id.split('|');
    var chr_code = chr.charCodeAt(0)
    col = parseInt(col);

    var i = 0;
    var adjust = 0;
    var do_replace = [];
    var fill_input;
    var replace;

    if (from_div.dataset.orient == 'horizontal'){
        // If the boat is horizontal, i gets incremented
        // adjust will check for if the boat would be off the grid and will set back the boat
        if (col + len_from_div > 10){
            adjust = (col + len_from_div - 1) - 10;
            i -= adjust;
        }

        // Adding the boat div and replacement div to a list
        for (i; i < len_from_div-adjust; i++){
            replace = dataDivId(`${chr}|${col+i}|none`);
            if (replace.classList.contains('fill')){
                return;
            } else {
                do_replace.push([from_div.children[i+adjust], replace])
            }
        }
    } else {
        // If the boat is vertical, chr_code gets incremented and then sent back to the letter value
        // adjust will check for if the boat would be off the grid and will set back the boat
        var j_chr = 'J'.charCodeAt(0)
        if (chr_code + len_from_div > j_chr){
            adjust = (chr_code + len_from_div - 1) - j_chr;
            i -= adjust;
        }

        var new_chr;
        for (i; i < len_from_div-adjust; i++){
            new_chr = String.fromCharCode(chr_code + i)
            replace = dataDivId(`${new_chr}|${col}|none`);
            if (replace.classList.contains('fill')){
                return;
            } else {
                do_replace.push([from_div.children[i+adjust], replace])
            }
        }

    }

    for (var j = 0; j < do_replace.length; j++){
        // Sets names and values for the input to be sent to flask in a POST request
        var [letter, number, x] = do_replace[j][1].dataset.div_id.split('|');
        var new_id = `i?${letter}|${number}|${boat}`
        fill_input = dataInputId(`i?${do_replace[j][1].dataset.div_id}`);
        fill_input.name = new_id;
        fill_input.dataset.input_id = new_id;
        fill_input.value = 'fill';
        do_replace[j][0].dataset.div_id = new_id;
        do_replace[j][1].replaceWith(do_replace[j][0])
    }
    from_p.remove();
    updateBoatCounter();
}


function onRotate(rotater){
    // Rotates the div that contains the boat cells
    var rotated = getId(rotater.id.split('|')[1])

    if (rotated.style.transform == 'rotate(90deg)'){
        rotated.style.transform = 'rotate(0deg)';
        rotated.dataset.orient = 'horizontal';
    } else {
        rotated.style.transform = 'rotate(90deg)';
        rotated.dataset.orient = 'vertical';
    }
}


function updateBoatCounter(){
    // Checks if all boats are placed on the grid
    // Updates the value for a hidden input
    var boats = getId('boat_counter');
    var num_boats = parseInt(boats.value);
    num_boats ++;
    boats.value = `${num_boats}`;
    if (num_boats == 5){
        var boats_ready = getId('boats_ready')
        boats_ready.style.visibility = 'visible';
    }
}

function onHitSelect(elem, player, p_ready, p_turn, o_ready){
    // Asynchronous POST request when the user has clicked a selected a grid cell
    var cell = elem.firstChild.nextSibling.dataset.div_id;

    if (p_ready === false){
        return
    } else if (o_ready === false) {
        alert('Other player is not ready');
        return
    } else if (p_turn === false) {
        alert('Not your turn')
        return
    } else {
        body = {
            'player': player,
            'cell': cell,
        };
        fetch(`${window.origin}/hit_select`, {
            method: 'POST',
            credentials: 'include',
            body: JSON.stringify(body),
            cache: 'no-cache',
            headers: new Headers({
                'content-type': 'application/json'
            })
        })
        .then(function(response) {
            if (response.status !== 200) {
                console.log(`Response was not 200: ${response.status}`);
            } else {
                response.json().then(function(data){
                    console.log(data);
                    alert(data['message']);
                    location.reload()
                })
            }
        })
    }
}


