Ext.define('pilight.control.Controllable', {
    constructor:function(config){
        Ext.apply(this, config);
        this.socket.listen(this.getId(), this);
    },
    receiveEvent:function(event){
    },
    sendCommand:function(command, params, callback){
        if (typeof(params) == 'function') {
            callback = params;
            params = undefined;
        }
        var c = {
            module:this.getId(),
            command:command
        }
        if (typeof(params) != 'undefined') c.params = params;
        this.socket.sendCommand(c, callback);
    }
});
