(function ($, console) {
    'use strict';

    window.WebSocket = window.WebSocket || window.MozWebSocket;

    if (!window.WebSocket) {
        $('#chat-window').prepend($('p').text('Sorry, WebSockets not supported by your browser.'));
        return;
    }

    var connection = new WebSocket('ws://' + window.location.host.substr(0, window.location.host.lastIndexOf(':')) + ':8001');

    connection.onopen = function () {
        // Stuff to do when we open our connection.
    };

    connection.onerror = function (error) {
        $('#chat-window').append($("<p>").text("Connection Error."));
    };

    connection.onmessage = function (message) {
        var response;

        try {
            response = JSON.parse(message.data);
        } catch (e) {
            console.error('Malformed response.');
            return;
        }

        if (typeof response === 'undefined' || response === null) {
            console.error('Response null.');
            return;
        }

        if ('history' in response) {
            for (var i = 0; i < response.history; ++i) {
                $('#chat-window').prepend($('<p>').text(response.history[i].message));
            }
        }

        if ('message' in response) {
            $('#chat-window').prepend($('<p>').text(response.message.sender + ': ' + response.message.message));
        }
    };

    $('#message-form').submit(function (event) {
        var chatMessageField = $('#chat-message');

        var message = chatMessageField.val();
        chatMessageField.val('');

        if (typeof message !== 'undefined' && message !== null && message !== '' ) {
            connection.send(message);
        }

        event.preventDefault();
    });
})(window.jQuery, window.console);