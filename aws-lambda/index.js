const ws = require('nodejs-websocket');

exports.handler = (event, context, callback) => {
    const server = process.env.PILIGHT_URL;
    var state;
    const connection = ws.connect(server, () => {
        connection.on('text', (text) => {
            var json = JSON.parse(text);
            if (state === 'getValues') {
                var value = 255;
                if (json.data.halogen > 0) {
                    value = 0;
                }
                const msg = {module:'submaster', command:'setChannelValue', params:{channel:'halogen', value:value}};
                state = 'setValues';
                connection.sendText(JSON.stringify(msg));
            } else if (state === 'setValues') {
                connection.close();
            }
        });
        state = 'getValues';
        connection.sendText(JSON.stringify({module:'submaster', command:'getValues'}));
    });

    connection.on('close', (code, reason) => {
        callback();
    });

};

exports.handler(null,null,(err, res) => {
});
