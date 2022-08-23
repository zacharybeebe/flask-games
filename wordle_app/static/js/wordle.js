//SOCKET, RESET_URL and CLIENT_RESET_URL are initialized in the base.html file


// Updating html for message receiver
SOCKET.on('message', function(message){
    [msg_type, msg] = message.split('!');

    if (msg_type == 'reload'){
        location.reload();
    } else if (msg_type == 'reset') {
        window.location = CLIENT_RESET_URL;
    } else {
        [input_value, input_id, next_id] = msg.split('?')

        if (input_value == 'null'){
            console.log('reloading...')
            location.reload();
        } else {
            console.log('updating input...')
            var input = getId(input_id);
            input.value = input_value;

            if (next_id != 'null'){
                var next_input = getId(next_id);
                next_input.focus();
                input.blur();
            }
        }
    }
});

// Shortened document.getElementById
function getId(id) {return document.getElementById(id);};


// Submit wordle guess - submits to index
function onFormSubmit(){
    form = getId('wordle_form')
    form.submit()
};

// Checking input character, advancing to next input box and
// sending the updated character to the other user
function onLetter(input, regex){
    var next_id;
    if (!regex.test(input.value)){
        input.value = '';
        next_id = 'null'
    } else {
        if (input.value.length > 1) {
            input.value = input.value.slice(0, 1);
        }
        var next_idx = parseInt(input.dataset.idx) + 1;
        if (next_idx == 5) {
            next_id = 'null';
        } else {
            var next = input.parentElement.parentElement.children[next_idx].children[0]
            input.value
            next.focus();
            input.blur();
            next_id = next.id;
        }
    }
    var message = `update_input!${input.value}?${input.id}?${next_id}`
    SOCKET.send(message);
}




