Ext.define('pilight.submaster.Panel', {
    extend:'Ext.form.Panel',
    items:[],
    frame:true,
    layout:'hbox',
    locked:false,
    backlog:{},
    initComponent:function(){
        var me = this;

        me.socket.sendCommand({module:'submaster', command:'getValues'}, function(data){
            var addChannel = function(channel, value){
                var fader = Ext.create('Ext.slider.Single', {
                    fieldLabel:channel,
                    name:channel,
                    vertical:true,
                    labelAlign:'top',
                    width:50,
                    height:200,
                    maxValue:255,
                    value:value
                });

                fader.on('change', function(slider, value){
                    if (me.suspended) return;
                    if (me.locked) {
                        return me.backlog[channel] = value;
                    }
                    me.locked = true;

                    var callback = function(){
                        for (var key in me.backlog) {
                            var value = me.backlog[key];
                            delete me.backlog[key];
                            return me.socket.sendCommand({module:'submaster', command:'setChannelValue', params:{channel:key, value:value}}, callback);
                        }
                        me.locked = false;
                    }
                    me.socket.sendCommand({module:'submaster', command:'setChannelValue', params:{channel:channel, value:value}}, callback);
                });

                me.add(fader);
            }

            for (var channel in data) addChannel(channel, data[channel]);
        });

        me.socket.listen('submaster', me);
        me.callParent(this, arguments)
    },
    receiveEvent:function(data) {
        var me = this;
        if (typeof(me.backlog[data.name]) != 'undefined') return;
        var formData = {};
        formData[data.name] = data.value;
        me.suspended = true;
        me.getForm().setValues(formData);
        me.suspended = false;
    }
});
