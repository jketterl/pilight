Ext.define('pilight.ConnectWindow', {
    extend:'Ext.window.Window',
    title:'Connect to pilight',
    connectionHandler:function(host, port){},
    initComponent:function(){
        var me = this;
        var form = Ext.create('Ext.form.Panel', {
            items:[{
                fieldLabel:'PiLight Server',
                xtype:'textfield',
                name:'host',
                value:window.location.host
            },{
                fieldLabel:'Port',
                xtype:'numberfield',
                name:'port',
                value:9001
            }]
        });

        me.items = [form];

        me.buttons = [{
            text:'Connect',
            handler:function(){
                var c = form.getValues();
                me.connectionHandler(c.host, c.port);
            }
        }];

        me.callParent(me, arguments);
    }
});
