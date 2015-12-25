Ext.define('pilight.submaster.Submaster', {
    extend:'pilight.control.Controllable',
    getId:function(){
        return this.id
    },
    getChannels:function(callback){
        var me = this;
        if (me.channels) return callback(me.channels);
        me.sendCommand('getValues', function(res){
            var channels = [];
            for (var name in res) {
                var channel = Ext.create('pilight.submaster.Channel', {
                    submaster:me,
                    name:name,
                    value:res[name]
                });
                channels.push(channel);
            }
            me.channels = channels;
            callback(channels);
        });
    },
    setValue:function(channel, value, callback){
        this.sendCommand('setChannelValue', {channel:channel.name, value:value}, callback);
    },
    getChannel:function(name){
        var me = this;
        for (var i = 0; i < me.channels.length; i++) {
            if (me.channels[i].name == name) return me.channels[i];
        }
        return false;
    },
    receiveEvent:function(event){
        var me = this;
        var name = event.name;
        var channel = me.getChannel(name);
        if (!channel) return;
        channel.updateValue(event.value);
    }
});
