Ext.define('pilight.show.colorwheel.Panel', {
    extend:'Ext.form.Panel',
    layout:'hbox',
    frame:true,
    initComponent:function(){
        var me = this;
        me.defaults = {
            xtype:'slider',
            labelAlign:'top',
            vertical:true,
            width:50,
            height:200,
            listeners:{
                change:function(slider, value){
                    var data = {};
                    data[slider.name] = value;
                    me.socket.sendCommand({module:'colorwheel', command:'setParams', params:data});
                }
            }
        };

        me.callParent(arguments);
    },
    items:[{
        fieldLabel:'Saturation',
        name:'saturation',
        value:255
    }, {
        fieldLabel:'Value',
        name:'value',
        value:255
    }, {
        fieldLabel:'Speed',
        name:'speed',
        value:255
    }]
});
