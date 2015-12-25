Ext.define('pilight.submaster.Panel', {
    extend:'Ext.form.Panel',
    items:[],
    frame:true,
    layout:'hbox',
    locked:false,
    backlog:{},
    initComponent:function(){
        var me = this;

        var submaster = Ext.create('pilight.submaster.Submaster', {
            socket:me.socket,
            id:me.id
        });
        
        submaster.getChannels(function(channels){
            channels.forEach(function(channel){
                var name = channel.name;
                var fader = Ext.create('Ext.slider.Single', {
                    fieldLabel:name,
                    name:name,
                    vertical:true,
                    labelAlign:'top',
                    width:50,
                    height:200,
                    maxValue:255,
                    value:channel.getValue()
                });

                var sendValue = function(value){
                    if (me.suspended) return;
                    if (me.locked) {
                        return me.backlog[name] = value;
                    }
                    me.locked = true;

                    var callback = function(){
                        me.locked = false;
                        for (var key in me.backlog) {
                            var value = me.backlog[key];
                            delete me.backlog[key];
                            sendValue(value);
                        }
                    }
                    channel.setValue(value, callback);
                };

                fader.on('change', function(slider, value){
                    sendValue(value)
                });

                var button = Ext.create('Ext.button.Button', {
                    text:'Flash',
                    listeners:{
                        render:function() {
                            var value = false;
                            this.el.on({
                                mousedown:function(){
                                    var v = fader.getValue();
                                    if (v == 255) return;
                                    value = v;
                                    sendValue(255);
                                },
                                mouseup:function(){
                                    if (value !== false) sendValue(value);
                                    value = false;
                                },
                                mouseout:function(){
                                    if (value !== false) sendValue(value);
                                    value = false;
                                }
                            });
                        }
                    }
                });

                channel.on('valueChanged', function(value){
                    if (typeof(me.backlog[name]) != 'undefined') return;
                    var formData = {};
                    formData[name] = value;
                    me.suspended = true;
                    me.getForm().setValues(formData);
                    me.suspended = false;
                });

                me.add({
                    xtype:'container',
                    border:false,
                    items:[
                       fader,
                       button
                    ]
                });
            });
        });

        me.callParent(this, arguments)
    },
});
