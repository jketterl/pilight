Ext.define('pilight.submaster.Panel', {
    extend:'Ext.form.Panel',
    items:[],
    frame:true,
    layout:'hbox',
    initComponent:function(){
        var me = this;
        me.socket.sendCommand({module:'submaster', command:'getChannels'}, function(data){
            data.forEach(function(channel){
                var fader = Ext.create('Ext.slider.Single', {
                    fieldLabel:channel,
                    name:channel,
                    vertical:true,
                    labelAlign:'top',
                    width:50,
                    height:200,
                    maxValue:255
                });

                fader.on('change', function(slider, value){
                    me.socket.sendCommand({module:'submaster', command:'setChannelValue', params:{channel:channel, value:value}});
                });

                me.add(fader);
            });
        });
        me.callParent(this, arguments)
    }
});
