Ext.define('pilight.messaging.Message', {
    extend:'Ext.data.Model',
    fields:[
        {name:'message', type:'string'}
    ]
});

Ext.define('pilight.messaging.Panel', {
    extend:'Ext.grid.Panel',
    border:false,
    columns:[
        {header:'Text', dataIndex:'message', flex:1}
    ],
    initComponent:function(){
        var me = this;
        me.store = Ext.create('Ext.data.Store', {
            model:'pilight.messaging.Message'
        });
        me.socket.listen('messenger', me);
        me.callParent(arguments);
    },
    receiveEvent:function(event){
        var me = this;
        while (me.store.getCount() > 10) me.store.removeAt(10);
        var log = Ext.create('pilight.messaging.Message', event);
        me.store.insert(0, log);
    }
});
